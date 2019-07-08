# coding: utf-8
import math
import scriptcontext
import Rhino


class Tetrahedron:

    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.radius = None
        self.center_p = None

    def cul_center_p_and_radius(self):
        '''外接球の中心点と半径を計算'''

        a = [
            [self.p1.x, self.p1.y, self.p1.z, 1],
            [self.p2.x, self.p2.y, self.p2.z, 1],
            [self.p3.x, self.p3.y, self.p3.z, 1],
            [self.p4.x, self.p4.y, self.p4.z, 1]
        ]

        d_x = [
            [pow(self.p1.x, 2) + pow(self.p1.y, 2) + pow(self.p1.z, 2), self.p1.y, self.p1.z, 1],
            [pow(self.p2.x, 2) + pow(self.p2.y, 2) + pow(self.p2.z, 2), self.p2.y, self.p2.z, 1],
            [pow(self.p3.x, 2) + pow(self.p3.y, 2) + pow(self.p3.z, 2), self.p3.y, self.p3.z, 1],
            [pow(self.p4.x, 2) + pow(self.p4.y, 2) + pow(self.p4.z, 2), self.p4.y, self.p4.z, 1]
        ]

        d_y = [
            [pow(self.p1.x, 2) + pow(self.p1.y, 2) + pow(self.p1.z, 2), self.p1.x, self.p1.z, 1],
            [pow(self.p2.x, 2) + pow(self.p2.y, 2) + pow(self.p2.z, 2), self.p2.x, self.p2.z, 1],
            [pow(self.p3.x, 2) + pow(self.p3.y, 2) + pow(self.p3.z, 2), self.p3.x, self.p3.z, 1],
            [pow(self.p4.x, 2) + pow(self.p4.y, 2) + pow(self.p4.z, 2), self.p4.x, self.p4.z, 1]
        ]

        d_z = [
            [pow(self.p1.x, 2) + pow(self.p1.y, 2) + pow(self.p1.z, 2), self.p1.x, self.p1.y, 1],
            [pow(self.p2.x, 2) + pow(self.p2.y, 2) + pow(self.p2.z, 2), self.p2.x, self.p2.y, 1],
            [pow(self.p3.x, 2) + pow(self.p3.y, 2) + pow(self.p3.z, 2), self.p3.x, self.p3.y, 1],
            [pow(self.p4.x, 2) + pow(self.p4.y, 2) + pow(self.p4.z, 2), self.p4.x, self.p4.y, 1]
        ]

        a = dit_4(a)
        d_x = dit_4(d_x)
        d_y = -(dit_4(d_y))
        d_z = dit_4(d_z)

        center_p_x = d_x / (2 * a)
        center_p_y = d_y / (2 * a)
        center_p_z = d_z / (2 * a)

        self.center_p = [float(center_p_x), float(center_p_y), float(center_p_z)]

        distance = math.sqrt(
            pow((self.p1.x - self.center_p[0]), 2) + pow((self.p1.y - self.center_p[1]), 2) + pow((self.p1.z - self.center_p[2]), 2))

        self.radius = float(distance)

    def draw_divide_tetrahedron(self):
        '''分割四面体をRhinoに描画するためのメソッド'''
        line1 = Rhino.Geometry.Line(self.p1.x, self.p1.y, self.p1.z, self.p2.x, self.p2.y, self.p2.z)
        line2 = Rhino.Geometry.Line(self.p1.x, self.p1.y, self.p1.z, self.p3.x, self.p3.y, self.p3.z)
        line3 = Rhino.Geometry.Line(self.p1.x, self.p1.y, self.p1.z, self.p4.x, self.p4.y, self.p4.z)
        line4 = Rhino.Geometry.Line(self.p2.x, self.p2.y, self.p2.z, self.p3.x, self.p3.y, self.p3.z)
        line5 = Rhino.Geometry.Line(self.p2.x, self.p2.y, self.p2.z, self.p4.x, self.p4.y, self.p4.z)
        line6 = Rhino.Geometry.Line(self.p3.x, self.p3.y, self.p3.z, self.p4.x, self.p4.y, self.p4.z)

        scriptcontext.doc.Objects.AddLine(line1)
        scriptcontext.doc.Objects.AddLine(line2)
        scriptcontext.doc.Objects.AddLine(line3)
        scriptcontext.doc.Objects.AddLine(line4)
        scriptcontext.doc.Objects.AddLine(line5)
        scriptcontext.doc.Objects.AddLine(line6)

    def check_point_include_circumsphere(self, check_p):
        '''外接球に任意の点が内包されているかどうか判定'''

        distance = math.sqrt(pow((check_p.x - self.center_p[0]), 2) + pow(
            (check_p.y - self.center_p[1]), 2) + pow((check_p.z - self.center_p[2]), 2))

        if distance < self.radius:
            return True
        else:
            return False


def dit_2(dit):
    '''二次元行列の計算'''
    cul = (dit[0][0] * dit[1][1]) - (dit[0][1] * dit[1][0])

    return cul


def dit_3(dit):
    '''三次行列の計算'''
    a = [
        [dit[1][1], dit[1][2]],
        [dit[2][1], dit[2][2]]
    ]

    b = [
        [dit[0][1], dit[0][2]],
        [dit[2][1], dit[2][2]]
    ]

    c = [
        [dit[0][1], dit[0][2]],
        [dit[1][1], dit[1][2]]
    ]

    cul = (dit[0][0] * dit_2(a)) - (dit[1][0] * dit_2(b)) + (dit[2][0] * dit_2(c))

    return cul


def dit_4(dit):
    '''4次元の行列'''
    a = [
        [dit[1][1], dit[1][2], dit[1][3]],
        [dit[2][1], dit[2][2], dit[2][3]],
        [dit[3][1], dit[3][2], dit[3][3]]
    ]

    b = [
        [dit[0][1], dit[0][2], dit[0][3]],
        [dit[2][1], dit[2][2], dit[2][3]],
        [dit[3][1], dit[3][2], dit[3][3]]
    ]

    c = [
        [dit[0][1], dit[0][2], dit[0][3]],
        [dit[1][1], dit[1][2], dit[1][3]],
        [dit[3][1], dit[3][2], dit[3][3]]
    ]

    d = [
        [dit[0][1], dit[0][2], dit[0][3]],
        [dit[1][1], dit[1][2], dit[1][3]],
        [dit[2][1], dit[2][2], dit[2][3]]
    ]

    cul = (dit[0][0] * dit_3(a)) - (dit[1][0] * dit_3(b)) + (dit[2][0] * dit_3(c)) - (dit[3][0] * dit_3(d))

    return cul
