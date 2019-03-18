import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class LiveRoverTracker:

    def __init__(self):
        self.fig = plt.figure()
        self.axes = self.fig.add_axes([0,0,1,1])
        self.axes.set_ylim([0,200])
        self.axes.set_xlim([-100,100])

        self.leaderXs = [1]
        self.leaderZs = [15]
        self.leaderPoint, = self.axes.plot(self.leaderXs, self.leaderZs)

        self.followerXs = [1]
        self.followerZs = [1]
        #self.followerPoint, = self.axes.plot(self.followerXs, self.followerZs)

        # Flip to True when started by Supervisor
        self.started = False


    def updateLeaderCoords(self, leaderX, leaderZ):
        self.leaderXs.append(leaderX)
        self.leaderZs.append(leaderZ)

    def updateFollowerCoords(self, followerX, followerZ):
        self.followerXs.append(followerX)
        self.followerZs.append(followerZ)



    def animate(self, i):
        #plt.ion()
        print("HOLDING HERE")
        #self.axes.clear()


        if len(self.leaderXs) > 0:
            #self.axes.scatter(self.leaderXs, self.leaderZs, c='red', label="Leader")
            #self.axes.scatter(self.followerXs, self.followerZs, c='blue', label="Follower")
            '''
            self.axes.axis('equal')
            ylims = self.axes.get_ylim()
            xlims = self.axes.get_xlim()
            self.axes.plot([0, 0], ylims, c="black")
            self.axes.plot(xlims, [0, 0], c="black")
            ylims = self.axes.get_ylim()
            xlims = self.axes.get_xlim()
            self.axes.plot([0, 0], ylims, c="black")
            self.axes.plot(xlims, [0, 0], c="black")
            '''

            self.leaderPoint.set_xdata(self.leaderXs)
            self.leaderPoint.set_ydata(self.leaderZs)

            #self.followerPoint.set_xdata(self.followerXs)
            #self.followerPoint.set_ydata(self.followerZs)

            '''
            # Add circles for goal distances from Leader
            minCircle = plt.Circle((self.leaderXs[-1], self.leaderZs[-1]),
                                   12,
                                   color="red",
                                   fill=False)
            maxCircle = plt.Circle((self.leaderXs[-1], self.leaderZs[-1]),
                                   15,
                                   color="red",
                                   fill=False)
            optimalCircle = plt.Circle((self.leaderXs[-1], self.leaderZs[-1]),
                                       13.5,
                                       color="green",
                                       fill=False)
            self.axes.add_artist(minCircle)
            self.axes.add_artist(maxCircle)
            self.axes.add_artist(optimalCircle)
            '''
            plt.pause(0.5)
        else:
            pass

        return self.leaderPoint, #self.followerPoint

    def start(self):

        ani = animation.FuncAnimation(self.fig, self.animate, interval=1000, blit=True)
        plt.show(block=False)

