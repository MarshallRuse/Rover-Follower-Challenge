import math

from pose import *
from configuration_settings import *
import math_utils as math_utils


class Supervisor:

    def __init__(self, Leader, Follower, Sim_Recorder):
        configSettings = ConfigurationSettings().settings

        self.Leader = Leader
        self.Follower = Follower
        self.SimRecorder = Sim_Recorder
        self.leaderPosition = [2,2] # initial dummy placeholder
        self.leaderRelativeCompassAngle = 1 # initial dummy placeholder
        self.followerPosition = [1,1] # initial dummy placeholder
        self.followerCompassHeading = 1 # initial dummy placeholder
        # FRF = Follower Reference Frame
        self.FCSLeaderPosition = [3,3] # initial dummy placeholder
        self.time = 0.0 # s
        self.deltaTime = 0.25 # s
        self.tooFarDist = int(configSettings["tooFar"])
        self.tooCloseDist = int(configSettings["tooClose"])
        self.optimalDist = self.tooCloseDist + ((self.tooFarDist - self.tooCloseDist) / 2)
        self.errorPosition = 1 # initial dummy placeholder
        self.errorHeading = 1 # initial dummy placeholder
        self.ep = 0
        self.kp = 10
        self.vMax = 25 # per wheel


    def updateRovers(self):
        # Update the Leader Rover's state info
        self.Leader.setPosition()
        # Update the Follower Rover's state info
        self.Follower.setPosition()
        self.Follower.setCompassHeading()

    def updateFollowerPose(self):
        self.followerPosition = self.Follower.getPosition()
        self.followerCompassHeading = self.Follower.getCompassHeading()
        # Record values
        self.SimRecorder.record_follower_world_cs_x(self.followerPosition[0])
        self.SimRecorder.record_follower_world_cs_z(self.followerPosition[1])
        self.SimRecorder.record_follower_compass_heading(self.followerCompassHeading)


    def updateLeaderPose(self):
        self.leaderPosition = self.Leader.getPosition() # [x, z]
        # Record values
        self.SimRecorder.record_leader_world_cs_x(self.leaderPosition[0])
        self.SimRecorder.record_leader_world_cs_z(self.leaderPosition[1])


    def updateFCSLeaderPose(self):
        # FF = FollowerFrame
        FFRot, FFTrans = math_utils.followerFrameTransformation(self.followerCompassHeading, self.followerPosition)
        self.FCSLeaderPosition = math_utils.leaderInFollowerFrame(FFRot, FFTrans, self.leaderPosition)
        # Record values
        self.SimRecorder.record_leader_follower_cs_x(self.FCSLeaderPosition[0])
        self.SimRecorder.record_leader_follower_cs_z(self.FCSLeaderPosition[1])
        self.SimRecorder.record_follower_FT(FFRot)



    def calculateErrorPose(self):
        # Use the leader in the follower's reference frame
        print("Follower in World CS: [" + str(self.followerPosition[0]) + ", " + str(self.followerPosition[1]) + "]")
        print("Leader in World CS: [" + str(self.leaderPosition[0]) + ", " + str(self.leaderPosition[1]) + "]")
        print("Leader in Follower CS: [" + str(self.FCSLeaderPosition[0]) + ", " + str(self.FCSLeaderPosition[1]) + "]" )
        #self.errorHeading = (math.pi / 2) - math.atan2(self.FRFLeaderPosition[1], self.FRFLeaderPosition[0])
        #self.errorHeading = math.atan2(self.FRFLeaderPosition[1], self.FRFLeaderPosition[0])
        xRelativeError = math.atan2(self.FCSLeaderPosition[1], self.FCSLeaderPosition[0])
        print("xRelative Error Heading: " + str(math.degrees(xRelativeError)))
        self.errorHeading = math_utils.xRelativeToCompass(xRelativeError)
        print("Compass errorHeading is: " + str(math.degrees(self.errorHeading)))

        # Record values
        self.SimRecorder.record_x_relative_error_heading(math.degrees(xRelativeError))
        self.SimRecorder.record_compass_relative_error_heading(math.degrees(self.errorHeading))

    def calculateProportionalVelocity(self):
        pass

    def calculateWheelVelocities(self):
        self.ep = self.errorHeading
        omega = self.kp * self.ep
        print("OMEGA: " + str(omega))
        v = self.vMax / math.sqrt(abs(omega) + 1)
        print("v: " + str(v))

        lVelocity, rVelocity = self.uniToDiff(v, omega)
        print("lVelocity is: " + str(lVelocity))
        print("rVelocity is: " + str(rVelocity))
        print("\n ------------------------------------- \n")

        # Record values
        self.SimRecorder.record_omega(omega)
        self.SimRecorder.record_v(v)
        self.SimRecorder.record_v_max(self.vMax)
        self.SimRecorder.record_left_wheel_velocity(lVelocity)
        self.SimRecorder.record_right_wheel_velocity(rVelocity)

        return lVelocity, rVelocity

    def execute(self):
        # Update the Rovers through communication with simulation
        self.updateRovers()
        # Update the Supervisors info about the Rovers
        self.updateFollowerPose()
        self.updateLeaderPose()
        self.updateFCSLeaderPose()
        # Calculate the error between the Leader and Follower
        self.calculateErrorPose()

        lVelocity, rVelocity = self.calculateWheelVelocities()
        self.Follower.accelerate(lVelocity, rVelocity)



    def uniToDiff(self, v, omega):
        radius = self.Follower.WHEEL_RADIUS
        wheelBase = self.Follower.WHEEL_AXLE_LENGTH
        self.SimRecorder.record_follower_wheel_radius(radius)
        self.SimRecorder.record_follower_axle_length(wheelBase)

        # The +/- were actually inverted from convention, and that
        # seemed to stop the heading error balancing on -180/180
        lVelocity = (2 * v) + (omega * wheelBase) / (2 * radius)
        rVelocity = (2 * v) - (omega * wheelBase) / (2 * radius)

        return lVelocity, rVelocity




