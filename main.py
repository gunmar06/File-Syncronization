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

"""
def segmentMessage(message):
    msg_list = []
    for i in range(len(message) % 50):
        try:
            msg_list.append(message[(i * 50):((i + 1) * 50]))]
        except IndexError as e:
            msg_list.append(message[(i * 50):)]
    return msg_list
"""

class SocketMessage():
    def __init__(self, _message, _client):
        self.message = _message
        self.client = _client

class SocketBufferGestionnary(threading.Thread):
    def __init__(self, _connections):
        super().__init__()
        self.connections = _connections
        self.transmission_buffer_size = 1024
        self.in_buffer = []
        self.out_buffer = []
        self.update_frequency = 1/60
    def run(self):
        self.on = True
        while self.on == True:
            self.__updateInputBuffer()
            self.__updateOutputBuffer()
            sleep(self.update_frequency)
    def __updateInputBuffer(self):
        rlist, _, _ = select.select(self.connections, [], [], 0.05)
        for client in rlist:
            tmp_buffer = []
            while self.in_buffer[-1][-1] != "\0".encode():
                tmp_buffer.append(client.recv(self.transmission_buffer_size))
            self.in_buffer.append("".encode())
            for item in tmp_buffer:
                self.in_buffer[-1] += item

            self.in_buffer.append()
    def __updateOutputBuffer(self):
        while len(self.out_buffer) > 0:
            if len(self.out_buffer[0].message) < 1024:
                self.out_buffer[0].client.send(self.out_buffer[0].message)
            else:
                sgmt_msg = self.__segmentMessage(self.out_buffer[0].message)
                for sgmt in sgmt_msg:
                    self.out_buffer[0].client.send(sgmt)
    def __segmentMessage(self, message):
        msg_list = []
        for i in range((len(message) // self.transmission_buffer_size) + 1):
            try:
                msg_list.append(message[(i * self.transmission_buffer_size):((i + 1) * self.transmission_buffer_size)])
            except IndexError:
                msg_list.append(message[(i * self.transmission_buffer_size):])
        if len(msg_list[-1]) < self.transmission_buffer_size:
            msg_list[-1] += "\0".encode()
        else:
            msg_list.append("\0".encode())
        return msg_list

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
        self.ip = self.getIp()
        self.port = 1001
        self.client_on = False
        self.searchServer()
    def getIp(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except OSError as e:
            print(e)
            return None
        
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
#server = Server()
client = Client()