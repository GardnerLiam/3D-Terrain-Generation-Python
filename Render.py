'''
@Author: Liam Gardner
@Date: 5/9/2019
'''
import noise
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Vector(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)


# def map(value, istart, istop, ostart, ostop):
#     return ostart + (ostop - ostart) * (value - istart) / (istop - istart)


scale = 15.0

height_scale = 15

octaves = 5
octaveOffsets = []

persistence = 0.5
lacunarity = 2

flattening_threshold = 0.0125

for i in range(octaves):
    octaveOffsets.append(Vector(np.random.randint(-10000, 10000), np.random.randint(-10000, 10000)))

terrain_size = 150

terrain = []
for y in range(terrain_size):
    terrain.append([])
    for x in range(terrain_size):
        terrain[-1].append(0)

for y in range(terrain_size):
    for x in range(terrain_size):
        amplitude = 1
        frequency = 1
        noiseHeight = 0
        for i in range(octaves):
            sampleX = frequency * (x + octaveOffsets[i].x) / scale
            sampleY = frequency * (y + octaveOffsets[i].y) / scale
            noiseHeight += amplitude * noise.pnoise2(sampleX, sampleY)
            amplitude *= persistence
            frequency *= lacunarity
        terrain[x][y] = noiseHeight

min_val = np.min(terrain)
max_val = np.max(terrain)

# for y in range(terrain_size):
#     for x in range(terrain_size):
#         terrain[x][y] = map(terrain[x][y], min_val, max_val, 0, 1)

terrain = np.array(terrain)
np.clip(terrain, -0.71, max_val)
terrain_max = np.max(terrain)
color_heights = [-0.7078, -0.6518, -0.5057, -0.27, -0.07, 0.1765, 0.3725, 0.5686, 0.9608]
for i in color_heights:
    print(i)


def initGL():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glShadeModel(GL_SMOOTH)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


def getColor(value):
    global color_heights
    if value < color_heights[0]:
        return 42 / 255.0, 93 / 255.0, 186 / 255.0
    elif color_heights[0] <= value < color_heights[1]:
        return 51 / 255.0, 102 / 255.0, 195 / 255.0
    elif color_heights[1] <= value < color_heights[2]:
        return 207 / 255.0, 215 / 255.0, 127 / 255.0
    elif color_heights[2] <= value < color_heights[3]:
        return 91 / 255.0, 169 / 255.0, 24 / 255.0
    elif color_heights[3] <= value < color_heights[4]:
        return 63 / 255.0, 119 / 255.0, 17 / 255.0
    elif color_heights[4] <= value < color_heights[5]:
        return 89 / 255.0, 68 / 255.0, 61 / 255.0
    elif color_heights[5] <= value < color_heights[6]:
        return 74 / 255.0, 59 / 255.0, 55 / 255.0
    elif color_heights[6] <= value < color_heights[7]:
        return 250 / 255.0, 250 / 255.0, 250 / 255.0
    elif value >= color_heights[7]:
        return 1, 1, 1


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(-terrain_size / 2.0, -25, -6)
    glRotate(60, -1, 0, 0)
    glBegin(GL_TRIANGLES)
    for y in range(1, terrain_size - 1):
        for x in range(1, terrain_size - 1):
            if terrain[x][y + 1] < flattening_threshold:
                color = getColor(terrain[x][y + 1])
                glColor3f(color[0], color[1], color[2])
                glVertex(x, (y + 1), 0)
            else:
                color = getColor(terrain[x][y + 1])
                glColor3f(color[0], color[1], color[2])
                glVertex3f(x, (y + 1), (terrain[x][y + 1] * height_scale))

            if terrain[x][y] < flattening_threshold:
                color = getColor(terrain[x][y])
                glColor3f(color[0], color[1], color[2])
                glVertex3f(x, y, 0)

            else:
                color = getColor(terrain[x][y])
                glColor3f(color[0], color[1], color[2])
                glVertex3f(x, y, (terrain[x][y] * height_scale))

            if terrain[x + 1][y + 1] < flattening_threshold:
                color = getColor(terrain[x + 1][y + 1])
                glColor3f(color[0], color[1], color[2])
                glVertex3f((x + 1), (y + 1), 0)
            else:
                color = getColor(terrain[x + 1][y + 1])
                glColor3f(color[0], color[1], color[2])
                glVertex3f((x + 1), (y + 1), (terrain[x + 1][y + 1] * height_scale))
    glEnd()

    glBegin(GL_TRIANGLES)
    for y in range(1, terrain_size - 1):
        for x in range(1, terrain_size - 1):
            if terrain[x + 1][y + 1] < flattening_threshold:
                color = getColor(terrain[x + 1][y + 1])
                glColor3f(color[0], color[1], color[2])
                glVertex3f((x + 1), (y + 1), 0)
            else:
                color = getColor(terrain[x + 1][y + 1])
                glColor3f(color[0], color[1], color[2])
                glVertex3f((x + 1), (y + 1), (terrain[x + 1][y + 1] * height_scale))

            if terrain[x + 1][y] < flattening_threshold:
                color = getColor(terrain[x + 1][y])
                glColor3f(color[0], color[1], color[2])
                glVertex3f((x + 1), y, 0)
            else:
                color = getColor(terrain[x + 1][y])
                glColor3f(color[0], color[1], color[2])
                glVertex3f((x + 1), y, (terrain[x + 1][y] * height_scale))

            if terrain[x][y] < flattening_threshold:
                color = getColor(terrain[x][y])
                glColor3f(color[0], color[1], color[2])
                glVertex3f(x, y, 0)
            else:
                color = getColor(terrain[x][y])
                glColor3f(color[0], color[1], color[2])
                glVertex3f(x, y, (terrain[x][y] * height_scale))
    glEnd()
    glutSwapBuffers()


def reshape(width, height):
    if height == 0:
        height = 1
    aspect = width / height

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0, aspect, 0.1, 100.0)


if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(50, 50)
    glutCreateWindow("3D Terrain")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    initGL()
    glutMainLoop()
