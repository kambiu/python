"""for all lanuage client """

import socket

# recevice buffer?

def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.bind((host,port))

    s.listen(1) #number of listen
    c, addr = s.accept()
    print( "Connection from: " + str(addr))
    while True:
        data = c.recv(1024)
        if not data:
            break
        data = data.decode("utf-8")
        print( "from connected user: " + str(data))
        data = data.upper().encode("utf-8")
        print( "sending: " + str(data))
        c.send(data)
    c.close()

if __name__ == '__main__':
    Main()

