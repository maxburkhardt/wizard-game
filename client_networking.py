__author__ = 'maxb'

import socket
import uuid
import thread
import Queue
import time

client_uuid = str(uuid.uuid4())
ctos_connection = None
stoc_connection = None
send_queue = Queue.Queue()
recv_queue = Queue.Queue()


def establish_connection(server, port):
    thread.start_new_thread(establish_ctos_connection, (server, port))
    thread.start_new_thread(establish_stoc_connection, (server, port))


def establish_ctos_connection(server, port):
    ctos_connection = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)
    ctos_connection.connect((server, port))
    ctos_connection.send("SEND " + client_uuid)
    while True:
        if not send_queue.empty():
            ctos_connection.send(send_queue.get() + "|")
        else:
            time.sleep(0.1)


def establish_stoc_connection(server, port):
    stoc_connection = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)
    stoc_connection.connect((server, port))
    stoc_connection.send("RECV " + client_uuid)
    while True:
        data = stoc_connection.recv(1024)
        separated = filter(lambda x: x != "", data.split("|"))
        for message in separated:
            recv_queue.put(message)
