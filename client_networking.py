__author__ = 'maxb'

import socket
import uuid
import thread
import Queue
import time

client_uuid = uuid.uuid4()
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
    ctos_connection.send("SEND " + str(client_uuid))
    while True:
        if not send_queue.empty():
            ctos_connection.send(send_queue.get())
        else:
            time.sleep(0.1)


def establish_stoc_connection(server, port):
    stoc_connection = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)
    stoc_connection.connect((server, port))
    stoc_connection.send("RECV " + str(client_uuid))
    while True:
        data = stoc_connection.recv(1024)
        recv_queue.put(data)