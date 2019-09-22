from time import sleep
import threading
import socket
import select
import sys

"""
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
s.close()
"""

class Server():
    def __init__(self):
        self.ip = self.getIp()
        self.port = 10011
        self.client_list = {}
        self.server_on = False
        self.setupSocket()
        self.waitConnection()
    def getIp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    def setupSocket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.ip, self.port))
            self.server_on = True
            self.socket.listen(5)
        except PermissionError as e:
            print(e)
    def waitConnection(self):
        while self.server_on:
            rlist, _, _ = select.select([self.socket], [], [], 0.05)
            for client in rlist:
                client.accept()

class Client():
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 1001
        self.client_on = False
        self.searchServer()
    def searchServer(self):
        ip_number = 0
        while self.client_on == False:
            separate_ip = self.ip.split(".")
            new_ip = "{}.{}.{}.{}".format(separate_ip[0], separate_ip[1], separate_ip[2], ip_number)
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((new_ip, self.port))
                self.ip = new_ip
            except ConnectionError as e:
                print("No connection at {}, try next ({})".format(new_ip, e))
                ip_number = (ip_number + 1) % 256
            

            
"""
if __name__ == "__main__":
    if len(sys.argv) > 0:
        if sys.argv[1] == "server":
            server = Server()
    else:
        print("To start server write \"python3 main.py server\"")
        client = Client()
"""
server = Server()
#client = Client()