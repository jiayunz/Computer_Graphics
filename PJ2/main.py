from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import PIL.Image as Image

texture_file = 'texture.jpg'

def get_light():
    glShadeModel(GL_SMOOTH)
    # 制定光源位置
    glLightfv(GL_LIGHT0, GL_POSITION, [-.5, .5, 1.5, 1.])
    # 设置材质对各种光的反光率
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1., 1., 1., 1.])
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_COLOR_MATERIAL)

def bind_texture(filename):
    # 读取材质贴图
    img = Image.open(filename)
    img = np.asarray(img, dtype=np.uint8)
    # 生成纹理
    texture = glGenTextures(1)
    # 将texture纹理绑定到GL_TEXTURE_2D纹理目标上
    glBindTexture(GL_TEXTURE_2D, texture)
    # 纹理坐标超出边界时，采用GL_REPEAT
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # 绘制图像大于或小于贴图尺寸时，采用GL_NEAREST
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    # 定义材质图片
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.shape[0], img.shape[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)


def draw_board():
    # 设置立方体顶点、面、坐标
    vertices = [
        [-.4, -.4, 0],
        [.4, -.4, 0],
        [.4, .4, 0],
        [-.4, .4, 0],
        [-.4, -.4, -.1],
        [.4, -.4, -.1],
        [.4, .4, -.1],
        [-.4, .4, -.1]
    ]
    coords = [
        [0., 0.],
        [1., 0.],
        [1., 1.],
        [0., 1.],
        [0., 0.],
        [1., 0.],
        [1., 1.],
        [0., 1.]
    ]
    faces = [
        [0, 1, 2, 3],
        [2, 6, 7, 3],
        [0, 3, 7, 4],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [1, 2, 6, 5]
    ]

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()

    glMatrixMode(GL_MODELVIEW)
    # 旋转角度
    glRotatef(20., 0., 1., 0.)
    glRotatef(20., 0., 0., 0.)

    # 绘制3个显示的面
    glBegin(GL_QUADS)
    # 前
    glNormal3f(0.0, 0.0, 1.0)
    for f in faces[0]:
        glTexCoord2fv(coords[f])
        glVertex3fv(vertices[f])
    # 上
    glNormal3f(0.0, 1.0, 0.0)
    for f in faces[1]:
        glTexCoord2fv(coords[f])
        glVertex3fv(vertices[f])
    # 左
    glNormal3f(-1.0, 0.0, 0.0)
    for f in faces[2]:
        glTexCoord2fv(coords[f])
        glVertex3fv(vertices[f])
    glEnd()

    glPopMatrix()
    glFlush()

if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(500, 500)
    glutCreateWindow("real board")
    get_light()
    bind_texture(texture_file)
    glutDisplayFunc(draw_board)
    glutMainLoop()
