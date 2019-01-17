import socket_controller as sc
import commands
import time

# Start the simulation by sending 'ready'
def startSimulation():
    sc.connectObserverSock() # connect the control socket
    sc.connectControlSock() # connect the observation socket

    sc.obsSock.sendall(commands.startLeader())
    confirmationStr = sc.obsSock.recv(1024).decode('utf-8') # receive confirmation string
    print(confirmationStr)


# getLeaderDist returns the distance to the leading rover as a float
def getLeaderDist(printResponse=False):
    sc.obsSock.sendall(commands.leaderDist())
    distString = sc.obsSock.recv(1024).decode('utf-8')
    if printResponse:
        print(distString)
    dist = distString.split(',')[1][:-2] # -2 b/c of the newline character
    return float(dist)

# getLeaderGPS returns the x, z position of the leader as floats
def getLeaderGPS(printResponse=False):
    sc.obsSock.sendall(commands.findLeader())
    GPSString = sc.obsSock.recv(1024).decode('utf-8')
    if printResponse:
        print(GPSString)
    positions = GPSString.split(',')[1:]
    xPos = float(positions[0])
    zPos = float(positions[1][:-2]) # -2 b/c of the newline character
    return xPos, zPos

# getRoverGPS returns the x, z position of the follower as floats
def getRoverGPS(printResponse=False):
    sc.controlSock.sendall(commands.findRover())
    GPSString = sc.controlSock.recv(1024).decode('utf-8')
    if printResponse:
        print(GPSString)
    positions = GPSString.split(',')[1:]
    xPos = float(positions[0])
    zPos = float(positions[1][:-2])  # -2 b/c of the newline character
    return xPos, zPos

def getFollowerCompass(printResponse=False):
    sc.controlSock.sendall(commands.roverCompassDir())
    CompassString = sc.controlSock.recv(1024).decode('utf-8')
    if printResponse:
        print(CompassString)
    compassAngle = CompassString.split(',')
    return float(compassAngle[1][:-2])


startSimulation()
while True:
    print("Leader GPS: ")
    ca = getFollowerCompass(True)
    print(type(ca))
    print("CA: " + str(ca))
    time.sleep(5)


