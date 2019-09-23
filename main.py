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
            while tmp_buffer[-1][-1] != "\0".encode():
                tmp_buffer.append(client.recv(self.transmission_buffer_size))
            msg = SocketMessage("".encode(), client)
            for chunck in tmp_buffer:
                msg.message += chunck
            self.in_buffer.append(msg)
    def __updateOutputBuffer(self):
        while len(self.out_buffer) > 0:
            if self.__isClientReadeable(self.out_buffer[0].client, self.connections):
                if len(self.out_buffer[0].message) < 1024:
                    self.out_buffer[0].client.send(self.out_buffer[0].message)
                else:
                    sgmt_msg = self.__segmentMessage(self.out_buffer[0].message)
                    for sgmt in sgmt_msg:
                        self.out_buffer[0].client.send(sgmt)
    def __isClientReadeable(self, _client, _cnt_list):
        _, wlist, _ = select.select([], _cnt_list, [], 0.05)
        if _client in wlist:
            return True
        return False
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
        self.client_list = []
        self.server_on = False
        if self.setupSocket():
            self.sck_buff_g = SocketBufferGestionnary([self.client_list])
            self.sck_buff_g.start()
            self.waitConnection()
    def getIp(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except OSError:
            return None
    def setupSocket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.ip, self.port))
            self.server_on = True
            self.socket.listen(5)
            return True
        except PermissionError as e:
            print(e)
        except TypeError:
            pass
    def waitConnection(self):
        while self.server_on:
            rlist, _, _ = select.select([self.socket], [], [], 0.05)
            for client in rlist:
                _clt, _ = client.accept()
                self.client_list.append(_clt)
            sleep(1/60)


class Client():
    def __init__(self):
        self.ip = self.getIp()
        self.port = 1001
        self.client_on = False
        self.searchServer()
        self.sck_buff_g = SocketBufferGestionnary([self.socket])
        self.sck_buff_g.start()
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
        try:
            ip_number = 0
            while self.client_on == False:
                separate_ip = self.ip.split(".")
                new_ip = "{}.{}.{}.{}".format(separate_ip[0], separate_ip[1], separate_ip[2], ip_number)
                try:
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socket.connect((new_ip, self.port))
                    self.ip = new_ip
                    self.client_on = True
                except ConnectionError as e:
                    print("No connection at {}, try next ({})".format(new_ip, e))
                    ip_number = (ip_number + 1) % 256
        except AttributeError:
            pass
            
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