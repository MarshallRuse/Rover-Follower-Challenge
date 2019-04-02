import math

from pose import *
from configuration_settings import *
import math_utils as math_utils
import global_vars


class Supervisor:

    def __init__(self, Leader, Follower, Sim_Recorder, LiveTracker=None, PostRunAnalyzer=None, testing=False):
        configSettings = ConfigurationSettings().settings

        # Just for the purposes of testing
        self.testing = testing

        # Leader properties
        self.Leader = Leader
        self.leaderPosition = [1, 15]  # based on previous analysis
        self.leaderPrevPosition = [1,15]
        self.leaderHeadingVector = [2,2]
        self.leaderCompassHeadingAngle = 2  # initial dummy placeholder
        self.leaderVelocity = [2,2]
        self.leaderSpeed = 2
            # FCS = Follower Coordinate System
        self.FCSLeaderPosition = [3, 3]  # initial dummy placeholder

        # Follower properties
        self.Follower = Follower
        self.followerPosition = [1, 1]  # initial dummy placeholder
        self.followerPrevPosition = [1,1]
        self.followerHeadingVector = [1,1]
        self.followerCompassHeading = 1  # initial dummy placeholder
        self.followerVelocity = 1
        self.followerSpeed = 1

        # Follower error metrics
        self.errorAngle = 0  # initial dummy placeholder
        self.errorAngleRiemannSum = 0 # for integral error
        self.prevErrorAngle = 0 # for derivative error
        self.errorDistance = 1  # initial dummy placeholder
        self.prevErrorDistance = 0

        # Simulation Recorder properties
        self.SimRecorder = Sim_Recorder

        # Live Tracker properties
        self.LiveTracker = LiveTracker

        # Post Run Analysis properties
        self.PostRunAnalysis = PostRunAnalyzer

        # Simulation Goal properties
        self.tooFarDist = int(configSettings["tooFar"])
        self.tooCloseDist = int(configSettings["tooClose"])
        self.optimalDist = self.tooCloseDist + ((self.tooFarDist - self.tooCloseDist) / 2)

        # Miscellaneous properties
        self.time = 0.0 # s
        self.deltaTime = global_vars.delta_time # s
            # Angular Velocity
        self.kP = 30 # Proportional gain
        self.kI = 0.5 # Integral gain
        self.kD = 0.1 # Derivative gain
            # Linear Velocity
        self.v = 0
        self.vMax = 100 # per wheel
        self.linVelErrDerivCoeff = 3



    def updateRovers(self):
        # Update the Leader Rover's state info
        self.Leader.setPosition()
        self.Leader.setHeadingVector()
        self.Leader.setCompassHeadingAngle()
        self.Leader.setVelocity()
        self.Leader.setSpeed()

        # Update the Follower Rover's state info
        self.Follower.setPosition()
        self.Follower.setHeadingVector()
        self.Follower.setCompassHeadingAngle()
        self.Follower.setVelocity()
        self.Follower.setSpeed()

    def updateFollowerPose(self):
        self.followerPrevPosition = self.Follower.getPrevPostion()
        self.followerPosition = self.Follower.getPosition()
        self.followerHeadingVector = self.Follower.getHeadingVector()
        self.followerCompassHeading = self.Follower.getCompassHeadingAngle()
        self.followerVelocity = self.Follower.getVelocity()
        self.followerSpeed = self.Follower.getSpeed()
        # Record values
        self.SimRecorder.record_follower_world_cs_x(self.followerPosition[0])
        self.SimRecorder.record_follower_world_cs_z(self.followerPosition[1])
        self.SimRecorder.record_follower_compass_heading(self.followerCompassHeading)
        # TODO: Record Heading, Velocity, Speed values


    def updateLeaderPose(self):
        self.leaderPrevPosition = self.Leader.getPrevPostion()
        self.leaderPosition = self.Leader.getPosition() # [x, z]
        self.leaderHeadingVector = self.Leader.getHeadingVector()
        self.leaderCompassHeadingAngle = self.Leader.getCompassHeadingAngle()
        self.leaderVelocity = self.Leader.getVelocity()
        self.leaderSpeed = self.Leader.getSpeed()
        # Record values
        self.SimRecorder.record_leader_world_cs_x(self.leaderPosition[0])
        self.SimRecorder.record_leader_world_cs_z(self.leaderPosition[1])
        # TODO: Record Heading, Velocity, Speed values

    def updateFCSLeaderPose(self):
        # FF = FollowerFrame
        FFRot, FFTrans = math_utils.followerFrameTransformation(self.followerCompassHeading, self.followerPosition)
        self.FCSLeaderPosition = math_utils.leaderInFollowerFrame(FFRot, FFTrans, self.leaderPosition)
        # Record values
        self.SimRecorder.record_leader_follower_cs_x(self.FCSLeaderPosition[0])
        self.SimRecorder.record_leader_follower_cs_z(self.FCSLeaderPosition[1])
        self.SimRecorder.record_follower_FT(FFRot)
        self.PostRunAnalysis.updateFollowerFrameTrans(FFRot)


    def calculateErrorAngle(self):

        # record the old error
        self.prevErrorAngle = self.errorAngle

        # Use the leader in the follower's reference frame
        xRelativeError = math.atan2(self.FCSLeaderPosition[1], self.FCSLeaderPosition[0])
        # atan2 is [+/- pi] relative to positive x-axis. Convert to compass angle.
        self.errorAngle = math_utils.xRelativeToCompass(xRelativeError)

        # add error to Riemann sum of errors (~= to integral of errors)
        self.errorAngleRiemannSum += self.errorAngle # note, multiplication by deltaTime factored into kI below

        # Record values
        self.SimRecorder.record_x_relative_error_heading(math.degrees(xRelativeError))
        self.SimRecorder.record_compass_relative_error_heading(math.degrees(self.errorAngle))

    def calculateErrorDistance(self):
        # Record the previous error distance
        self.prevErrorDistance = self.errorDistance
        leaderFollowerDiff = math_utils.euclideanDist(self.leaderPosition, self.followerPosition)
        self.errorDistance = leaderFollowerDiff - self.optimalDist

        # Record values
        self.SimRecorder.record_linear_distance_error(self.errorDistance)

    def calculateAppropriateLinearVelocity(self):
        logisticFuncMid = 1
        logisticFuncGrowthRate = 10

        errorDeriv = (self.errorDistance - self.prevErrorDistance) / self.deltaTime
        tanh_error = math_utils.tanh(errorDeriv)
        #print("tanh_error: " + str(tanh_error))
        #print("errorDeriv: " + str(errorDeriv))

        self.v = (math_utils.logistic(self.errorDistance, mid=logisticFuncMid,
                                     growthRate=logisticFuncGrowthRate) * self.vMax) + (self.linVelErrDerivCoeff * tanh_error * abs(errorDeriv))

        self.SimRecorder.record_logistic_function_mid(logisticFuncMid)
        self.SimRecorder.record_logistic_function_growth_rate(logisticFuncGrowthRate)

        # Record value
        self.SimRecorder.record_v_without_angle_error(self.v)


    def calculateWheelVelocities(self):
        proportionalError = (self.kP / self.deltaTime) * self.errorAngle
        integralError = (self.kI * self.deltaTime) * self.errorAngleRiemannSum
        derivativeError = (self.kD / self.deltaTime) * (self.errorAngle - self.prevErrorAngle)
        omega = proportionalError + integralError + derivativeError
        #print("OMEGA: " + str(omega))
        v = self.v / math.sqrt(abs(omega) + 1)
        #print("v: " + str(v))

        lVelocity, rVelocity = self.uniToDiff(v, omega)
        #print("lVelocity is: " + str(lVelocity))
        #print("rVelocity is: " + str(rVelocity))
        #print("\n ------------------------------------- \n")

        # Bound the possible velocity values
        if lVelocity < -100:
            lVelocity = -100
        elif lVelocity > 100:
            lVelocity = 100
        if rVelocity < -100:
            rVelocity = -100
        elif rVelocity > 100:
            rVelocity = 100

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
        self.calculateErrorAngle()
        self.calculateErrorDistance()
        self.calculateAppropriateLinearVelocity()

        lVelocity, rVelocity = self.calculateWheelVelocities()

        if self.testing:
            if self.time < 4:
                self.Follower.accelerate(100, -100)
            else:
                self.Follower.accelerate(100,100)
        else:
            self.Follower.accelerate(lVelocity, rVelocity)

        self.time += self.time + self.deltaTime

        # Record constant values
        # For flexibility of analysis, even if unlikely to change
        self.SimRecorder.record_delta_time(self.deltaTime)
        self.SimRecorder.record_proportional_gain(self.kP)
        self.SimRecorder.record_integral_gain(self.kI)
        self.SimRecorder.record_derivative_gain(self.kD)
        self.SimRecorder.record_lin_val_err_deriv_coeff(self.linVelErrDerivCoeff)
        self.SimRecorder.record_max_follower_distance(self.tooFarDist)
        self.SimRecorder.record_min_follower_distance(self.tooCloseDist)
        self.SimRecorder.record_optimal_follower_distance(self.optimalDist)

        # Send Rover coordinates to LiveTracker
        if self.LiveTracker != None:
            self.LiveTracker.updateLeaderCoords(self.leaderPosition[0], self.leaderPosition[1])
            self.LiveTracker.updateFollowerCoords(self.followerPosition[0], self.followerPosition[1])
            if self.LiveTracker.started == False:
                self.LiveTracker.started = True
                self.LiveTracker.start()

        if self.PostRunAnalysis != None:
            self.PostRunAnalysis.updateLeaderCoords(self.leaderPosition[0], self.leaderPosition[1])
            self.PostRunAnalysis.updateFollowerCoords(self.followerPosition[0], self.followerPosition[1])
            self.PostRunAnalysis.updateTime()
            self.PostRunAnalysis.updateGoalDistances()


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




