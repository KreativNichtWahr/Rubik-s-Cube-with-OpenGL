import sys
import math
import ctypes
import numpy as np
import random
import time

import OpenGL.GL as gl
import OpenGL.GLUT as glut



class wholeCube():

    def __init__(self, objectIndices, lineIndices, coordinateAxes, listWithCubies):

        # Set important variables and launch both init funcs
        self.lineIndices = lineIndices
        self.objectIndices = objectIndices
        self.coordinateAxes = coordinateAxes
        self.listWithCubies = np.array([*listWithCubies])
        self.cubeOrder = np.arange(27).reshape(3,3,3)
        self.angles = [0.0,0.0,0.0]
        self.xRotPos, self.yRotPos, self.zRotPos = 0,1,2
        self.difStartPosXRot, self.difStartYRot, self.difStartZRot = 0.0, 0.0, 0.0

        for i in range(27):
            self.cubeOrder[i//9][(i - i%3 - 2*(i//3))%3][2-i%3] = i

        self.whatCubesToRotate = np.array([])
        self.angleValue = 5*math.pi/180

        self.initGlut()
        self.initProgram()


    def initGlut(self):

        # Glut init
        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH)
        glut.glutCreateWindow("Rubik's Cube")
        glut.glutReshapeWindow(512, 512)
        glut.glutReshapeFunc(self.reshape)
        glut.glutKeyboardFunc(self.keyboard)
        glut.glutDisplayFunc(self.display)
        # Depth / Cull init
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthMask(gl.GL_TRUE)
        gl.glDepthFunc(gl.GL_LESS)
        #gl.glDepthRange(-1.0, 1.0)
        #gl.glEnable(gl.GL_CULL_FACE)
        #gl.glCullFace(gl.GL_BACK)

    def initProgram(self):

        # Shader code
        vertexShaderCode = """
            uniform vec3 angles;
            attribute float change;
            attribute vec3 position;
            attribute vec4 color;
            varying vec4 v_color;
            mat4 modelMatrix;
            mat4 viewMatrix;
            mat4 projectionMatrix;
            void main() {
                modelMatrix = mat4(1,0,0,0,  0,cos(angles.x),-sin(angles.x),0,  0,sin(angles.x),cos(angles.x),0,  0,0,0,1) *
                              mat4(cos(angles.y),0,sin(angles.y),0,  0,1,0,0,  -sin(angles.y),0,cos(angles.y),0,  0,0,0,1) *
                              mat4(cos(angles.z),-sin(angles.z),0,0,  sin(angles.z),cos(angles.z),0,0,  0,0,1,0,  0,0,0,1);
                viewMatrix = mat4(1,0,0,0,  0,1,0,0,  0,0,1,0,  0,0,-4.5,1);
                projectionMatrix = mat4(1,0,0,0,  0,1,0,0,  0,0,0,-1, 0,0,-1.5,0);
                vec4 temporary = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
                gl_Position = temporary / temporary.w;
                v_color = color;
            }
        """

        fragmentShaderCode = """
            varying vec4 v_color;
            void main() {
                gl_FragColor = v_color;
            }
        """

        # Compile and link shader code
        self.program = gl.glCreateProgram()
        vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

        gl.glShaderSource(vertexShader, vertexShaderCode)
        gl.glShaderSource(fragmentShader, fragmentShaderCode)

        gl.glCompileShader(vertexShader)
        if not gl.glGetShaderiv(vertexShader, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(vertexShader).decode()
            print(error)
            raise RuntimeError("Vertex shader compilation error")

        gl.glCompileShader(fragmentShader)
        if not gl.glGetShaderiv(fragmentShader, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(fragmentShader).decode()
            print(error)
            raise RuntimeError("Fragment shader compilation error")

        gl.glAttachShader(self.program, vertexShader)
        gl.glAttachShader(self.program, fragmentShader)

        gl.glLinkProgram(self.program)
        if not gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS):
            print(gl.glGetProgramInfoLog(self.program))
            raise RuntimeError("Linking error")

        gl.glDetachShader(self.program, vertexShader)
        gl.glDetachShader(self.program, fragmentShader)

        gl.glUseProgram(self.program)


    # Glut funcs
    def reshape(self, width, height):

        gl.glViewport(0, 0, width, height)


    def keyboard(self, key, x, y):

        # Cube rotations
        # Left
        if key == b'1':

            for _ in range(5):
                self.angles[1] -= 2*math.pi/180
                self.display()

        # Right
        elif key == b'3':

            for _ in range(5):
                self.angles[1] += 2*math.pi/180
                self.display()

        # Down
        elif key == b'2':

            if abs(self.angles[0] - self.difStartPosXRot) > math.pi/4:
                self.angles.append(self.angles[1])
                self.angles.pop(1)
                temp = self.yRotPos
                self.yRotPos = self.zRotPos
                self.zRotPos = temp
                self.difStartPosXRot += math.pi/2

            for _ in range(5):
                self.angles[0] += 2*math.pi/180
                self.display()

        # Up
        elif key == b'5':

            if abs(self.angles[0] - self.difStartPosXRot) > math.pi/4:
                self.angles.append(self.angles[1])
                self.angles.pop(1)
                temp = self.yRotPos
                self.yRotPos = self.zRotPos
                self.zRotPos = temp
                self.difStartPosXRot -= math.pi/2

            for _ in range(5):
                self.angles[0] -= 2*math.pi/180
                self.display()


        # Side rotations

        # Front
        elif key == b'f' or key == "f":

            self.rotateCubeSide(0, 0)
        # Back
        elif key == b'b' or key == "b":

            self.rotateCubeSide(0, 0, (0,1), 2, True)

        # Top
        elif key == b't' or key == "t":

            self.rotateCubeSide(2, 0, (0,1), 3)
        # Down
        elif key == b'd' or key == "d":

            self.rotateCubeSide(2, 0, (0,1), 1, True)

        # Right
        elif key == b'r' or key == "r":

            self.rotateCubeSide(1, 0, (0,2), 1)
        # Left
        elif key == b'l' or key == "l":

            self.rotateCubeSide(1, 0, (0,2), 3, True)

        # Middle
        elif key == b'm' or key == "m":

            self.rotateCubeSide(1, 1, (0,2), 3, True)
        # Equator
        elif key == b'e' or key == "e":

            self.rotateCubeSide(2, 1, (0,1), 1, True)
        # Standing
        elif key == b's' or key == "s":

            self.rotateCubeSide(0, 1)

        elif key == b'h':

            self.scramble(70)

        self.display()


    def rotateCubeSide(self, sideRotationMatricesArrayIndex, layer, axes = (0,1), amountForth = 0, invertAngle = False):

        if invertAngle:
            self.angleValue = -self.angleValue

        self.cubeOrder = np.rot90(self.cubeOrder, amountForth, axes = axes)
        self.whatCubesToRotate = self.cubeOrder[layer]
        self.cubeOrder[layer] = np.rot90(self.cubeOrder[layer], 3)
        self.cubeOrder = np.rot90(self.cubeOrder, 4-amountForth, axes = axes)

        sideRotationMatricesArray = (
            np.array([[np.cos(self.angleValue),np.sin(self.angleValue),0,0] , [-np.sin(self.angleValue),np.cos(self.angleValue),0,0] , [0,0,1,0] , [0,0,0,1]]),
            np.array([[1,0,0,0] , [0,np.cos(self.angleValue),np.sin(self.angleValue),0] , [0,-np.sin(self.angleValue),np.cos(self.angleValue),0] , [0,0,0,1]]),
            np.array([[np.cos(self.angleValue),0,-np.sin(self.angleValue),0] , [0,1,0,0] , [np.sin(self.angleValue),0,np.cos(self.angleValue),0] , [0,0,0,1]])
        )

        for _ in range(int(round((math.pi/2)/abs(self.angleValue)))):
            for cuby in [x for x in self.listWithCubies if np.where(x == self.listWithCubies)[0][0] in self.whatCubesToRotate]:
                for vertex in cuby:
                    vertex["position"] = (sideRotationMatricesArray[sideRotationMatricesArrayIndex] @ np.array([vertex["position"][0], vertex["position"][1], vertex["position"][2], 1]))[:3]
            self.display()

        self.angleValue = abs(self.angleValue)


    def scramble(self, amountOfMoves):

        self.angleValue = math.pi/6
        listWithMoves = [random.choice("fbtdrlmes") for _ in range(amountOfMoves)]
        for move in listWithMoves:
            self.keyboard(move, 0, 0)
            time.sleep(0.01)

        self.angleValue = 5*math.pi/180

    def display(self):

        loc = gl.glGetUniformLocation(self.program, "angles")
        gl.glUniform3f(loc, self.angles[self.xRotPos], self.angles[self.yRotPos], self.angles[self.zRotPos])

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        #gl.glClearColor(0.0, 0.0, 0.0, 0.0)
        #gl.glClearDepth(1.0)
        for i in self.listWithCubies:
            self.drawCubies(i)
        self.drawAxes()

        glut.glutSwapBuffers()


    # Buffer stuff
    def drawCubies(self, objectToDraw, outLines = True):

        Vbos = gl.glGenBuffers(4)

        posLoc = gl.glGetAttribLocation(self.program, "position")
        colorLoc = gl.glGetAttribLocation(self.program, "color")
        posOffset = ctypes.c_void_p(0)
        colorOffset = ctypes.c_void_p(objectToDraw.dtype["position"].itemsize)

        objectStride = objectToDraw.strides[0]

        # Cube itself
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbos[0])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, objectToDraw.nbytes, objectToDraw, gl.GL_DYNAMIC_DRAW)

        gl.glEnableVertexAttribArray(posLoc)
        gl.glVertexAttribPointer(posLoc, 3, gl.GL_FLOAT, False, objectStride, posOffset)

        gl.glEnableVertexAttribArray(colorLoc)
        gl.glVertexAttribPointer(colorLoc, 4, gl.GL_FLOAT, False, objectStride, colorOffset)

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, objectToDraw.size)

        """
        if not outLines:

            outlines = np.zeros(8, [("position", np.float32, 3), ("color", np.float32, 4)])
            outlines["position"] = objectToDraw["position"]
            outlines["color"] = np.ones(4, dtype = np.float32)

            # Lines for visibility's sake
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, Vbos[3])
            gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.lineIndices.nbytes, self.lineIndices, gl.GL_DYNAMIC_DRAW)

            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbos[1])
            gl.glBufferData(gl.GL_ARRAY_BUFFER, outlines.nbytes, outlines, gl.GL_DYNAMIC_DRAW)

            gl.glEnableVertexAttribArray(posLoc)
            gl.glVertexAttribPointer(posLoc, 3, gl.GL_FLOAT, False, objectStride, posOffset)

            gl.glEnableVertexAttribArray(colorLoc)
            gl.glVertexAttribPointer(colorLoc, 4, gl.GL_FLOAT, False, objectStride, colorOffset)

            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, Vbos[3])
            gl.glDrawElements(gl.GL_LINES, self.lineIndices.size, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        """

    def drawAxes(self):

        Vbo = gl.glGenBuffers(1)

        posLoc = gl.glGetAttribLocation(self.program, "position")
        colorLoc = gl.glGetAttribLocation(self.program, "color")
        posOffset = ctypes.c_void_p(0)
        colorOffset = ctypes.c_void_p(self.coordinateAxes.dtype["position"].itemsize)

        axesStride = self.coordinateAxes.strides[0]

        # Coordinate axes
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, Vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.coordinateAxes.nbytes, self.coordinateAxes, gl.GL_DYNAMIC_DRAW)

        gl.glEnableVertexAttribArray(posLoc)
        gl.glVertexAttribPointer(posLoc, 3, gl.GL_FLOAT, False, axesStride, posOffset)

        gl.glEnableVertexAttribArray(colorLoc)
        gl.glVertexAttribPointer(colorLoc, 4, gl.GL_FLOAT, False, axesStride, colorOffset)

        gl.glDrawArrays(gl.GL_LINES, 0, 6)


def createNewCubyDataTest(cubeType, cubyFaceWidth, cubyRoundedPartWidth, fTRC, colors):

    listWithCubies = []
    feinKoernigkeit = 9

    for cuby in range(cubeType**3):

        cubyData = np.zeros(36 + (feinKoernigkeit*6)*5, [("position", np.float32, 3), ("color", np.float32, 4)])
        tRC = (fTRC[0]-cuby+(cuby//3 * 3), fTRC[1]-(cuby//3)+(cuby//9 * 3), fTRC[2]-(cuby//9))
        # Colored Faces
        # Each line one triangle, 2 lines one face, up to the part where the rounded forms are being stored
        cubyData["position"][:36] = [
            # Front
            tRC, (tRC[0]-cubyFaceWidth, tRC[1], tRC[2]), (tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth, tRC[2]),
            tRC, (tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth, tRC[2]), (tRC[0], tRC[1]-cubyFaceWidth, tRC[2]),
            # Right
            (tRC[0]+cubyRoundedPartWidth, tRC[1], tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]+cubyRoundedPartWidth, tRC[1], tRC[2]-cubyRoundedPartWidth), (tRC[0]+cubyRoundedPartWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth),
            (tRC[0]+cubyRoundedPartWidth, tRC[1], tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]+cubyRoundedPartWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0]+cubyRoundedPartWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth),
            # Back
            (tRC[0]-cubyFaceWidth, tRC[1], tRC[2]-2*cubyRoundedPartWidth-cubyFaceWidth), (tRC[0], tRC[1], tRC[2]-2*cubyRoundedPartWidth-cubyFaceWidth), (tRC[0], tRC[1]-cubyFaceWidth, tRC[2]-2*cubyRoundedPartWidth-cubyFaceWidth),
            (tRC[0]-cubyFaceWidth, tRC[1], tRC[2]-2*cubyRoundedPartWidth-cubyFaceWidth), (tRC[0], tRC[1]-cubyFaceWidth, tRC[2]-2*cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth, tRC[2]-2*cubyRoundedPartWidth-cubyFaceWidth),
            # Left
            (tRC[0]-cubyRoundedPartWidth-cubyFaceWidth, tRC[1], tRC[2]-cubyRoundedPartWidth), (tRC[0]-cubyRoundedPartWidth-cubyFaceWidth, tRC[1], tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]-cubyRoundedPartWidth-cubyFaceWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth),
            (tRC[0]-cubyRoundedPartWidth-cubyFaceWidth, tRC[1], tRC[2]-cubyRoundedPartWidth), (tRC[0]-cubyRoundedPartWidth-cubyFaceWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]-cubyRoundedPartWidth-cubyFaceWidth, tRC[1]-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth),
            # Top
            (tRC[0], tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]-cubyFaceWidth, tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]-cubyFaceWidth, tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth),
            (tRC[0], tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0]-cubyFaceWidth, tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0], tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth),
            # Down
            (tRC[0]-cubyFaceWidth, tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0], tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0], tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth),
            (tRC[0]-cubyFaceWidth, tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth-cubyFaceWidth), (tRC[0], tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth),
        ]

        for colorIndex in range(36):
            cubyData["color"][colorIndex] = colors[cuby*36 + colorIndex]

        # Rounded parts
            # Middle
                # Front Top
        oldTopCorners = [(tRC[0], tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyRoundedPartWidth)]
        for korn in range(feinKoernigkeit):

            oldBottomCorners = [(tRC[0], tRC[1]+(math.cos((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth, tRC[2]-(1-math.sin((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]+(math.cos((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth, tRC[2]-(1-math.sin((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth)]
            cubyData["position"][(36+korn*6):(42+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
            oldTopCorners = oldBottomCorners

            cubyData["color"][(36+korn*6):(42+korn*6)] = [(0.2,0.8,0.8,1.0) for _ in range(6)]

                # Front Bot
        oldTopCorners = [(tRC[0], tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyRoundedPartWidth)]
        for korn in range(feinKoernigkeit):

            oldBottomCorners = [(tRC[0], tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth, tRC[2]-(1-math.sin((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth, tRC[2]-(1-math.sin((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth)]
            cubyData["position"][(90+korn*6):(96+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
            oldTopCorners = oldBottomCorners

            cubyData["color"][(90+korn*6):(96+korn*6)] = [(0.2,0.8,0.8,1.0) for _ in range(6)]

                # Back Top
        oldTopCorners = [(tRC[0], tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]+cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
        for korn in range(feinKoernigkeit):

            oldBottomCorners = [(tRC[0], tRC[1]+(math.cos((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-(1+math.sin((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]+(math.cos((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-(1+math.sin((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth)]
            cubyData["position"][(144+korn*6):(150+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
            oldTopCorners = oldBottomCorners

            cubyData["color"][(144+korn*6):(150+korn*6)] = [(0.2,0.8,0.8,1.0) for _ in range(6)]

                # Back Bot
        oldTopCorners = [(tRC[0], tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]-cubyRoundedPartWidth-cubyFaceWidth, tRC[2]-cubyFaceWidth-cubyRoundedPartWidth)]
        for korn in range(feinKoernigkeit):

            oldBottomCorners = [(tRC[0], tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-(1+math.sin((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth), (tRC[0]-cubyFaceWidth, tRC[1]-cubyFaceWidth-(math.cos((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth, tRC[2]-cubyFaceWidth-(1+math.sin((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth)]
            cubyData["position"][(198+korn*6):(204+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
            oldTopCorners = oldBottomCorners

            cubyData["color"][(198+korn*6):(204+korn*6)] = [(0.2,0.8,0.8,1.0) for _ in range(6)]

            # Standing
                # Front Right
        oldTopCorners = [(tRC[0], tRC[1]-cubyFaceWidth, tRC[2]), tRC]
        for korn in range(feinKoernigkeit):

            oldBottomCorners = [(tRC[0]+(math.sin((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth, tRC[1], tRC[2]-(1-math.cos((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth), (tRC[0]+(math.sin((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth, tRC[1]-cubyFaceWidth, tRC[2]-(1-math.cos((math.pi/2) * (korn+1)/9))*cubyRoundedPartWidth)]
            cubyData["position"][(252+korn*6):(258+korn*6)] = [*oldTopCorners, oldBottomCorners[0], oldTopCorners[1], *oldBottomCorners]
            oldTopCorners = oldBottomCorners

            cubyData["color"][(252+korn*6):(258+korn*6)] = [(0.2,0.8,0.8,1.0) for _ in range(6)]

        listWithCubies.append(cubyData)


    return listWithCubies



def createNewCubyData(amount, cubyWidth, *tRC): # tRC = topRightCorner, but the verteces' colors are also part of that n-tuple (second half)

    listWithCubies = []
    cubyData = np.zeros(8, [("position", np.float32, 3)])
    dataIndices = np.array([0,1,3, 1,2,3, 5,0,4, 0,3,4, 6,5,7, 5,4,7, 1,6,2, 6,7,2, 5,6,0, 6,1,0, 7,4,2, 4,3,2], dtype = np.int32)

    for i in range(amount):
        cubyData["position"] = [tRC[i], (tRC[i][0]-cubyWidth, tRC[i][1], tRC[i][2]), (tRC[i][0]-cubyWidth, tRC[i][1]-cubyWidth, tRC[i][2]), (tRC[i][0], tRC[i][1]-cubyWidth, tRC[i][2]), (tRC[i][0], tRC[i][1]-cubyWidth, tRC[i][2]-cubyWidth), (tRC[i][0], tRC[i][1], tRC[i][2]-cubyWidth), (tRC[i][0]-cubyWidth, tRC[i][1], tRC[i][2]-cubyWidth), (tRC[i][0]-cubyWidth, tRC[i][1]-cubyWidth, tRC[i][2]-cubyWidth)]
        convertedData = np.zeros(36, [("position", np.float32, 3), ("color", np.float32, 4)])

        for count, e in enumerate(dataIndices):
            convertedData["position"][count] = cubyData["position"][e]
            try:
                convertedData["color"][count] = tRC[amount][i * 36 + count]         # Skip the topRightCorner positions and the colors for the cubes which have already been treated
            except:
                print("Weird, you did not finish filling in the arguments...")

        listWithCubies.append(convertedData)

    print(listWithCubies)
    return listWithCubies



if __name__ == "__main__":

    # Cuby data
    dataIndices = np.array([0,1,3, 1,2,3, 5,0,4, 0,3,4, 6,5,7, 5,4,7, 1,6,2, 6,7,2, 5,6,0, 6,1,0, 7,4,2, 4,3,2], dtype = np.int32)
    edgeDataIndices = np.array([0,1, 1,2, 2,3, 3,0, 4,7, 7,6, 6,5, 5,4, 0,5, 1,6, 2,7, 3,4], dtype = np.int32)

    axesData = np.zeros(6, [("position", np.float32, 3), ("color", np.float32, 4)])
    axesData["position"] = [(0.0, 0.0, 0.0), (3.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 3.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 3.0)]
    axesData["color"] = [(1.0, 0.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0)]

    testCube = wholeCube(
            dataIndices, edgeDataIndices, axesData,
            createNewCubyDataTest(
                    3, 0.8696, 0.0652,
                    # topRightCorner positions
                    (1.4348,1.4348,1.5),
                    # colors

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
    )

    # Final Rubik's Cube
    """
    testCube = wholeCube(
            dataIndices, edgeDataIndices, axesData,
            createNewCubyData(
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
    )
    """
    # And finally the Mainloop()
    glut.glutMainLoop()
