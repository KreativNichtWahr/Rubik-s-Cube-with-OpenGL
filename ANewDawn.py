import sys
import math
import numpy as np


def createNewCubyData(amount, cubyWidth, *tRC): # tRC = topRightCorner, but the verteces' colors are also part of that n-tuple (second half)

    listWithCubies = []
    cubyData = np.zeros(8, [("position", np.float32, 3), ("color", np.float32, 4)])
    dataIndices = np.array([0,1,3, 1,2,3, 5,0,4, 0,3,4, 6,5,7, 5,4,7, 1,6,2, 6,7,2, 5,6,0, 6,1,0, 7,4,2, 4,3,2], dtype = np.int32)

    for i in range(amount):
        cubyData["position"] = [tRC[i], (tRC[i][0]-cubyWidth, tRC[i][1], tRC[i][2]), (tRC[i][0]-cubyWidth, tRC[i][1]-cubyWidth, tRC[i][2]), (tRC[i][0], tRC[i][1]-cubyWidth, tRC[i][2]), (tRC[i][0], tRC[i][1]-cubyWidth, tRC[i][2]-cubyWidth), (tRC[i][0], tRC[i][1], tRC[i][2]-cubyWidth), (tRC[i][0]-cubyWidth, tRC[i][1], tRC[i][2]-cubyWidth), (tRC[i][0]-cubyWidth, tRC[i][1]-cubyWidth, tRC[i][2]-cubyWidth)]
        convertedData = np.zeros(36, [("position", np.float32, 3), ("color", np.float32, 4), ("animationAngles", np.float32, 3)])

        for count, e in enumerate(dataIndices):
            convertedData["position"][count] = cubyData["position"][e]
            try:
                convertedData["color"][count] = tRC[amount][i * 36 + count]         # Skip the topRightCorner positions and the colors for the cubes which have already been treated
            except:
                print("Weird, you did not finish filling in the arguments...")

        listWithCubies.append(convertedData)

    return listWithCubies


def vertexToQuat(cube, betraege):

    listWithQuats = np.empty(27, dtype = np.object_)
    listWithQuats.fill(np.array([], dtype = np.object_))
    normalizedCuby = np.zeros(36, [("position", np.float32, 4)])

    for cubyIndex, cuby in enumerate(cube):
        for index, vertex in enumerate(cuby):
            # Normalize Ortsvektoren and store Beträge
            #listWithQuats[cubyIndex][index]["position"][:3] = np.divide(vertex["position"],np.array([math.sqrt(math.pow(vertex["position"][0],2) + math.pow(vertex["position"][1],2) + math.pow(vertex["position"][2],2))],dtype=np.float32))
            normalizedCuby[index]["position"][:3] = np.divide(vertex["position"],np.array([math.sqrt(math.pow(vertex["position"][0],2) + math.pow(vertex["position"][1],2) + math.pow(vertex["position"][2],2))],dtype=np.float32))

        listWithQuats[cubyIndex] = normalizedCuby
        normalizedCuby = np.zeros(36, [("position", np.float32, 4)])

    print(listWithQuats)
    return listWithQuats


def quatMult(listWithQuats, multQuat):

    invMultQuat = np.zeros(4, dtype = np.float32)
    invMultQuat[:3] = (-1) * multQuat[:3]
    multipliedCuby = np.zeros(36, [("position", np.float32, 4)])
    temp = np.zeros(4, dtype = np.float32)

    for cubyIndex, cuby in enumerate(listWithQuats):
        for index, vertex in enumerate(cuby):
            

            mutlipliedCuby[index]["position"][:3][0] =

        listWithQuats[cubyIndex] = multipliedCuby
        multipliedCuby = np.zeros(36, [("position", np.float32, 4)])

if __name__ == "__main__":

    listWithCubies = createNewCubyData(
                                27, 1.0,
                                # topRightCorner positions
                                (1.7,1.7,1.7), (0.5,1.7,1.7), (-0.7,1.7,1.7),
                                (1.7,0.5,1.7), (0.5,0.5,1.7), (-0.7,0.5,1.7),
                                (1.7,-0.7,1.7), (0.5,-0.7,1.7), (-0.7,-0.7,1.7),

                                (1.7,1.7,0.5), (0.5,1.7,0.5), (-0.7,1.7,0.5),
                                (1.7,0.5,0.5), (0.5,0.5,0.5), (-0.7,0.5,0.5),
                                (1.7,-0.7,0.5), (0.5,-0.7,0.5), (-0.7,-0.7,0.5),

                                (1.7,1.7,-0.7), (0.5,1.7,-0.7), (-0.7,1.7,-0.7),
                                (1.7,0.5,-0.7), (0.5,0.5,-0.7), (-0.7,0.5,-0.7),
                                (1.7,-0.7,-0.7), (0.5,-0.7,-0.7), (-0.7,-0.7,-0.7),

                                # colors
                                #dataIndices = np.array([0,1,3, 1,2,3, 5,0,4, 0,3,4, 6,5,7, 5,4,7, 1,6,2, 6,7,2, 5,6,0, 6,1,0, 7,4,2, 4,3,2], dtype = np.int32)

                                # Six arguments = six verteces' colors = one face
                                # Six lines = six faces = one cube
                                # 9 blocks of six lines each = front cubes
                                [
                                (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                                (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                                (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                                (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                                (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                                (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),

                                (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),

                                (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                                (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),




                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                                (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                                (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                                (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),




                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                                (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                                (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                                (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0), (1.0,1.0,1.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                                (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                                (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                                (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0), (0.0,0.0,1.0,1.0),
                                (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),

                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,0.5,0.0,1.0),
                                (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0),
                                (0.0,0.0,0.0,0.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0), (0.0,0.0,0.0,1.0),
                                (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0), (1.0,1.0,0.0,1.0),
                                ]
                )

    betraege = np.zeros(972, dtype = np.float32)
    listWithQuats = vertexToQuat(listWithCubies, betraege)
    listWithMultQuats = quatMult(listWithQuats, np.array([0.0,1.0,0.0,0.0], dtype = np.float32))
