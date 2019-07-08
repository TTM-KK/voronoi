# coding: utf-8
import Rhino
import scriptcontext
import rhinoscriptsyntax as rs
import Tetrahedron
import Point

crv = rs.GetObject('select crv', rs.filter.curve)
voronoi_line = rs.GetObject('select crv', rs.filter.curve)

crv = [rs.CurveStartPoint(crv), rs.CurveEndPoint(crv)]
voronoi_line = [rs.CurveStartPoint(voronoi_line), rs.CurveEndPoint(voronoi_line)]


a_1 = (crv[1][1] - crv[0][1]) / (crv[1][0] - crv[0][0])
b_1 = ((crv[0][1] * crv[1][0]) - (crv[1][1] * crv[0][0])) / (crv[1][0] - crv[0][0])

if crv[0][0] > crv[1][0]:
    x_1 = crv[1][0]
    x_2 = crv[0][0]
else:
    x_1 = crv[0][0]
    x_2 = crv[1][0]

if crv[0][1] > crv[1][1]:
    y_1 = crv[1][1]
    y_2 = crv[0][1]
else:
    y_1 = crv[0][1]
    y_2 = crv[1][1]


a_2 = (voronoi_line[1][1] - voronoi_line[0][1]) / (voronoi_line[1][0] - voronoi_line[0][0])
b_2 = ((voronoi_line[0][1] * voronoi_line[1][0]) - (voronoi_line[1][1] * voronoi_line[0][0])) / (voronoi_line[1][0] - voronoi_line[0][0])


intersect_point_x = (b_2 - b_1) / (a_1 - a_2)  # 傾きが同じだとまずい。
intersect_point_y = ((a_1 * b_2) - (a_2 * b_1)) / (a_1 - a_2)

if voronoi_line[0][0] > voronoi_line[1][0]:
    x_3 = voronoi_line[1][0]
    x_4 = voronoi_line[0][0]
else:
    x_3 = voronoi_line[0][0]
    x_4 = voronoi_line[1][0]

if voronoi_line[0][1] > voronoi_line[1][1]:
    y_3 = voronoi_line[1][1]
    y_4 = voronoi_line[0][1]
else:
    y_3 = voronoi_line[0][1]
    y_4 = voronoi_line[1][1]

intersect_flag_count = 0
if (x_1 < intersect_point_x) and (intersect_point_x < x_2):
    intersect_flag_count += 1
else:
    print('not intersect 1')
if (x_3 < intersect_point_x) and (intersect_point_x < x_4):
    intersect_flag_count += 1
else:
    print('not intersect 2')
if (y_1 < intersect_point_y) and (intersect_point_y < y_2):
    intersect_flag_count += 1
else:
    print('not intersect 3')
if (y_3 < intersect_point_y) and (intersect_point_y < y_4):
    intersect_flag_count += 1
else:
    print('not intersect 4')

if intersect_flag_count == 4:
    print('y1 : {} y2 : {}'.format(y_1, y_2))
    print('y3 : {} y4 : {}'.format(y_3, y_4))
    print('intersect_point : {}'.format(intersect_point_y))

