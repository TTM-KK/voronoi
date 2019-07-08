# coding: utf-8
import math
import Rhino
import scriptcontext


class Triangle:

    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.radius = None
        self.center_p = None

    def cul_center_coordinate_and_radius(self):
        '''任意の3点の外接円の中心と半径を取得。'''

        # 外接円の中心点を計算
        c = 2 * ((self.p2.x - self.p1.x)*(self.p3.y - self.p1.y) - (self.p2.y - self.p1.y)*(self.p3.x - self.p1.x))

        x = ((self.p3.y - self.p1.y)*(pow(self.p2.x, 2) - pow(self.p1.x, 2) + pow(self.p2.y, 2) - pow(self.p1.y, 2)) +
             (self.p1.y - self.p2.y)*(pow(self.p3.x, 2) - pow(self.p1.x, 2) + pow(self.p3.y, 2) - pow(self.p1.y, 2))) / c

        y = ((self.p1.x - self.p3.x)*(pow(self.p2.x, 2) - pow(self.p1.x, 2) + pow(self.p2.y, 2) - pow(self.p1.y, 2)) +
             (self.p2.x - self.p1.x)*(pow(self.p3.x, 2) - pow(self.p1.x, 2) + pow(self.p3.y, 2) - pow(self.p1.y, 2))) / c

        self.center_p = [x, y, 0]

        # 外接円の半径を計算
        radius = math.sqrt(pow((self.p1.x - self.center_p[0]), 2) + pow((self.p1.y - self.center_p[1]), 2))
        self.radius = radius

    def draw_triangle(self):
        '''分割三角形をRhinoに描画するためのメソッド'''
        line1 = Rhino.Geometry.Line(self.p1.x, self.p1.y, self.p1.z, self.p2.x, self.p2.y, self.p2.z)
        line2 = Rhino.Geometry.Line(self.p1.x, self.p1.y, self.p1.z, self.p3.x, self.p3.y, self.p3.z)
        line3 = Rhino.Geometry.Line(self.p2.x, self.p2.y, self.p2.z, self.p3.x, self.p3.y, self.p3.z)
        scriptcontext.doc.Objects.AddLine(line1)
        scriptcontext.doc.Objects.AddLine(line2)
        scriptcontext.doc.Objects.AddLine(line3)

    def check_point_include_circumscribed_circle(self, check_p):
        '''外接円に任意の点が内包されているかどうか判定'''

        distance = math.sqrt(pow((check_p.x - self.center_p[0]), 2) + pow((check_p.y - self.center_p[1]), 2))

        if distance < self.radius:
            return True
        else:
            return False


