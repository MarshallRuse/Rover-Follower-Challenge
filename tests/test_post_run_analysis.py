import pandas as pd
from analysis.post_run_analysis import *

testData = pd.read_csv('post_run_testing_sample_data.csv')

PostRunAnalysis = PostRunAnalyzer(4)

leaderXs = list(testData['leader_world_cs_x'])
leaderZs = list(testData['leader_world_cs_z'])

followerXs = list(testData['follower_world_cs_x'])
followerZs = list(testData['follower_world_cs_z'])

follower2Xs = list(testData['follower_2_world_cs_x'])
follower2Zs = list(testData['follower_2_world_cs_z'])

follower3Xs = list(testData['follower_3_world_cs_x'])
follower3Zs = list(testData['follower_3_world_cs_z'])

follower4Xs = list(testData['follower_4_world_cs_x'])
follower4Zs = list(testData['follower_4_world_cs_z'])

for i in range(0,len(leaderXs)):
    PostRunAnalysis.updateLeaderCoords(leaderXs[i],leaderZs[i])
    PostRunAnalysis.updateFollowerCoords(1,followerXs[i], followerZs[i])
    PostRunAnalysis.updateFollowerCoords(2,follower2Xs[i], follower2Zs[i])
    PostRunAnalysis.updateFollowerCoords(3,follower3Xs[i], follower3Zs[i])
    PostRunAnalysis.updateFollowerCoords(4,follower4Xs[i], follower4Zs[i])

    PostRunAnalysis.updateTime()
    PostRunAnalysis.updateGoalDistances(1)
    PostRunAnalysis.updateGoalDistances(2)
    PostRunAnalysis.updateGoalDistances(3)
    PostRunAnalysis.updateGoalDistances(4)

PostRunAnalysis.revealAnimatedPlot()
