# coding: utf-8
import Rhino
import scriptcontext
import rhinoscriptsyntax as rs
import time

from voronoi_module import Triangle
from voronoi_module import Point
from voronoi_module import Voronoi
from voronoi_module import Delaunay
from convexhull_module import ConvexHull

from GA import Generator


points_obj_list = []  # Pointのオブジェクトを保持。
delaunay_triangles = []  # このリストに三角形分割を保持していく。[p1, p2, p3]
original_points = []  # TODO とりあえずの応急処置。Pointクラスインスタンスを保持するリストを作成し、Triangleクラスは各Pointクラスインスタンスのインデックスを参照するようにする。

# GAに関するパラメーター
each_generation_gene_list = []
generation_num = 10
pop_num = 50

# 選択のパラメータ
tournament_size = 10
tournament_select_num = 2
elite_select_num = 1

# 交叉の確率
crossover_prob = 50

# 突然変異の確率
mutation_prob = 3


# Rhino上の点群を取得し座標値を取得。
# points = rs.GetObjects('select points to use Delaunay', rs.filter.point)
points = Generator.generator(50)
print(points)

for point in points:
    rs.AddPoint(point)

# Time Start
t_start = time.time()

for i in range(len(points)):
    point = Point.Point(points[i])
    point.change_coordinate()
    # point.system_guid_obj_to_coordinate()
    points_obj_list.append(point)
    original_points.append(point)


# 初期遺伝子リスト
gene = [original_point.coordinate for original_point in original_points]
each_generation_gene_list.append(gene)

# ドロネー分割を行う。
delaunay = Delaunay.Delaunay()
delaunay.points_to_delaunay(points_obj_list)
# delaunay.draw_delaunay()


# ボロノイ図を作成。各領域のインスタンスを取得。
voronoi = Voronoi.Voronoi()
voronoi.delaunay_to_voronoi(original_points, delaunay.each_triangles)


# 2Dの凸包図形作成。
original_points_coordinate = [point.coordinate for point in original_points]
convexhull_points = ConvexHull.convex_hull(original_points_coordinate)
convexhull_line = ConvexHull.make_line(convexhull_points)
ConvexHull.draw_rhino(convexhull_points)


# 凸包図形を使用してボロノイをトリミング
voronoi.rebuild_voronoi_by_convexhull(convexhull_line)
voronoi.reculculate_voronoi_area()
voronoi.draw_voronoi()


# Time Fin
t_fin = time.time()
print('Fin Time : {}'.format(t_fin - t_start))
