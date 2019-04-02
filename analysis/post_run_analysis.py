import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math_utils
import global_vars

class PostRunAnalyzer:

    def __init__(self, numFollowers):

        self.numFollowers = numFollowers

        self.fig = plt.figure(figsize=[8,7])
        self.axes = self.fig.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [3, 1]})

        self.leaderXs = [1]
        self.leaderZs = [15]
        self.animatedLeaderXs = [1]
        self.animatedLeaderZs = [15]

        self.followerXs = []
        for i in range(0, numFollowers):
            self.followerXs.append([1])

        self.followerZs = []
        for i in range(0, numFollowers):
            self.followerZs.append([1])

        self.animatedFollowerXs = []
        for i in range(0, numFollowers):
            self.animatedFollowerXs.append([1])

        self.animatedFollowerZs = []
        for i in range(0, numFollowers):
            self.animatedFollowerZs.append([15])

        self.follower_FT_R11s = []
        for i in range(0, numFollowers):
            self.follower_FT_R11s.append([])

        self.follower_FT_R21s = []
        for i in range(0, numFollowers):
            self.follower_FT_R21s.append([])

        self.follower_FT_R12s = []
        for i in range(0, numFollowers):
            self.follower_FT_R12s.append([])

        self.follower_FT_R22s = []
        for i in range(0, numFollowers):
            self.follower_FT_R22s.append([])

        self.animatedFollower_FT_R11s = []
        for i in range(0, numFollowers):
            self.animatedFollower_FT_R11s.append([])

        self.animatedFollower_FT_R21s = []
        for i in range(0, numFollowers):
            self.animatedFollower_FT_R21s.append([])

        self.animatedFollower_FT_R12s = []
        for i in range(0, numFollowers):
            self.animatedFollower_FT_R12s.append([])

        self.animatedFollower_FT_R22s = []
        for i in range(0, numFollowers):
            self.animatedFollower_FT_R22s.append([])


        self.currentTime = 0
        self.times = [0]
        self.timesSec = [0]
        self.timeElapsed = 0
        self.goalDistances = []
        for i in range(0, numFollowers):
            self.goalDistances.append([0])

        self.goalDeviances = []
        for i in range(0, numFollowers):
            self.goalDeviances.append([0])

        self.goalDistanceFlags = [] # -1: Too Close, 0: Good, 1: Too Far
        for i in range(0, numFollowers):
            self.goalDistanceFlags.append([0])

        self.count = 1

        self.animationInterval = 500 # ms
        self.animatedDeviances = []
        for i in range(0, numFollowers):
            self.animatedDeviances.append([0])

        self.animatedTimes = [0]

    def updateLeaderCoords(self, leaderX, leaderZ):
        self.leaderXs.append(leaderX)
        self.leaderZs.append(leaderZ)

    def updateFollowerCoords(self, followerNum, followerX, followerZ):
        followerNum -= 1 # Followers are 1-based index
        self.followerXs[followerNum].append(followerX)
        self.followerZs[followerNum].append(followerZ)

    def updateFollowerFrameTrans(self, followerNum, FT):
        followerNum -= 1 # Followers are 1-based index
        self.follower_FT_R11s[followerNum].append(FT[0][0])
        self.follower_FT_R21s[followerNum].append(FT[1][0])
        self.follower_FT_R12s[followerNum].append(FT[0][1])
        self.follower_FT_R22s[followerNum].append(FT[1][1])

    def updateTime(self):
        self.currentTime += 1
        self.times.append(self.currentTime)
        self.timesSec.append(self.currentTime * global_vars.delta_time)

    def updateGoalDistances(self, followerNum):
        followerNum -= 1
        dist = math_utils.euclideanDist([self.leaderXs[-1],self.leaderZs[-1]],
                                        [self.followerXs[followerNum][-1],self.followerZs[followerNum][-1]])
        if dist > 15:
            self.goalDistanceFlags[followerNum].append(1)
        elif dist < 12:
            self.goalDistanceFlags[followerNum].append(-1)
        else:
            self.goalDistanceFlags[followerNum].append(0)

        deviance = dist - 13.5

        self.goalDistances[followerNum].append(dist)
        self.goalDeviances[followerNum].append(deviance)

    def plotResultsStatic(self):
        self.axes[0].scatter(self.followerXs, self.followerZs, c=self.times, cmap="Blues",
                     label="Follower")
        self.axes[0].scatter(self.leaderXs, self.leaderZs, c=self.times, cmap="Reds",
                     label="Leader")
        ylims = self.axes[0].get_ylim()
        xlims = self.axes[0].get_xlim()
        self.axes[0].plot([0, 0], ylims, c="black")
        self.axes[0].plot(xlims, [0, 0], c="black")

        self.axes[0].legend()

    def plotResultsAnimated(self, i):
        stepForward = round((self.count/global_vars.delta_time))
        if stepForward > len(self.followerXs[0]):
            stepForward = len(self.followerXs[0])

        for follNum in range(0, self.numFollowers):
            self.animatedFollowerXs[follNum] = self.followerXs[follNum][:stepForward]
            self.animatedFollowerZs[follNum] = self.followerZs[follNum][:stepForward]
            #self.animatedFollower_FT_R11s[follNum] = self.follower_FT_R11s[follNum][:stepForward]
            #print("follNum is: " + str(follNum))
            #print(self.follower_FT_R11s[follNum])
            #print(self.animatedFollower_FT_R11s[follNum])
            #self.animatedFollower_FT_R21s[follNum] = self.follower_FT_R21s[follNum][:stepForward]
            #self.animatedFollower_FT_R12s[follNum] = self.follower_FT_R12s[follNum][:stepForward]
            #self.animatedFollower_FT_R22s[follNum] = self.follower_FT_R22s[follNum][:stepForward]

            self.animatedLeaderXs = self.leaderXs[:stepForward]
            self.animatedLeaderZs = self.leaderZs[:stepForward]

            self.animatedDeviances[follNum] = self.goalDeviances[follNum][:stepForward]
            self.animatedTimes = self.timesSec[:stepForward]

        self.axes[0].clear()
        self.axes[1].clear()


        #self.axes[0].scatter(self.animatedLeaderXs, self.animatedLeaderZs, c=self.times[:stepForward], cmap="Reds",
        #                  label="Leader")
        self.axes[0].scatter(self.animatedLeaderXs[:(stepForward-1)], self.animatedLeaderZs[:(stepForward - 1)], facecolors='none',
                            edgecolors='red')
        self.axes[0].scatter(self.animatedLeaderXs[-1], self.animatedLeaderZs[-1],
                            facecolors='red',edgecolors='red', label="Leader")

        trackerColours = ['blue','orange','green','magenta']
        for follNum in range(0, self.numFollowers):
            #self.axes[0].scatter(self.animatedFollowerXs, self.animatedFollowerZs, c=self.times[:stepForward], cmap="Blues",
            #                  label="Follower")
            self.axes[0].scatter(self.animatedFollowerXs[follNum][:(stepForward - 1)], self.animatedFollowerZs[follNum][:(stepForward - 1)],
                                 facecolors='none',
                                 edgecolors=trackerColours[follNum], alpha=0.5)
            self.axes[0].scatter(self.animatedFollowerXs[follNum][-1], self.animatedFollowerZs[follNum][-1],
                                 facecolors=trackerColours[follNum], edgecolors=trackerColours[follNum], label="Follower")

            ylims = self.axes[0].get_ylim()
            xlims = self.axes[0].get_xlim()
            self.axes[0].plot([0, 0], ylims, c="black")
            self.axes[0].plot(xlims, [0, 0], c="black")
            self.axes[0].axis('equal')

            if self.goalDistanceFlags[follNum][stepForward - 1] == 1 or self.goalDistanceFlags[follNum][stepForward - 1] == -1:
                self.axes[0].set_facecolor('xkcd:salmon')
            elif self.goalDistanceFlags[follNum][stepForward - 1] == 0:
                self.axes[0].set_facecolor('xkcd:mint green')

            self.axes[0].set_title('Leader, Follower in World Coordinates', fontdict = {'fontsize':'small',
                                                                          'fontweight': 'bold'})
            self.axes[0].set_xlabel('x', fontdict = {'fontsize':'small',
                                                                          'fontweight': 'bold'})
            self.axes[0].set_ylabel('z', fontdict = {'fontsize':'small',
                                                                          'fontweight': 'bold'})

            # Add circles for goal distances from Leader
        minCircle = plt.Circle((self.animatedLeaderXs[-1], self.animatedLeaderZs[-1]),12, color="red", fill=False)
        maxCircle = plt.Circle((self.animatedLeaderXs[-1], self.animatedLeaderZs[-1]),15, color="red",fill=False)
        optimalCircle = plt.Circle((self.animatedLeaderXs[-1], self.animatedLeaderZs[-1]),13.5, color="green",fill=False)
        self.axes[0].add_artist(minCircle)
        self.axes[0].add_artist(maxCircle)
        self.axes[0].add_artist(optimalCircle)

        for follNum in range(0, self.numFollowers):
            #FT_R11 = self.animatedFollower_FT_R11s[follNum][-1]
            #FT_R21 = self.animatedFollower_FT_R21s[follNum][-1]
            #FT_R12 = self.animatedFollower_FT_R12s[follNum][-1]
            #FT_R22 = self.animatedFollower_FT_R22s[follNum][-1]

            #followerFT = np.array([[FT_R11, FT_R12], [FT_R21, FT_R22]])
            #invFollowerFT = np.linalg.inv(followerFT)

            #basis = np.array([[20, 0], [0, 20]])
            #rotatedBasis = invFollowerFT.dot(basis)

            #followerPos = np.array([self.animatedFollowerXs[follNum][-1], self.animatedFollowerZs[follNum][-1]])
            # Find the end points for the follower's own axes IN WORLD CS
            # Translate the basis to the Follower's position IN WORLD CS
            #followerXAxEP1 = followerPos - rotatedBasis[:, 0]
            #followerXAxEP2 = followerPos + rotatedBasis[:, 0]
            #followerZAxEP1 = followerPos - rotatedBasis[:, 1]
            #followerZAxEP2 = followerPos + rotatedBasis[:, 1]

            # x-axis
            #self.axes[0].plot(np.array([followerXAxEP1[0], followerXAxEP2[0]]), np.array([followerXAxEP1[1], followerXAxEP2[1]]),
                              #color='b')
            # z-axis
            #self.axes[0].plot(np.array([followerZAxEP1[0], followerZAxEP2[0]]), np.array([followerZAxEP1[1], followerZAxEP2[1]]),
                              #color='b')

            self.axes[1].set_xlim(0, self.timeElapsed)
            self.axes[1].set_ylim(-5, 5)

            # Plot the goal-deviance vs. time graph
            self.axes[1].plot(self.axes[1].get_xlim(),[1.5,1.5], c="black")
            self.axes[1].plot(self.axes[1].get_xlim(), [-1.5, -1.5], c="black")
            self.axes[1].plot(self.axes[1].get_xlim(), [0, 0], c="black")
            self.axes[1].axhspan(-5,-1.5, facecolor='xkcd:salmon', alpha=0.7)
            self.axes[1].axhspan(-1.5,1.5, facecolor='xkcd:mint green', alpha=0.7)
            self.axes[1].axhspan(1.5, 5, facecolor='xkcd:salmon', alpha=0.7)

            self.axes[1].plot(self.animatedTimes, self.animatedDeviances[follNum], linewidth=2, c=trackerColours[follNum])

            self.axes[1].set_title('Goal Deviance over Time', fontdict = {'fontsize':'small',
                                                                          'fontweight': 'bold'})
            self.axes[1].set_xlabel('Time (s)', fontdict = {'fontsize':'small',
                                                                          'fontweight': 'bold'})
            self.axes[1].set_ylabel('Deviance', fontdict = {'fontsize':'small',
                                                                          'fontweight': 'bold'})

            self.fig.tight_layout()

            self.count += 1

    def revealStaticPlot(self):
        self.plotResultsStatic()
        plt.show()

    def revealAnimatedPlot(self):
        self.timeElapsed = self.currentTime * global_vars.delta_time # seconds


        self.ani = animation.FuncAnimation(self.fig, self.plotResultsAnimated, interval=self.animationInterval)
        plt.show()