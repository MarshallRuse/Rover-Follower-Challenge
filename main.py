import math
import time


from simulation_socket_interface import *
from Supervisor import *
from analysis.simulation_recorder import *
from analysis.live_rover_tracking import *
from analysis.post_run_analysis import *
import Rover
import commands
import global_vars


# Instantiate Leader, Follower Rovers (with their socket connections)
# Start the simulation by sending 'ready'
def startSimulation(SSI):

    # Leader must be instantiated first, initialization of follower depends on it
    # A follower must have someone to follow
    Leader = Rover.Leader(SSI.observationSocket)
    Follower = Rover.Follower(SSI.controlSocket, Leader)
    print("Gets here")
    confirmationStr = SSI.observationSocket.sendAndReceive(commands.startLeader()) # Receive a confirmation string
    print("Also gets here")
    print(confirmationStr)

    return Leader, Follower


def main():
    SSI = SimulationSocketInterface()
    Leader, Follower = startSimulation(SSI)
    SimRecorder = SimulationRecorder()
    #LiveTracker = LiveRoverTracker()
    PostRunAnalysis = PostRunAnalyzer()

    supervisor = Supervisor(Leader, Follower, SimRecorder, PostRunAnalyzer=PostRunAnalysis)

    startTime = time.time()
    i = 0
    while time.time() < startTime + 60:
        #print("TIME::: " + str(i) + " secs.")
        SimRecorder.record_time(i)
        supervisor.execute()
        i += global_vars.delta_time
        time.sleep(global_vars.delta_time)
    SimRecorder.writeToCSV()
    SimRecorder.appendGoalPerformanceMeasures()
    PostRunAnalysis.revealAnimatedPlot()

main()







