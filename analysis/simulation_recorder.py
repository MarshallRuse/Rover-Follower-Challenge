import os
import csv

from analysis.goal_performance_analyzer import *

class SimulationRecorder:

    def __init__(self):
        self.recordsDirectory = os.path.join(os.getcwd(), "analysis", "records")
        self.goalPerformanceRecordsDirectory = os.path.join(os.getcwd(), "analysis","goal_performance_records")
        # version number subject to change based on fields recorded
        self.recordVersionNum = 3

        # determine what to call the output file based on existing files
        dirContents = os.listdir(self.recordsDirectory)
        print("dirContents: " + str(dirContents))
        if len(os.listdir(os.path.join(os.getcwd(), "analysis", "records"))) > 0:
            recordNums = []
            for file in dirContents:
                # assumes file name format "simulation-record--v#-1"
                # first split on "." for .csv
                recordNum = file.split(".")[0].split("-")[-1]
                recordNums.append(int(recordNum))
            mostRecentNum = sorted(recordNums)[-1]

            self.thisRecordNum = mostRecentNum + 1
        else:
            self.thisRecordNum = 1

        self.fileName = "simulation-record-"+ str(self.recordVersionNum) + "-" + str(self.thisRecordNum) + ".csv"

        # column headers
        self.columns = ["time",
                        "delta_time",
                        "follower_world_cs_x",
                        "follower_world_cs_z",
                        "follower_compass_heading",
                        "leader_world_cs_x",
                        "leader_world_cs_z",
                        "leader_follower_cs_x",
                        "leader_follower_cs_z",
                        "follower_FT_R11",
                        "follower_FT_R21",
                        "follower_FT_R12",
                        "follower_FT_R22",
                        "x_relative_error_heading",
                        "compass_relative_error_heading",
                        "linear_distance_error",
                        "omega",
                        "v",
                        "v_without_angle_error",
                        "v_max",
                        "left_wheel_velocity",
                        "right_wheel_velocity",
                        "follower_wheel_radius",
                        "follower_axle_length",
                        "proportional_gain",
                        "integral_gain",
                        "derivative_gain",
                        "logistic_function_mid",
                        "logistic_function_growth_rate",
                        "max_follower_distance",
                        "min_follower_distance",
                        "optimal_follower_distance"]

        # column value lists
        self.time = []
        self.delta_time = []
        self.follower_world_cs_x = []
        self.follower_world_cs_z = []
        self.follower_compass_heading = []
        self.leader_world_cs_x = []
        self.leader_world_cs_z = []
        self.leader_follower_cs_x = []
        self.leader_follower_cs_z = []
        self.follower_FT_R11 = []
        self.follower_FT_R21 = []
        self.follower_FT_R12 = []
        self.follower_FT_R22 = []
        self.x_relative_error_heading = []
        self.compass_relative_error_heading = []
        self.linear_distance_error = []
        self.omega = []
        self.v = []
        self.v_without_angle_error = []
        self.v_max = []
        self.left_wheel_velocity = []
        self.right_wheel_velocity = []
        self.follower_wheel_radius = []
        self.follower_axle_length = []
        self.proportional_gain = []
        self.integral_gain = []
        self.derivative_gain = []
        self.logistic_function_mid = []
        self.logistic_function_growth_rate = []
        self.max_follower_distance = []
        self.min_follower_distance = []
        self.optimal_follower_distance = []
        self.too_close_percentage = 0
        self.too_far_percentage = 0
        self.goal_distance_percentage = 0

        self.GPA = None # to be assigned once above values collected

    # functions for recording column values
    def record_time(self, val):
        self.time.append(val)
        
    def record_delta_time(self, val):
        self.delta_time.append(val)

    def record_follower_world_cs_x(self, val):
        self.follower_world_cs_x.append(val)

    def record_follower_world_cs_z(self, val):
        self.follower_world_cs_z.append(val)

    def record_follower_compass_heading(self, val):
        self.follower_compass_heading.append(val)

    def record_leader_world_cs_x(self, val):
        self.leader_world_cs_x.append(val)

    def record_leader_world_cs_z(self, val):
        self.leader_world_cs_z.append(val)

    def record_leader_follower_cs_x(self, val):
        self.leader_follower_cs_x.append(val)

    def record_leader_follower_cs_z(self, val):
        self.leader_follower_cs_z.append(val)

    def record_follower_FT(self, val):
        # val expected to be a 2x2 rotation matrix
        self.follower_FT_R11.append(val[0][0])
        self.follower_FT_R21.append(val[1][0])
        self.follower_FT_R12.append(val[0][1])
        self.follower_FT_R22.append(val[1][1])

    def record_x_relative_error_heading(self, val):
        self.x_relative_error_heading.append(val)

    def record_compass_relative_error_heading(self, val):
        self.compass_relative_error_heading.append(val)

    def record_linear_distance_error(self, val):
        self.linear_distance_error.append(val)

    def record_omega(self, val):
        self.omega.append(val)

    def record_v(self, val):
        self.v.append(val)

    def record_v_without_angle_error(self, val):
        self.v_without_angle_error.append(val)

    def record_v_max(self, val):
        self.v_max.append(val)

    def record_left_wheel_velocity(self, val):
        self.left_wheel_velocity.append(val)

    def record_right_wheel_velocity(self, val):
        self.right_wheel_velocity.append(val)

    def record_follower_wheel_radius(self, val):
        self.follower_wheel_radius.append(val)

    def record_follower_axle_length(self, val):
        self.follower_axle_length.append(val)

    def record_proportional_gain(self, val):
        self.proportional_gain.append(val)
        
    def record_integral_gain(self, val):
        self.integral_gain.append(val)
        
    def record_derivative_gain(self, val):
        self.derivative_gain.append(val)

    def record_logistic_function_mid(self, val):
        self.logistic_function_mid.append(val)

    def record_logistic_function_growth_rate(self, val):
        self.logistic_function_growth_rate.append(val)

    def record_max_follower_distance(self, val):
        self.max_follower_distance.append(val)

    def record_min_follower_distance(self, val):
        self.min_follower_distance.append(val)

    def record_optimal_follower_distance(self, val):
        self.optimal_follower_distance.append(val)


    def writeToCSV(self):
        fullPath = os.path.join(self.recordsDirectory, self.fileName)
        with open(fullPath, 'w', newline='') as f:
            csvWriter = csv.DictWriter(f, fieldnames=self.columns)

            csvWriter.writeheader()
            for i in range(0, len(self.time)):
                csvWriter.writerow({
                    "time" : self.time[i],
                    "delta_time" : self.delta_time[i],
                    "follower_world_cs_x" : self.follower_world_cs_x[i],
                    "follower_world_cs_z" : self.follower_world_cs_z[i],
                    "follower_compass_heading" : self.follower_compass_heading[i],
                    "leader_world_cs_x" : self.leader_world_cs_x[i],
                    "leader_world_cs_z" : self.leader_world_cs_z[i],
                    "leader_follower_cs_x" : self.leader_follower_cs_x[i],
                    "leader_follower_cs_z" : self.leader_follower_cs_z[i],
                    "follower_FT_R11" : self.follower_FT_R11[i],
                    "follower_FT_R21" : self.follower_FT_R21[i],
                    "follower_FT_R12" : self.follower_FT_R12[i],
                    "follower_FT_R22" : self.follower_FT_R22[i],
                    "x_relative_error_heading" : self.x_relative_error_heading[i],
                    "compass_relative_error_heading" : self.compass_relative_error_heading[i],
                    "linear_distance_error" : self.linear_distance_error[i],
                    "omega": self.omega[i],
                    "v" : self.v[i],
                    "v_without_angle_error" : self.v_without_angle_error[i],
                    "v_max" : self.v_max[i],
                    "left_wheel_velocity" : self.left_wheel_velocity[i],
                    "right_wheel_velocity" : self.right_wheel_velocity[i],
                    "follower_wheel_radius" : self.follower_wheel_radius[i],
                    "follower_axle_length" : self.follower_axle_length[i],
                    "proportional_gain" : self.proportional_gain[i],
                    "integral_gain": self.integral_gain[i],
                    "derivative_gain": self.derivative_gain[i],
                    "logistic_function_mid": self.logistic_function_mid[i],
                    "logistic_function_growth_rate": self.logistic_function_growth_rate[i],
                    "max_follower_distance": self.max_follower_distance[i],
                    "min_follower_distance": self.min_follower_distance[i],
                    "optimal_follower_distance": self.optimal_follower_distance[i]
                })

    def appendGoalPerformanceMeasures(self):
        fullPath = os.path.join(self.goalPerformanceRecordsDirectory, "parameter_tuning.csv")

        self.GPA = GoalPerformanceAnalyzer(self.linear_distance_error,
                                           self.min_follower_distance[0],
                                           self.max_follower_distance[0],
                                           self.optimal_follower_distance[0])
        self.too_close_percentage = self.GPA.calcPercentTooClose()
        self.too_far_percentage = self.GPA.calcPercentTooFar()
        self.goal_distance_percentage = self.GPA.calcPercentGoalDist()

        with open(fullPath, 'a', ) as f:
            fieldnames = ["delta_time",
                          "proportional_gain",
                          "integral_gain",
                          "derivative_gain",
                          "logistic_function_mid",
                          "logistic_function_growth_rate",
                          "follower_too_far_percent",
                          "follower_too_close_percent",
                          "follower_goal_dist_percent"]
            csvWriter = csv.DictWriter(f, fieldnames=fieldnames)
            csvWriter.writerow({
                "delta_time" : self.delta_time[0],
                "proportional_gain" : self.proportional_gain[0],
                "integral_gain" : self.integral_gain[0],
                "derivative_gain" : self.derivative_gain[0],
                "logistic_function_mid" : self.logistic_function_mid[0],
                "logistic_function_growth_rate" : self.logistic_function_growth_rate[0],
                "follower_too_far_percent" : self.too_far_percentage,
                "follower_too_close_percent" : self.too_close_percentage,
                "follower_goal_dist_percent" : self.goal_distance_percentage
            })

