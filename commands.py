
def moveForward(amount):
    return str.encode("Rover,setForwardPower(" + str(amount) + ")")

def accelerate(amount):
    return str.encode("Rover,incrementPower(" + str(amount) + ")")

def left(lWheels, rWheels):
    return str.encode("Rover,setLRPower(" + str((-1 * lWheels)) + "," + str(abs(rWheels)) + ")")

def right(lWheels, rWheels):
    return str.encode("Rover,setLRPower(" + str(abs(lWheels)) + "," + str((-1 * rWheels)) + ")")

def stop():
    return str.encode("Rover,setForwardPower(0)")

def reverse(amount):
    return str.encode("Rover,setForwardPower(" + str(-1 * amount) + ")")

def brake(amount):
    return str.encode("Rover,break(" + str(amount) + ")")

def findRover():
    return str.encode("Rover,GPS()")

def roverCompassDir():
    return str.encode("Rover,getCompass()")

def findLeader():
    return str.encode("Leader,GPS()")

def leaderDist():
    return str.encode("Leader,Distance()")

def startLeader():
    return str.encode("ready")