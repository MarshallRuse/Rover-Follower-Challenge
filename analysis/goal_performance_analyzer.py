

class GoalPerformanceAnalyzer:

    def __init__(self, linearDistErrors, tooCloseDist, tooFarDist, optimalDist):
        self.linearDistanceError = linearDistErrors
        self.tooClose = tooCloseDist
        self.tooFar = tooFarDist
        self.optimal = optimalDist
        self.tooCloseErr = self.tooClose - self.optimal  # 12 - 13.5 = -1.5
        self.tooFarErr = self.tooFar - self.optimal # 15 - 13.5 = 1.5

    def calcPercentTooClose(self):
        count = 0
        total = len(self.linearDistanceError)

        for dist in self.linearDistanceError:
            if dist < self.tooCloseErr:
                count += 1
        return count / total

    def calcPercentTooFar(self):
        count = 0
        total = len(self.linearDistanceError)

        for dist in self.linearDistanceError:
            if dist > self.tooFarErr:
                count += 1
        return count / total

    def calcPercentGoalDist(self):
        count = 0
        total = len(self.linearDistanceError)

        for dist in self.linearDistanceError:
            if dist < self.tooFarErr and dist > self.tooCloseErr:
                count += 1
        return count / total