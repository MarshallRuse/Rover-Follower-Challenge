import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math_utils
import global_vars

class PostRunAnalyzer:

    def __init__(self):
        self.fig = plt.figure(figsize=[8,7])
        self.axes = self.fig.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [3, 1]})

        self.leaderXs = [1]
        self.leaderZs = [15]
        self.animatedLeaderXs = [1]
        self.animatedLeaderZs = [15]

        self.followerXs = [1]
        self.followerZs = [1]
        self.animatedFollowerXs = [1]
        self.animatedFollowerZs = [15]

        self.currentTime = 0
        self.times = [0]
        self.timesSec = [0]
        self.timeElapsed = 0
        self.goalDistances = [0]
        self.goalDeviances = [0]
        self.goalDistanceFlags = [0] # -1: Too Close, 0: Good, 1: Too Far
        self.count = 1

        self.animationInterval = 500 # ms
        self.animatedDeviance = [0]
        self.animatedTimes = [0]

    def updateLeaderCoords(self, leaderX, leaderZ):
        self.leaderXs.append(leaderX)
        self.leaderZs.append(leaderZ)

    def updateFollowerCoords(self, followerX, followerZ):
        self.followerXs.append(followerX)
        self.followerZs.append(followerZ)

    def updateTime(self):
        self.currentTime += 1
        self.times.append(self.currentTime)
        self.timesSec.append(self.currentTime * global_vars.delta_time)

    def updateGoalDistances(self):
        dist = math_utils.euclideanDist([self.leaderXs[-1],self.leaderZs[-1]],
                                        [self.followerXs[-1],self.followerZs[-1]])
        if dist > 15:
            self.goalDistanceFlags.append(1)
        elif dist < 12:
            self.goalDistanceFlags.append(-1)
        else:
            self.goalDistanceFlags.append(0)

        deviance = dist - 13.5

        self.goalDistances.append(dist)
        self.goalDeviances.append(deviance)

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
        if stepForward > len(self.followerXs):
            stepForward = len(self.followerXs)

        self.animatedFollowerXs = self.followerXs[:stepForward]
        self.animatedFollowerZs = self.followerZs[:stepForward]
        self.animatedLeaderXs = self.leaderXs[:stepForward]
        self.animatedLeaderZs = self.leaderZs[:stepForward]

        self.animatedDeviance = self.goalDeviances[:stepForward]
        self.animatedTimes = self.timesSec[:stepForward]

        self.axes[0].clear()
        self.axes[1].clear()


        self.axes[0].scatter(self.animatedLeaderXs, self.animatedLeaderZs, c=self.times[:stepForward], cmap="Reds",
                          label="Leader")
        self.axes[0].scatter(self.animatedFollowerXs, self.animatedFollowerZs, c=self.times[:stepForward], cmap="Blues",
                          label="Follower")

        ylims = self.axes[0].get_ylim()
        xlims = self.axes[0].get_xlim()
        self.axes[0].plot([0, 0], ylims, c="black")
        self.axes[0].plot(xlims, [0, 0], c="black")
        self.axes[0].axis('equal')

        if self.goalDistanceFlags[stepForward - 1] == 1 or self.goalDistanceFlags[stepForward - 1] == -1:
            self.axes[0].set_facecolor('xkcd:salmon')
        elif self.goalDistanceFlags[stepForward - 1] == 0:
            self.axes[0].set_facecolor('xkcd:mint green')

        self.axes[0].set_title('Leader, Follower in World Coordinates', fontdict = {'fontsize':'small',
                                                                      'fontweight': 'bold'})
        self.axes[0].set_xlabel('x', fontdict = {'fontsize':'small',
                                                                      'fontweight': 'bold'})
        self.axes[0].set_ylabel('z', fontdict = {'fontsize':'small',
                                                                      'fontweight': 'bold'})

        self.axes[1].set_xlim(0, self.timeElapsed)
        self.axes[1].set_ylim(-5, 5)

        # Plot the goal-deviance vs. time graph
        self.axes[1].plot(self.axes[1].get_xlim(),[1.5,1.5], c="black")
        self.axes[1].plot(self.axes[1].get_xlim(), [-1.5, -1.5], c="black")
        self.axes[1].plot(self.axes[1].get_xlim(), [0, 0], c="black")
        self.axes[1].axhspan(-5,-1.5, facecolor='xkcd:salmon', alpha=0.7)
        self.axes[1].axhspan(-1.5,1.5, facecolor='xkcd:mint green', alpha=0.7)
        self.axes[1].axhspan(1.5, 5, facecolor='xkcd:salmon', alpha=0.7)

        self.axes[1].plot(self.animatedTimes, self.animatedDeviance, linewidth=2)

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