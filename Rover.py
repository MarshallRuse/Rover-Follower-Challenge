import time
import math

import commands
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
        self.compassHeading = 1
        self.position = [1,1]

    #TODO: Tie the updating of these values
    # to a state update interval
    '''
    def getPosition(self):
        return self.position

    def getSpeed(self):
        return self.speed

    def getVelocity(self):
        return self.velocity

    def getCompassHeading(self):
        return self.compassHeading
    '''

class Leader(Rover):

    def __init__(self, socketConn):
        super().__init__(socketConn)


    def setPosition(self):
        GPSString = self.conn.sendAndReceive(commands.findLeader())
        positions = GPSString.split(',')[1:]
        xPos = float(positions[0])
        zPos = float(positions[1][:-2])  # -2 b/c of the newline character
        self.position = [xPos, zPos]


    def setVelocity(self):
        timeInterval = 0.2
        pos1 = self.getPosition()
        time.sleep(timeInterval)
        pos2 = self.getPosition()
        xSpeed = (pos2[0] - pos1[0]) / timeInterval
        zSpeed = (pos2[1] - pos1[1]) / timeInterval
        return [xSpeed, zSpeed]

    def setSpeed(self):
        vel = self.getVelocity()
        return math.sqrt(math.pow(vel[0], 2) + math.pow(vel[1], 2))


    def getPosition(self):
        return self.position


    def getVelocity(self):
        return self.velocity

    def getSpeed(self):
        return self.speed



class Follower(Rover):


    def __init__(self, socketConn, leader):
        super().__init__(socketConn)
        ### Self Observing Attributes ###
        self.Leader = leader

    #### Self Observing Methods ####
    def setPosition(self):
        GPSString = self.conn.sendAndReceive(commands.findRover())
        try:
            if len(GPSString) > 0:
                print("Follower GPS:  " + GPSString)
                positions = GPSString.split(',')[1:]
                xPos = float(positions[0])
                zPos = float(positions[1][:-2])  # -2 b/c of the newline character
                self.position = [xPos, zPos]
            else:
                raise RoverCoordinatesReturnError('Follower GPS Coordinates not returned by socket')
        except RoverCoordinatesReturnError as e:
            print(e)

    def setCompassHeading(self):
        try:
            CompassString = self.conn.sendAndReceive(commands.roverCompassDir())
            if len(CompassString) > 0:
                print("Follower Compass: " + CompassString)
                compassAngle = CompassString.split(',')
                self.compassHeading = float(compassAngle[1][:-2])
            else:
                raise RoverCompassReturnError('Follower Compass Angle not returned by socket')
        except RoverCompassReturnError as e:
            print(e)


    def getCompassHeading(self):
        return self.compassHeading


    def getPosition(self):
        return self.position

    #### Self Actuating Methods ####
    def accelerate(self, leftWheel, rightWheel):
        leftWheel = round(leftWheel)
        rightWheel = round(rightWheel)
        self.conn.sendOnly(commands.setLRPower(leftWheel, rightWheel))