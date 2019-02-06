import math
import time

from simulation_socket_interface import *
import Rover
import commands


# Instantiate Leader, Follower Rovers (with their socket connections)
# Start the simulation by sending 'ready'
def startSimulation(SSI):

    # Leader must be instantiated first, initialization of follower depends on it
    # A follower must have someone to follow
    Leader = Rover.Leader(SSI.observationSocket)
    Follower = Rover.Follower(SSI.controlSocket, Leader)
    confirmationStr = SSI.observationSocket.sendAndReceive(commands.startLeader()) # Receive a confirmation string
    print(confirmationStr)

    return Leader, Follower


def main():
    SSI = SimulationSocketInterface()
    Leader, Follower = startSimulation(SSI)








