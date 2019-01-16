import socket_controller as sc
import commands
import time


def startSimulation():
    sc.connectObserverSock()
    sc.connectControlSock()

    sc.obsSock.sendall(commands.startLeader())
    sc.obsSock.sendall(commands.leaderDist())
    #sc.controlSock.send(commands.moveForward(50))
    sc.controlSock.send(commands.left(100,100))

def getLeaderDist():
    sc.obsSock.send(commands.leaderDist())
    distString = sc.obsSock.recv(1024).decode('utf-8')
    print(distString)
    print("LEADER DISTANCE! " + distString)


startSimulation()
#getLeaderDist()

