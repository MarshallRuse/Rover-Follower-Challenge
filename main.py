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


def main():
    SSI = SimulationSocketInterface()

    # Leader must be instantiated first, initialization of follower depends on it
    # A follower must have someone to follow
    Leader = Rover.Leader(SSI.observationSocket)
    Follower = Rover.Follower(SSI.controlSocket, Leader)
    confirmationStr = SSI.observationSocket.sendAndReceive(commands.startLeader())  # Receive a confirmation string
    print(confirmationStr)

    SimRecorder = SimulationRecorder()
    #LiveTracker = LiveRoverTracker()
    PostRunAnalysis = PostRunAnalyzer()
    supervisor = Supervisor(Leader, Follower, SimRecorder, PostRunAnalyzer=PostRunAnalysis)

    startTime = time.time()
    i = 0
    while time.time() < startTime + 60:
        SimRecorder.record_time(i)
        supervisor.execute()
        i += global_vars.delta_time
        time.sleep(global_vars.delta_time)
    SimRecorder.writeToCSV()
    SimRecorder.appendGoalPerformanceMeasures()
    PostRunAnalysis.revealAnimatedPlot()

main()







