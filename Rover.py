import time
import math

import commands


# The Rover class
class Rover:

    def __init__(self, socketConn):

        self.conn = socketConn
        self.WHEEL_RADIUS = 0.5 # m, based off of Curiosity Rover specs
        self.WHEEL_AXLE_LENGTH = 2.8 # m
        self.speed = 0
        self.velocity = [0,0]
        self.orientation = 0
        self.position = [0,0]

    #TODO: Some of these get overwritten in subclasses, lookup
    # Python interfaces
    # returns the x, z position of the Rover as floats
    def getPosition(self):
        return self.position

    def getSpeed(self):
        return self.speed

    def getVelocity(self):
        return self.velocity

    def getOrientation(self):
        return self.orientation


class Leader(Rover):

    def __init__(self, socketConn):
        super().__init__(socketConn)
        self.position = self.setPosition()


    def setPosition(self):
        GPSString = self.conn.sendAndReceive(commands.findLeader())
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

    def setVelocity(self):
        timeInterval = 0.2
        pos1 = self.getPosition()
        time.sleep(timeInterval)
        pos2 = self.getPosition()
        xSpeed = (pos2[0] - pos1[0]) / timeInterval
        zSpeed = (pos2[1] - pos1[1]) / timeInterval
        self.velocity = [xSpeed, zSpeed]

    def setSpeed(self):
        self.setVelocity()
        self.speed = math.sqrt(math.pow(self.velocity[0], 2) + math.pow(self.velocity[1], 2))


    def getPosition(self):
        self.setPosition()
        return self.position

    def getVelocity(self):
        self.setVelocity()
        return self.velocity

    def getSpeed(self):
        self.setSpeed()
        return self.speed



class Follower(Rover):


    def __init__(self, socketConn, leader):
        super().__init__(socketConn)
        ### Self Observing Attributes ###
        self.Leader = leader
        self.position = self.setPosition()
        self.orientation = self.setOrientation()


    #### Self Observing Methods ####
    def setPosition(self):
        GPSString = self.conn.sendAndReceive(commands.findRover())
        positions = GPSString.split(',')[1:]
        xPos = float(positions[0])
        zPos = float(positions[1][:-2])  # -2 b/c of the newline character
        self.position = [xPos, zPos]

    def setOrientation(self):
        CompassString = self.conn.sendAndReceive(commands.roverCompassDir())
        compassAngle = CompassString.split(',')
        self.orientation = float(compassAngle[1][:-2])


    #### Self Actuating Methods ####
    def accelerate(self):
        pass