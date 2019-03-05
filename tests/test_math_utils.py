import math
import math_utils as mu

# Test Rotation of 2d basis
base = [[1,0],[0,1]]
mu.rotateClockwise(base,45)


# Test 45 degree rotation clockwise of point
# Point in canonical Cartesian coordinate system
point1A = [-10,20] # interpreted as column vector
print("point1A: " + str(point1A))
point1B = mu.rotateClockwise(point1A, 45)
print("point1B: " + str(point1B) + "\n")

# Test 180 degree rotation clockwise of point
# Point in canonical Cartesian coordinate system
point2A = [15,-25] # interpreted as column vector
print("point2A: " + str(point2A))
point2B = mu.rotateClockwise(point2A, 180)
print("point2B: " + str(point2B) + "\n")


# Rotation Matrix for 45 degree rotation clockwise
mat1 = mu.clockwise2DRotationMatrix(45)
print("Mat1 is: " + str(mat1))


# Inverse of Mat1
mat1B = mu.matrixInverse(mat1)
print("Mat1B is: " + str(mat1B) + "\n")


# Rotation Matrix for 70 degree rotation clockwise
mat2 = mu.clockwise2DRotationMatrix(70)
print("Mat2 is: " + str(mat2))

# Inverse of Mat2
mat2B = mu.matrixInverse(mat2)
print("Mat2B is: " + str(mat2B) + "\n")

# Rotation matrix of 16.5 degree rotation clockwise
mat165 = mu.clockwise2DRotationMatrix(16.5)
print("Mat165 is: " + str(mat165))
invMat165 = mu.matrixInverse(mat165)
print("InvMat165 is: " + str(invMat165))
point165 = [14.5,15.5]
rotatedPoint165 = mu.matrixVectorMult(invMat165,point165)
print("rotatedPoint165 is: " + str(rotatedPoint165) + "\n")

# Rotation matrix of 26.7 degree rotation clockwise
mat267 = mu.clockwise2DRotationMatrix(26.7)
print("Mat267 is: " + str(mat267))
invMat267 = mu.matrixInverse(mat267)
print("InvMat267 is: " + str(invMat267))
point267 = [27.8,6.6]
rotatedPoint267 = mu.matrixVectorMult(invMat267,point267)
print("rotatedPoint267 is: " + str(rotatedPoint267) + "\n")


# Random Matrix
mat3 = [[5,15],[23,6]]
print("Mat3 is: " + str(mat3))
mat3B = mu.matrixInverse(mat3)
print("Mat3B is: " + str(mat3B) + "\n")

# Random 3x3 Matrix
mat4 = [[24, 17, 11],[5, 14, 15],[9, 8, 1]]
print("Mat4 is: " + str(mat4))
mat4B = mu.matrixInverse(mat4)
print("Mat4B is: " + str(mat4B) + "\n")

newCoords1 = mu.matrixVectorMult(mat1B, point1A)
print("newCoords1 are: " + str(newCoords1))


# Test followerFrameTransformation
fftRot1, fftTrans1 = mu.followerFrameTransformation(45, [10,20])
print("fftRot1 is: " + str(fftRot1))

# Test leader in follower frame
leaderCoords = [-10, 50]
leaderFFTCoords = mu.leaderInFollowerFrame(fftRot1, fftTrans1, leaderCoords)
print("Leader in FFT is: " + str(leaderFFTCoords))


# Test followerFrameTransformation, part 2
fftRot2, fftTrans2 = mu.followerFrameTransformation(120, [-5,60])
print("fftRot2 is: " + str(fftRot2))

# Test leader in follower frame
leaderCoords2 = [6, 80]
leaderFFTCoords2 = mu.leaderInFollowerFrame(fftRot2, fftTrans2, leaderCoords2)
print("Leader in FFT is: " + str(leaderFFTCoords2))

leaderCoords165 = [16.2, 35.8]
fftRot165, fftTrans165 = mu.followerFrameTransformation(16.5, [1.7,20.3])
leaderFFTCoords165 = mu.leaderInFollowerFrame(fftRot165, fftTrans165, leaderCoords165)
print("Leader in FFT is: " + str(leaderFFTCoords165))

leaderCoords267 = [42.7, 54.1]
fftRot267, fftTrans267 = mu.followerFrameTransformation(26.7, [14.9,47.5])
leaderFFTCoords267 = mu.leaderInFollowerFrame(fftRot267, fftTrans267, leaderCoords267)
print("Leader in FFT is: " + str(leaderFFTCoords267))