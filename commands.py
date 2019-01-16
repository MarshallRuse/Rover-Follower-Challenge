
def moveForward(amount):
    return str.encode("Rover,setForwardPower(" + str(amount) + ")\n")

def accelerate(amount):
    return str.encode("Rover,incrementPower(" + str(amount) + ")\n")

def left(lWheels, rWheels):
    return str.encode("Rover,setLRPower(" + str((-1 * lWheels)) + "," + str(abs(rWheels)) + ")\n")

def right(lWheels, rWheels):
    return str.encode("Rover,setLRPower(" + str(abs(lWheels)) + "," + str((-1 * rWheels)) + ")\n")

def stop():
    return str.encode("Rover,setForwardPower(0)\n")

def reverse(amount):
    return str.encode("Rover,setForwardPower(" + str(-1 * amount) + ")\n")

def brake(amount):
    return str.encode("Rover,break(" + str(amount) + ")\n")

def findRover():
    return str.encode("Rover,GPS()\n")

def roverCompassDir():
    return str.encode("Rover,getCompass()\n")

def findLeader():
    return str.encode("Leader,GPS()\n")

def leaderDist():
    return str.encode("Leader,Distance()\n")

def startLeader():
    return str.encode("ready\n")