# platonic solids

from math import sqrt, pi, sin, cos


class PlatoSolids:
    sqrt2 = sqrt(2)
    X = 0.525731112119133606
    Z = 0.850650808352039932
    pi2 = pi * 2

    geoObject = {  # format: 'object' (faces, coords)
        'cube': ([[3, 0, 1, 2], [3, 4, 5, 0], [0, 5, 6, 1],
                  [1, 6, 7, 2], [2, 7, 4, 3], [5, 4, 7, 6]],
                 [[1, 1, 1], [-1, 1, 1], [-1, -1, 1],
                  [1, -1, 1], [1, -1, -1], [1, 1, -1],
                  [-1, 1, -1], [-1, -1, -1]]
                 ),
        'tetrahedron': ([[0, 1, 2], [0, 2, 3], [0, 3, 1], [1, 3, 2]],
                        [[0, 0, 1.732051],
                         [1.632993, 0, -0.5773503],
                         [-0.8164966, sqrt2, -0.5773503],
                         [-0.8164966, -sqrt2, -0.5773503]]
                        ),
        'octahedron': ([[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 1],
                        [1, 4, 5], [1, 5, 2], [2, 5, 3], [3, 5, 4]],
                       [[0, 0, 1.414], [1.414, 0, 0],
                        [0, 1.414, 0], [-1.414, 0, 0],
                        [0, -1.414, 0], [0, 0, -1.414]]),
        'icosahedron': ([[0, 4, 1], [0, 9, 4], [9, 5, 4], [4, 5, 8],
                         [4, 8, 1], [8, 10, 1], [8, 3, 10], [5, 3, 8],
                         [5, 2, 3], [2, 7, 3], [7, 10, 3], [7, 6, 10],
                         [7, 11, 6], [11, 0, 6], [0, 1, 6], [6, 1, 10],
                         [9, 0, 11], [9, 11, 2], [9, 2, 5], [7, 2, 11]],
                        [[-X, 0.0, Z], [X, 0.0, Z], [-X, 0.0, -Z],
                         [X, 0.0, -Z], [0.0, Z, X], [0.0, Z, -X],
                         [0.0, -Z, X], [0.0, -Z, -X], [Z, X, 0.0],
                         [-Z, X, 0.0], [Z, -X, 0.0], [-Z, -X, 0.0]]),
        'dodecahedron': ([[0, 1, 4, 7, 2], [0, 2, 6, 9, 3], [0, 3, 8, 5, 1],
                          [1, 5, 11, 10, 4], [2, 7, 13, 12, 6], [3, 9, 15, 14, 8],
                          [4, 10, 16, 13, 7], [5, 8, 14, 17, 11], [6, 12, 18, 15, 9],
                          [10, 11, 17, 19, 16], [12, 13, 16, 19, 18], [14, 15, 18, 19, 17]],
                         [[0, 0, 1.07047], [0.713644, 0, 0.797878], [-0.356822, 0.618, 0.797878],
                          [-0.356822, -0.618, 0.797878], [0.797878, 0.618034, 0.356822], [0.797878, -0.618, 0.356822],
                          [-0.934172, 0.381966, 0.356822], [0.136294, 1., 0.356822], [0.136294, -1., 0.356822],
                          [-0.934172, -0.381966, 0.356822], [0.934172, 0.381966, -0.356822],
                          [0.934172, -0.381966, -0.356822],
                          [-0.797878, 0.618, -0.356822], [-0.136294, 1., -0.356822], [-0.136294, -1., -0.356822],
                          [-0.797878, -0.618034, -0.356822], [0.356822, 0.618, -0.797878],
                          [0.356822, -0.618, -0.797878],
                          [-0.713644, 0, -0.797878], [0, 0, -1.07047]]),
        'sphere': ()

    }
    text_coords = None

    def __init__(self):
        self.text_coords = {i: self.texture_polygon(i) for i in (3, 4, 5)}  # generate dict texture coords 3,4,5
        self.geoObject['sphere'] = self.sphere_coords()  # add sphere

    def texture_polygon(self, n: int) -> list:
        def _a(i): return n / 2 - i

        pi2n = self.pi2 / n
        return [[0.5 * sin(_a(i) * pi2n) + 0.5,
                 0.5 * cos(_a(i) * pi2n) + 0.5] for i in range(n)]

    def partialname(self, name):
        pn = [key for key in self.geoObject.keys() if key.startswith(name)]
        return pn[0] if pn else []

    def _draw(self, gl, mode, graph_object='cube'):  # gl.GL_LINE_LOOP
        f, c = self.geoObject[self.partialname(graph_object)]
        for face in f:
            gl.glBegin(mode)
            for nf, ci in enumerate(face):
                if self.text_coords is not None and mode == gl.GL_TRIANGLE_FAN:  # textures coords
                    gl.glTexCoord2fv(self.text_coords[len(face)][nf])  # common polygon face textures
                gl.glVertex3fv(c[ci])
            gl.glEnd()

    def draw(self, gl, type='wire', graph_object='cube'):  # gl.GL_LINE_LOOP
        if self.partialname(graph_object) == 'sphere':
            self.draw_sphere(gl, type)
        else:
            self._draw(gl, mode=gl.GL_TRIANGLE_FAN if type == 'solid' else gl.GL_LINE_LOOP, graph_object=graph_object)

    def draw_sphere(self, gl, type='wire'):
        c, f, t = self.geoObject['sphere']

        mode = gl.GL_QUADS if type == 'solid' else gl.GL_LINE_LOOP

        for face in f:
            gl.glBegin(mode)
            for ci in face:
                if type == 'solid': gl.glTexCoord2fv(t[ci])
                gl.glVertex3fv(c[ci])
            gl.glEnd()

    def sphere_coords(self, sec=50, rad=1.):

        coords, faces, texture = [], [], []

        for r in range(sec + 1):  # coords & textures
            v = r / sec
            theta1 = v * pi
            xn, yn, zn = 0, 1, 0
            cosry, sinry = cos(theta1), sin(theta1)
            xt, yt, zt = -(yn * sinry), +(yn * cosry), 0
            xn, yn, zn = xt, yt, zt

            for c in range(sec + 1):
                u = c / sec
                theta2 = u * self.pi2
                x, y, z = xn, yn, zn

                cosry, sinry = cos(theta2), sin(theta2)
                xt, zt = (x * cosry) + (z * sinry), (x * -sinry) + (z * cosry)
                x, z = xt, zt

                coords += [[x * rad, y * rad, z * rad]]
                texture += [[u, v]]

        cl = sec + 1  # faces
        for r in range(sec):
            off = r * cl
            faces += [[off + c, off + c + 1, off + (c + 1 + cl), off + (c + 0 + cl)] for c in range(sec)]

        return coords, faces, texture
