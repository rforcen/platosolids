'''
draw cropcircles in svg part files
'''

import sys
from os.path import join

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QOpenGLTexture, QImage
from PyQt5.QtWidgets import (QApplication, QMainWindow)

from platosolids import PlatoSolids
from rendererGL import RendererGL


class TextureWidget(RendererGL):
    ps = PlatoSolids()

    resource_path = 'rsc'
    texture_file = 'indalo.jpg'

    texture = None
    zoom = -5
    ang = 0

    def __init__(self):
        super(TextureWidget, self).__init__()
        self.setFocusPolicy(Qt.StrongFocus)  # accepts key events

        timer = QTimer(self)
        timer.timeout.connect(self.onTimer)
        timer.start(20)

    def init(self, gl):
        self.texture = QOpenGLTexture(QImage(join(self.resource_path, self.texture_file)).mirrored())

    def draw(self, gl):
        def drawTextures():
            gl.glEnable(gl.GL_TEXTURE_2D)
            self.texture.bind()
            self.ps.draw(gl, 'solid', 'dodeca')
            # self.ps.draw(gl,'solid', 'sphere')

        gl.glRotatef(self.ang, 1, 1, 1)

        drawTextures()

    def onTimer(self):
        self.ang += 0.6
        self.repaint()


class Main(QMainWindow):
    def __init__(self, *args):
        super(Main, self).__init__(*args)

        self.cc = TextureWidget()

        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle('texture sample ')

        self.setCentralWidget(self.cc)
        self.show()

    def keyPressEvent(self, event):
        if event.key() < 256:
            ch = chr(event.key()).lower()
            if ch == 'q':
                exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = Main()

    exit(app.exec_())
