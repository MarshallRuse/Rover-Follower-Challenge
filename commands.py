
def moveForward(amount):
    return str.encode("Rover,setForwardPower(" + str(amount) + ")\n")

def accelerate(amount):
    return str.encode("Rover,incrementPower(" + str(amount) + ")\n")

def setLRPower(name, left, right):
    return str.encode(name + ",setLRPower(" + str(left) + "," + str(right) + ")\n")

def stop():
    return str.encode("Rover,setForwardPower(0)\n")

def reverse(amount):
    return str.encode("Rover,setForwardPower(" + str(-1 * amount) + ")\n")

def brake(amount):
    return str.encode("Rover,break(" + str(amount) + ")\n")

def findRover(name):
    return str.encode(name + ",GPS()\n")

def roverCompassDir(name):
    return str.encode(name + ",getCompass()\n")

def findLeader():
    return str.encode("Leader,GPS()\n")

def leaderDist():
    return str.encode("Leader,Distance()\n")

def startLeader():
    return str.encode("ready\n")