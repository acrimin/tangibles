import socket, pickle
import sys
import socket
import pickle
import os
import errno
from time import sleep
from threading import Thread

class Internet():
    def __init__(self, **kwargs):
        self.function = kwargs['function']
        # self.ip = kwargs['ip']
        # self.port = kwargs['port']

        self.listener = Thread(target = self.recv)
        self.listener.setDaemon(True)
        self.listener.start()


    def recv(self):
        ip = "127.0.0.1"
        port = 5000
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip, port))
        sock.setblocking(0)
        
        while True:
            try:
                val = sock.recvfrom(4096)
            except socket.error, e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    continue
                else:
                    print e
                    sys.exit(1)
            else:
                data = pickle.loads(val[0])
                print data

                self.function(data)

                

