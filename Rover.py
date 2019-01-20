import socket_controller as sc
import commands

# The Rover class
class Rover:

    def __init__(self, socketConn):

        self.conn = socketConn
        self.speed = 0
        self.orientation = 0
        self.position = [0,0]

    # returns the x, z position of the Rover as floats
    def getPosition(self):
        return self.position

    def getSpeed(self):
        return self.speed

    def getOrientation(self):
        return self.orientation

class Leader(Rover):

    def __init__(self, socketConn):
        super().__init__(socketConn)
        self.position = self.setPosition()
        self.distFromFollower = self.setDistFromFollower()


    def setPosition(self):
        self.conn.sendall(commands.findLeader())
        GPSString = sc.obsSock.recv(1024).decode('utf-8')
        positions = GPSString.split(',')[1:]
        xPos = float(positions[0])
        zPos = float(positions[1][:-2])  # -2 b/c of the newline character
        self.position = [xPos, zPos]

    def setDistFromFollower(self):
        self.conn.sendall(commands.leaderDist())
        distString = self.conn.recv(1024).decode('utf-8')
        dist = distString.split(',')[1][:-2]  # -2 b/c of the newline character
        self.distFromFollower = float(dist)

    def getDistFromFollower(self):
        return self.distFromFollower


class Follower(Rover):

    def __init__(self, socketConn, leader):
        super().__init__(socketConn)
        self.position = self.setPosition()
        self.orientation = self.setOrientation()
        self.distToLeader = self.setDistToLeader(leader)


    def setPosition(self):
        self.conn.sendall(commands.findRover())
        GPSString = self.conn.recv(1024).decode('utf-8')
        positions = GPSString.split(',')[1:]
        xPos = float(positions[0])
        zPos = float(positions[1][:-2])  # -2 b/c of the newline character
        self.position = [xPos, zPos]

    def setOrientation(self):
        self.conn.sendall(commands.roverCompassDir())
        CompassString = self.conn.recv(1024).decode('utf-8')
        compassAngle = CompassString.split(',')
        self.orientation = float(compassAngle[1][:-2])

    def setDistToLeader(self, leader):
        if isinstance(leader, Leader):
            self.distToLeader = leader.getDistFromFollower()


    def getDistToLeader(self):
        return self.distToLeader