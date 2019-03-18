
from analysis.post_run_analysis import *

PostRunAnalysis = PostRunAnalyzer()

leaderXs = [1,1.2,1.3,1.4,1.6,1.7,2,2.5,3,3.5,3.5,3.5]
leaderZs = [1,1.2,1.3,1.4,1.6,1.7,2,2.5,3,3.5,3.5,3.5]

followerXs = [1,1.2,1.3,1.4,1.6,1.7,2,2.5,3,3.5,3.5,3.5]
followerZs = [1,1.2,1.3,1.4,1.6,1.7,2,2.5,3,3.5,3.5,3.5]

for i in range(0,len(leaderXs)):
    PostRunAnalysis.updateLeaderCoords(leaderXs[i],leaderZs[i])
    PostRunAnalysis.updateFollowerCoords(0.5 * followerXs[i], 0.5* followerZs[i])
    PostRunAnalysis.updateTime()
    PostRunAnalysis.updateGoalDistances()

PostRunAnalysis.revealAnimatedPlot()
