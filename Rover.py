import socket_controller as sc
import commands
import time
import math

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

    # Note to self: Find a better way to do this that doesn't
    # pause program execution
    def setOrientation(self):
        pos1 = self.getPosition()
        time.sleep(0.2)
        self.setPosition()
        pos2 = self.getPosition()
        if pos1[0] != pos2[0] or pos1[1] != pos2[1]: #ie. the rover has moved
            xDiff = pos2[0] - pos1[0]
            zDiff = pos2[1] - pos1[1]
            if xDiff > 0 and zDiff > 0:
                clockwiseFromNorth = math.degrees(math.atan(xDiff / zDiff))
            elif xDiff < 0 and zDiff > 0:
                clockwiseFromNorth = 360 - math.degrees(math.atan(abs(xDiff) / zDiff))
            elif xDiff > 0 and zDiff < 0:
                clockwiseFromNorth = 90 + math.degrees(math.atan(abs(zDiff) / xDiff))
            else:
                clockwiseFromNorth = 270 - math.degrees(math.atan(abs(zDiff) / abs(xDiff)))

            self.orientation = clockwiseFromNorth


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
        self.TOO_CLOSE = int(sc.configSettings["tooClose"])
        self.TOO_FAR = int(sc.configSettings["tooFar"])



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