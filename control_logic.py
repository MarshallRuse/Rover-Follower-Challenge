import socket_controller as sc
import Rover
import commands
import time

# Establish socket connections to the Rovers
# Instantiate Leader, Follower Rovers (with their socket connections)
# Start the simulation by sending 'ready'
def startSimulation():
    sc.connectObserverSock() # connect the control socket
    sc.connectControlSock() # connect the observation socket

    # Leader must be instantiated first, initialization of follower depends on it
    # A follower must have someone to follow
    Leader = Rover.Leader(sc.obsSock)
    Follower = Rover.Follower(sc.controlSock, Leader)
    sc.obsSock.sendall(commands.startLeader())
    confirmationStr = sc.obsSock.recv(1024).decode('utf-8') # receive confirmation string
    print(confirmationStr)



startSimulation()






