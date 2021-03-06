import math

import commands
import global_vars
import math_utils as mathUtils
from socket_communication_errors import *


# The Rover class
class Rover:

    def __init__(self, socketConn):

        self.conn = socketConn
        self.WHEEL_RADIUS = 0.5 # m, based off of Curiosity Rover specs
        self.WHEEL_AXLE_LENGTH = 2.8 # m
        self.speed = 0
        self.velocity = [0,0]
        self.headingVector = [1, 1]
        self.compassHeadingAngle = 1
        self.position = [1,1]
        self.prevPosition = [1,1]

    def getPosition(self):
        return self.position

    def getPrevPostion(self):
        return self.prevPosition

    def getVelocity(self):
        return self.velocity

    def getSpeed(self):
        return self.speed

    def getCompassHeadingAngle(self):
        return self.compassHeadingAngle

    def getHeadingVector(self):
        return self.headingVector


class Leader(Rover):

    def __init__(self, socketConn):
        super().__init__(socketConn)

    def setPosition(self):
        self.prevPosition = self.position
        GPSString = self.conn.sendAndReceive(commands.findLeader())
        positions = GPSString.split(',')[1:]
        xPos = float(positions[0])
        zPos = float(positions[1][:-2])  # -2 b/c of the newline character
        self.position = [xPos, zPos]

    # MUST BE CALLED AFTER setPosition for accurate up-to-date results
    def setHeadingVector(self):
        self.compassHeadingVector = mathUtils.differenceVec(self.position[0], self.position[1],
                                                            self.prevPosition[0], self.prevPosition[1])

    # MUST BE CALLED AFTER setCompassHeadingVector for accurate up-to-date results
    def setCompassHeadingAngle(self):
        self.compassHeadingAngle = mathUtils.xRelativeToCompass(math.atan2(self.headingVector[1],
                                                                           self.headingVector[0]))

    def setVelocity(self):
        timeInterval = global_vars.delta_time
        pos1 = self.prevPosition
        pos2 = self.position
        xSpeed = (pos2[0] - pos1[0]) / timeInterval
        zSpeed = (pos2[1] - pos1[1]) / timeInterval
        return [xSpeed, zSpeed]

    def setSpeed(self):
        vel = self.velocity
        return math.sqrt(math.pow(vel[0], 2) + math.pow(vel[1], 2))


class Follower(Rover):


    def __init__(self, socketConn, leader):
        super().__init__(socketConn)
        ### Self Observing Attributes ###
        self.Leader = leader

    #### Self Observing Methods ####
    def setPosition(self):
        self.prevPosition = self.position
        GPSString = self.conn.sendAndReceive(commands.findRover())
        try:
            if len(GPSString) > 0:
                positions = GPSString.split(',')[1:]
                xPos = float(positions[0])
                zPos = float(positions[1][:-2])  # -2 b/c of the newline character
                self.position = [xPos, zPos]
            else:
                raise RoverCoordinatesReturnError('Follower GPS Coordinates not returned by socket')
        except RoverCoordinatesReturnError as e:
            print(e)

    # MUST BE CALLED AFTER setPosition for accurate up-to-date results
    def setHeadingVector(self):
        self.compassHeadingVector = mathUtils.differenceVec(self.position[0], self.position[1],
                                                            self.prevPosition[0], self.prevPosition[1])

    def setCompassHeadingAngle(self):
        try:
            CompassString = self.conn.sendAndReceive(commands.roverCompassDir())
            if len(CompassString) > 0:
                compassAngle = CompassString.split(',')
                self.compassHeadingAngle = float(compassAngle[1][:-2])
            else:
                raise RoverCompassReturnError('Follower Compass Angle not returned by socket')
        except RoverCompassReturnError as e:
            print(e)

    def setVelocity(self):
        timeInterval = global_vars.delta_time
        pos1 = self.prevPosition
        pos2 = self.position
        xSpeed = (pos2[0] - pos1[0]) / timeInterval
        zSpeed = (pos2[1] - pos1[1]) / timeInterval
        return [xSpeed, zSpeed]

    def setSpeed(self):
        vel = self.velocity
        return math.sqrt(math.pow(vel[0], 2) + math.pow(vel[1], 2))

    #### Self Actuating Methods ####
    def accelerate(self, leftWheel, rightWheel):
        leftWheel = round(leftWheel)
        rightWheel = round(rightWheel)
        self.conn.sendOnly(commands.setLRPower(leftWheel, rightWheel))