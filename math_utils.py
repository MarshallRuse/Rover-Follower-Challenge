import math
import numpy as np

'''
Takes the degrees clockwise from North (pos z-axis in simulation coordinates)
and converts to angle relative to positive x-axis. Positive angles are counter-clockwise
from positive x-axis, and angles range from [-180, 180], for easy conversion to radians
and atan2 function
'''
def compassToXRelative(degreesFromNorth):
    if degreesFromNorth >= 0 and degreesFromNorth <= 90:
        xRelative = 90 - degreesFromNorth
    elif degreesFromNorth > 90 and degreesFromNorth <= 270:
        xRelative = -1 * (degreesFromNorth - 90)
    elif degreesFromNorth > 270:
        xRelative = 90 + (360 - degreesFromNorth)
    return xRelative

def xRelativeToCompass(angleFromX):
    angleFromX = math.degrees(angleFromX)

    if angleFromX >= 0 and angleFromX <= 90:
        compassRelative = 90 - angleFromX
    elif angleFromX > 90 and angleFromX <= 180:
        compassRelative = -1 * (90 - (180 - angleFromX))
    elif angleFromX < 0 and angleFromX >= -90:
        compassRelative = 90 + (-1 * angleFromX)
    else:
        compassRelative = -90 - (180 + angleFromX)
    return math.radians(compassRelative)

'''
rotateCounterClockwise rotates a matrix (possibly vector) in the counter clockwise direction by 
the specified angle. The vector is rotated clockwise in accordance with the GPS
coordinates returned by the simulation, which are number of degrees clockwise from
the z-axis (north).
'''
def rotateCounterClockwise(matrix, angle):

    angle = math.radians(angle)

    a = math.cos(angle)
    b = -1 * math.sin(angle)
    c = math.sin(angle)
    d = math.cos(angle)

    rotationMat = np.array([[a,b],
                      [c,d]])
    matrix = np.array(matrix)

    rotatedMat = rotationMat.dot(matrix)

    return rotatedMat.tolist()

'''
rotateClockwise rotates a matrix (possibly single vector) in the clockwise direction by 
the specified angle. The matrix is rotated clockwise in accordance with the GPS
coordinates returned by the simulation, which are number of degrees clockwise from
the z-axis (north).
'''
def rotateClockwise(matrix, angle):
    # rotation matrices are counterclockwise by default
    # invert for clockwise, convert to radians for python trig functions
    angle = math.radians(-1 * angle)

    a = math.cos(angle)
    b = -1 * math.sin(angle)
    c = math.sin(angle)
    d = math.cos(angle)

    rotationMat = np.array([[a,b],
                      [c,d]])
    matrix = np.array(matrix)

    rotatedMat = rotationMat.dot(matrix)

    return rotatedMat.tolist()

'''
clockwiseRotationMatrix returns a 2D List representing the canonical
Cartesian coordinate system, rotated by the input angle. Each inner list represents
a column vector for one of the basis vectors of the new coordinate system.
'''
def counterClockwise2DRotationMatrix(angle):
    basis = [[1,0],[0,1]]
    rotatedBasis = rotateCounterClockwise(basis,angle)

    return rotatedBasis

'''
clockwiseRotationMatrix returns a 2D List representing the canonical
Cartesian coordinate system, rotated by the input angle. Each inner list represents
a column vector for one of the basis vectors of the new coordinate system.
'''
def clockwise2DRotationMatrix(angle):
    basis = [[1,0],[0,1]]
    rotatedBasis = rotateClockwise(basis,angle)

    return rotatedBasis


def differenceVec(Bx, Bz, Ax, Az):
    diffX = Bx - Ax
    diffZ = Bz - Az
    return [diffX, diffZ]

def euclideanDist(point2, point1):
    diffVec = differenceVec(point2[0], point2[1], point1[0], point1[1])
    return (diffVec[0]**2 + diffVec[1]**2)**0.5

def logistic(x, mid=0, max=1, growthRate=1):
    return max / (1 + math.exp(-1 * growthRate * (x - mid)))

def tanh(x):
    return (2 / (1 + math.exp(-2 * x))) - 1
'''
matrixInverse returns the inverse of a matrix
'''
def matrixInverse(matrix):
    matrix = np.array(matrix)
    inverseMat = np.linalg.inv(matrix)
    return inverseMat.tolist()

def matrixVectorMult(matrix, vector):

    vecLength = len(vector)
    matCols = len(matrix)
    matRows = len(matrix[0])

    if vecLength != matCols:
        return "Matrix-vector dimensions do not agree"

    mat = np.array(matrix)
    vec = np.array(vector)

    productVec = mat.dot(vec)

    return productVec.tolist()

def followerFrameTransformation(compassAngle, followerCoords):

    # get the clockwise rotation matrix for the Follower's heading
    rotationMat = clockwise2DRotationMatrix(compassAngle)
    #xRelAngle = compassToXRelative(compassAngle)
    #rotationMat = counterClockwise2DRotationMatrix(xRelAngle)

    # Invert that rotation matrix, and convert to numpy matrix
    invRotationMat = matrixInverse(rotationMat)
    invRotationMat = np.array(invRotationMat)

    # convert follower coordinates to a frame translation vector (as a numpy array)
    # Assumes home/world coordinate system origin is [0,0]
    followerCoords = np.array(followerCoords)
    translationVec = -1 * followerCoords
    #translationVec = translationVec.reshape(-1,1)

    '''For traditional rigid body transformation matrix, uncomment below.
    For the purposes of this transformation, its more useful to return values independently '''
    ## Concatenate rotation and translation into a frame transformation
    ## (rotation + translation)
    #rigidTransformation = np.concatenate((invRotationMat, translationVec), axis=1)
    #padding = np.array([0,0,1])
    #rigidTransformation = np.vstack((rigidTransformation, padding))

    #return rigidTransformation.tolist()

    return invRotationMat.tolist(), translationVec.tolist()

def leaderInFollowerFrame(followerFrameRotation, followerFrameTranslation, leaderCoords):

    # pad for frame transformation matrix
    #leaderCoords.append(1)

    # translate first by distance from Follower
    leaderCoords = np.array(leaderCoords)
    leaderCoordsTrans = leaderCoords + np.array(followerFrameTranslation)
    # translate back to list (I know this is stupid, but too lazy to rework every function
    # to accept np arrays or python lists)
    leaderCoordsTrans = leaderCoordsTrans.tolist()

    leaderInFollowerCoords = matrixVectorMult(followerFrameRotation, leaderCoordsTrans)

    # remove padding
    #leaderInFollowerCoords.pop()

    return leaderInFollowerCoords
