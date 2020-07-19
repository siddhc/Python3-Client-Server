#!/usr/bin/env python3

import socket
import time
import threading
import pickle

HOST_CLIENT = '127.0.0.1'  # The server's hostname or IP address
PORT_CLIENT = 51232        # The port used by the server


def network_receive(socket_object, size=1024):
    try:
        data = pickle.loads(socket_object.recv(size))
    except EOFError as e:
        print("EOFError. Program will continue.")
        return b''
    return data


def network_send(socket_object, message_object):
    socket_object.sendall(pickle.dumps(message_object))


def receiving_threaded(s):
    '''
    Receives messages from the server, anytime.
    :param s: Socket object that connects to the server.
    :return: None
    '''
    with s:
        while True:
            data = network_receive(s)
            print('Received <', data, '> from server @ ', str(time.time()))
            if not data:
                break


def main():
    '''
    Connects to server and sends "Hello, world" every 5 seconds.
    Receiving is handled by a separate thread (receiving_thread)
    :return: None
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST_CLIENT, PORT_CLIENT))
        k = 0  # Non-mandatory counter to track of number of times messages are sent.
        t1 = time.time()
        t = threading.Thread(target=receiving_threaded, args=(s,))
        t.start()
        time.sleep(5)  # Non-mandatory delay before client begins to send messages
        while True:
            t2 = time.time()
            if t2 - t1 > 5:  # Send messages in an interval of 5 seconds
                k = k + 1
                print(f'k = {k}: ', end="")
                t1 = t2
                message_string = "Act now"
                print("Sending <", message_string, "> to server <", str(HOST_CLIENT)+'_'+str(PORT_CLIENT), "> @ ", str(time.time()))
                network_send(s, message_string)
        t.join()


if __name__ == "__main__":
    main()
