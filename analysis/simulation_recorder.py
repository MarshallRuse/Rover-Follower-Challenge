import os
import csv

class SimulationRecorder:

    def __init__(self):
        self.recordsDirectory = os.path.join(os.getcwd(), "analysis", "records")
        print("recordsDirectory is: " + self.recordsDirectory)
        # version number subject to change based on fields recorded
        self.recordVersionNum = 1

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
                        "omega",
                        "v",
                        "v_max",
                        "left_wheel_velocity",
                        "right_wheel_velocity",
                        "follower_wheel_radius",
                        "follower_axle_length"]

        # column value lists
        self.time = []
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
        self.omega = []
        self.v = []
        self.v_max = []
        self.left_wheel_velocity = []
        self.right_wheel_velocity = []
        self.follower_wheel_radius = []
        self.follower_axle_length = []

    # functions for recording column values
    def record_time(self, val):
        self.time.append(val)

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

    def record_omega(self, val):
        self.omega.append(val)

    def record_v(self, val):
        self.v.append(val)

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


    def writeToCSV(self):
        fullPath = os.path.join(self.recordsDirectory, self.fileName)
        with open(fullPath, 'w', newline='') as f:
            csvWriter = csv.DictWriter(f, fieldnames=self.columns)

            csvWriter.writeheader()
            for i in range(0, len(self.time)):
                csvWriter.writerow({
                    "time" : self.time[i],
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
                    "omega": self.omega[i],
                    "v" : self.v[i],
                    "v_max" : self.v_max[i],
                    "left_wheel_velocity" : self.left_wheel_velocity[i],
                    "right_wheel_velocity" : self.right_wheel_velocity[i],
                    "follower_wheel_radius" : self.follower_wheel_radius[i],
                    "follower_axle_length" : self.follower_axle_length[i]
                })