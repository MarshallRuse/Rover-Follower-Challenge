import socket
import time

class SimulationSocket:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = self.connectSocket()
        self.prevUseTime = time.time()
        self.dt = 0.01 # seconds

    def connectSocket(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((self.host,self.port ))
        return connection

    def sendAndReceive(self, message):
        if time.time() < self.prevUseTime + self.dt:
            time.sleep(self.dt)
        response = ""
        self.connection.sendall(message)
        response = self.connection.recv(1024).decode('utf-8')
        self.prevUseTime = time.time()
        return response

    def sendOnly(self, message):
        if time.time() < self.prevUseTime + self.dt:
            time.sleep(self.dt)
        self.connection.sendall(message)
        self.prevUseTime = time.time()
