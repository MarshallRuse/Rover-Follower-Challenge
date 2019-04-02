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

    # Instantiate Leader, Follower Rovers (with their socket connections)
    # Start the simulation by sending 'ready'
    Leader = Rover.Leader(SSI.observationSocket, "Leader")
    Follower = Rover.Follower(SSI.controlSocket, "Rover", Leader)
    Follower2 = Rover.Follower(SSI.controlSocket, "Follower2", Follower)
    Follower3 = Rover.Follower(SSI.controlSocket, "Follower3", Follower2)
    Follower4 = Rover.Follower(SSI.controlSocket, "Follower4", Follower3)

     # Start the Simulation
    confirmationStr = SSI.observationSocket.sendAndReceive(commands.startLeader())  # Receive a confirmation string
    print(confirmationStr)

    SimRecorder = SimulationRecorder()
    #LiveTracker = LiveRoverTracker()
    PostRunAnalysis = PostRunAnalyzer(4)
    supervisor0_1 = Supervisor(Leader, Follower, 0, 1, SimRecorder, PostRunAnalyzer=PostRunAnalysis)
    supervisor1_2 = Supervisor(Follower, Follower2, 1, 2,PostRunAnalyzer=PostRunAnalysis)
    supervisor2_3 = Supervisor(Follower2, Follower3, 2, 3,PostRunAnalyzer=PostRunAnalysis)
    supervisor3_4 = Supervisor(Follower3, Follower4, 3, 4,PostRunAnalyzer=PostRunAnalysis)

    startTime = time.time()
    i = 0
    while time.time() < startTime + 60:
        #print("TIME::: " + str(i) + " secs.")
        SimRecorder.record_time(i)
        supervisor0_1.execute()
        supervisor1_2.execute()
        supervisor2_3.execute()
        supervisor3_4.execute()
        i += global_vars.delta_time
        time.sleep(global_vars.delta_time)
    SimRecorder.writeToCSV()
    SimRecorder.appendGoalPerformanceMeasures()
    PostRunAnalysis.revealAnimatedPlot()

main()







