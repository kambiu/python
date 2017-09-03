"""python client """

import socket

def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.connect((host, port))

    message = input("-> ").encode("utf-8")
    while message != 'q':
        s.send(message)
        data = s.recv(1024)
        print ('Received from server: ' + str(data.decode("utf-8")))
        message = input("-> ").encode("utf-8")
    s.close()

if __name__ == '__main__':
    Main()