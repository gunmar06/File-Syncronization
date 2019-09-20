import threading
import asyncio
import socket
import select
import sys

class Server():
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 1001
        self.setupSocket()
        loop = asyncio.new_event_loop()

    def setupSocket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.ip, self.port))
            self.socket.listen(5)
            self.server_on = True
        except PermissionError:
            pass
    async def waitConnection(self):
        while self.server_on:
            rlist, _, _ = select.select([self.socket], [], [], 0.05)
            for client in rlist:
                client.accept()

class Client():
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 1001
        self.client_on = False
    def searchServer(self):
        ip_number = 0
        while self.client_on == False:
            separate_ip = self.ip.split(".")
            new_ip = "{}.{}.{}.{}".format(separate_ip[0], separate_ip[1], separate_ip[2], ip_number)
            

            
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