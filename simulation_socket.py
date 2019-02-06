import socket

class SimulationSocket():

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = self.connectSocket()

    def connectSocket(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((self.host,self.port ))
        return connection

    def sendAndReceive(self, message):
        response = ""
        self.connection.sendall(message)
        response = self.connection.recv(1024).decode('utf-8')
        return response

    def sendOnly(self, message):
        self.connection.sendall(message)
