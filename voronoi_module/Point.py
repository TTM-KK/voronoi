# coding: utf-8
import rhinoscriptsyntax as rs


class Point:
    def __init__(self, point):
        self.point = point
        self.x = None
        self.y = None
        self.z = None
        self.coordinate = None

    def system_guid_obj_to_coordinate(self):
        '''System.GuidObjectをRhino.Objectに変換。クラス変数に座標値を保持させる'''

        p = rs.coerce3dpoint(self.point)
        self.x = p[0]
        self.y = p[1]
        self.z = p[2]
        self.coordinate = [p[0], p[1], p[2]]

    def change_coordinate(self):
        '''はじめの外接円を構成する点を変換するメソッド'''

        p = self.point
        self.x = p[0]
        self.y = p[1]
        self.z = p[2]
        self.coordinate = [p[0], p[1], p[2]]
