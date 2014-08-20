__author__ = 'maxb'

import socket
import thread
import threading
import Queue
import time
import random
from sigils import heiroglyphs, futhark, combo
from sigil_util import *
from wizard import Wizard
# for later:
# import ssl


class Player:
    def __init__(self):
        self.ctos_queue = None
        self.stoc_queue = None
        self.uuid = None
        self.wizard = Wizard()


def handle_initial(clientsock, addr):
    print "Got an initial connection"
    try:
        data = clientsock.recv(1024)
        conntype,uuid = data.split(" ")

        # this part will initialize the UUID of a player
        players_lock.acquire()
        uninitialized_player = None
        seen = False
        for player in players:
            if player.uuid == uuid:
                seen = True
            elif player.uuid is None:
                uninitialized_player = player
        if not seen and uninitialized_player:
            uninitialized_player.uuid = uuid
            print "Initialized a player with UUID", uuid
        players_lock.release()

        # now we dispatch based on which socket we're looking at
        if conntype == "SEND":
            skip_release = False
            players_lock.acquire()
            for player in players:
                if player.uuid == uuid:
                    print "found a player with UUID", uuid
                    if player.ctos_queue is None:
                        player.ctos_queue = Queue.Queue()
                        print "Created a CTOS queue for player", player.uuid
                        skip_release = True
                        players_lock.release()
                        handle_ctos_socket(clientsock, addr, player.ctos_queue)
                        break
                    else:
                        # this means this player already has a ctos queue
                        players_lock.release()
                        return
            if not skip_release:
                players_lock.release()
        elif conntype == "RECV":
            skip_release = False
            players_lock.acquire()
            for player in players:
                if player.uuid == uuid:
                    if player.stoc_queue is None:
                        player.stoc_queue = Queue.Queue()
                        print "Created a STOC queue for player", player.uuid
                        skip_release = True
                        players_lock.release()
                        handle_stoc_socket(clientsock, addr, player.stoc_queue)
                        break
                    else:
                        # this means this player already has a stoc queue
                        players_lock.release()
                        return
            if not skip_release:
                players_lock.release()
    except socket.error:
        print "Socket error encountered in dispatch from", addr[0]
        return


def handle_ctos_socket(clientsock, addr, queue):
    print "Handed to client-to-server"
    try:
        while True:
            data = clientsock.recv(1024)
            queue.put(data)
    except socket.error as e:
        print "Socket error encountered in ctos from", addr[0]
        print e.strerror
        return


def handle_stoc_socket(clientsock, addr, queue):
    print "Handed to server-to-client"
    try:
        while True:
            if not queue.empty():
                clientsock.send(queue.get() + "\n")
            else:
                time.sleep(0.1)
    except socket.error as e:
        print "Socket error encountered in stoc from", addr[0]
        print e.strerror
        return


def start_socket_server():
    # make the server socket
    IP = "127.0.0.1"
    PORT = 1111
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this next line lets the socket be reused, which makes testing way better
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((IP, PORT))
    sock.listen(4)
    while True:
        clientsock, addr = sock.accept()
        print "Connection from", addr
        thread.start_new_thread(handle_initial, (clientsock, addr))


def broadcast(message):
    for player in players:
        player.stoc_queue.put(message)


def get_random_sigil():
    return random.choice([futhark.Fehu, heiroglyphs.Bird])


def lookup_sigil(uuid):
    try:
        return sigil_uuid_map[uuid]
    except KeyError:
        return None

# make data structures
players = (Player(), Player())
players_lock = threading.Lock()

sigil_uuid_map = {}

available_sigils = []
available_sigils_lock = threading.Lock()

casting_sigils = []

# kick off the server thread
thread.start_new_thread(start_socket_server, ())

# now we'll go in to the main event loop
print "Waiting for clients to connect"
while True:
    time.sleep(0.5)
    all_in = True
    for player in players:
        if player.ctos_queue is None or player.stoc_queue is None:
            all_in = False
    if all_in:
        broadcast("READY")
        print "Game ready!"
        break

running = True
start_time = time.time()
loop_count = 0
sigils_deployed = 0
while running:
    time.sleep(0.1)

    # process messages from clients
    for player in players:
        if not player.ctos_queue.empty():
            message = player.ctos_queue.get()
            split_message = filter(lambda s: s != "", message.split(" "))
            command = split_message[0]
            if command == "CLAIM":
                print "Saw a claim request"
                requested = lookup_sigil(split_message[1])
                if requested is None:
                    continue
                available_sigils_lock.acquire()
                if requested in available_sigils:
                    broadcast("CLAIMED " + player.uuid + " " + requested.uuid)
                    player.wizard.spellbook.append(requested)
                    requested.owner = player
                    available_sigils.remove(requested)
                # TODO move sigil to a player spellbook structure
                available_sigils_lock.release()
            elif command == "CAST":
                if len(split_message) == 2:
                    # regular cast
                    cast_sigil = lookup_sigil(split_message[1])
                    if cast_sigil:
                        print "Casting", cast_sigil.name
                        cast_sigil.start_time = time.time()
                        casting_sigils.append(cast_sigil)
                elif len(split_message) > 2:
                    # combo cast
                    print "Got a combo cast"
                    selected_sigils = map(lookup_sigil, split_message[1:])
                    print "Split message:", split_message[1:]
                    print "Selected sigils:", selected_sigils
                    if None in selected_sigils:
                        print "Breaking due to sigil lookup failure"
                        continue
                    combo_type = combo.select_combo("".join(sorted(map(str, selected_sigils))))
                    selected_combo = combo_type(selected_sigils)
                    selected_combo.start_time = time.time()
                    selected_combo.owner = player
                    casting_sigils.append(selected_combo)
                    print "Casting", selected_combo.name
    # create new sigils
    if loop_count % 10 == 0:
        current_time = time.time()
        if (current_time - start_time) / 3 >= sigils_deployed:
            print "Deploying a sigil:", (current_time - start_time)
            new_sigil = get_random_sigil()()
            available_sigils_lock.acquire()
            available_sigils.append(new_sigil)
            sigil_uuid_map[new_sigil.uuid] = new_sigil
            available_sigils_lock.release()
            broadcast("NEW " + sigil_serialize(new_sigil))
            sigils_deployed += 1

    # check on sigils that are currently casting
    to_remove = []
    for sigil in casting_sigils:
        if (time.time() - sigil.start_time) >= sigil.cast_time:
            print casting_sigils
            broadcast("COMPLETE " + sigil_serialize(sigil) + " " + sigil.owner.uuid)
            to_remove.append(sigil)
            if sigil in sigil.owner.wizard.spellbook:
                # if it's in the spellbook, this is a single sigil
                sigil.owner.wizard.spellbook.remove(sigil)
                broadcast("REMOVE " + sigil.uuid)
            else:
                # if it's not, then this is a combo and we have to remove individuals
                for sub_sigil in sigil.child_sigils:
                    sub_sigil.owner.wizard.spellbook.remove(sub_sigil)
                    broadcast("REMOVE " + sub_sigil.uuid)
    # we do this to avoid modifying the list we're looping through above
    for sigil in to_remove:
        casting_sigils.remove(sigil)

    loop_count += 1
