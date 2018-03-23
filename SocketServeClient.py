import socket
import threading
import sys
from datetime import datetime

class startSock:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    user_names = {}

    def __init__(self):

        addr_name = socket.gethostname()
        addr = socket.gethostbyname(addr_name)

        print(addr)

        add = (addr, 10000)

        self.sock.bind(add)
        self.sock.listen(1)

        
    def handler(self, c, a):

        c.send(bytes("\nYou have connected! Welcome!\nAdminBot >> Pick a username: ", 'utf-8'))
        data = c.recv(4096)
        self.user_names[str(a[0])] = str(data, 'utf-8')
        c.send(bytes("\nAdminBot >> Welcome " + self.user_names[str(a[0])] + "\n", 'utf-8'))
        
        for connection in self.connections:
            if(connection != c):
                connection.send(bytes("\n" + a[0] + "'" + self.user_names[str(a[0])] + "'" + " has connected!\n", "utf-8"))

        while True:
            data = c.recv(1024)
            for connection in self.connections:
                if(connection != c):
                    connection.send(bytes(datetime.now().strftime('%Y-%m-%d %H:%M') + " | " +
                                          self.user_names[str(a[0])] + " >> " + str(data, 'utf-8'), 'utf-8'))
            if not data:
                self.connections.remove(c)
                c.close()
                for connection in self.connections:
                    connection.send(bytes("\n" + self.user_names[str(a[0])] + " has disconnected!\n>", 'utf-8'))
                break


    def run(self):

        while True:
            c, a = self.sock.accept()
            conn_thread = threading.Thread(target = self.handler, args = (c, a))
            conn_thread.daemon = True
            conn_thread.start()
            self.connections.append(c)
            print(self.connections)


    def pause(self):
        
        for connection in self.connections:
            connection.send(bytes("<><><><><><><><><><><><>", 'utf-8'))


class startClient:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendMsg(self):
        while True:
            self.sock.send(bytes(input(""), "utf-8"))

    
    def __init__(self, address):
        
        self.sock.connect((address, 10000))
        iThread = threading.Thread(target = self.sendMsg)
        iThread.daemon - True
        iThread.start()

        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data, 'utf-8'))


if (len(sys.argv) > 1):
    client = startClient(sys.argv[1])
else:
    server = startSock()
    server.run()
