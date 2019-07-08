# coding: utf-8
# import Rhino
# import scriptcontext
# import rhinoscriptsyntax as rs
import time

from voronoi_module import Triangle
from voronoi_module import Point
from voronoi_module import Voronoi
from voronoi_module import Delaunay
from convexhull_module import ConvexHull

from GA import Generator
from GA import Evaluate
from GA import Selection
from GA import Crossover
from GA import Mutation


points_obj_list = []  # Pointのオブジェクトを保持。
delaunay_triangles = []  # このリストに三角形分割を保持していく。[p1, p2, p3]
original_points = []  # TODO とりあえずの応急処置。Pointクラスインスタンスを保持するリストを作成し、Triangleクラスは各Pointクラスインスタンスのインデックスを参照するようにする。

# GAに関するパラメーター
each_generation_optimize_gene = []
each_generation_optimize_evaluation_value = []


generation_num = 2
pop_num = 1
x_range = 2000
y_range = 2000

# 選択のパラメータ
tournament_size = 10
tournament_select_num = 2
elite_select_num = 1

# 交叉の確率
crossover_prob = 50

# 突然変異の確率
mutation_prob = 3


def save_optimize_pop(all_pop, evaluate_value):
    '''優良個体の評価値と遺伝子配列をリターン'''
    max_value = max(evaluate_value)
    max_index = evaluate_value.index(max_value)
    superior_pop = all_pop[max_index]

    return max_value, superior_pop


def draw_result(pop, loop):
    points_obj_list = []
    original_points = []
    for point in pop:
        p = Point.Point(point)
        p.change_coordinate()
        points_obj_list.append(p)
        original_points.append(p)

    # ドロネー分割を行う。
    delaunay = Delaunay.Delaunay()
    delaunay.points_to_delaunay(points_obj_list)
    # delaunay.draw_delaunay()

    # ボロノイ図を作成。各領域のインスタンスを取得。
    voronoi = Voronoi.Voronoi()
    voronoi.delaunay_to_voronoi(original_points, delaunay.each_triangles)
    voronoi.draw_voronoi()

    # 2Dの凸包図形作成。
    original_points_coordinate = [point.coordinate for point in original_points]
    convexhull_points = ConvexHull.convex_hull(original_points_coordinate)
    # convexhull_line = ConvexHull.make_line(convexhull_points)
    ConvexHull.draw_rhino(convexhull_points)

    # 凸包図形を使用してボロノイをトリミング
    # voronoi.rebuild_voronoi_by_convexhull(convexhull_line)
    # voronoi.reculculate_voronoi_area()
    # voronoi.draw_voronoi_loop(loop, x_range)


# Time Start
t_start = time.time()

# 初期個体生成
all_pop = []
for i in range(pop_num):
    points = Generator.generator(10, x_range, y_range)
    all_pop.append(points)


# 初期評価
evaluate_value = Evaluate.evaluate(all_pop)
max_value, superior = save_optimize_pop(all_pop, evaluate_value)
each_generation_optimize_evaluation_value.append(int(max_value))
each_generation_optimize_gene.append(superior)

#
# for loop in range(generation_num):
#     # 選択
#     select_pop, elite_pop = Selection.selection(
#         all_pop, evaluate_value, tournament_select_num, tournament_size, elite_select_num, ascending=True)
#
#     # 選択した個体の中から2個体選択し交叉や突然変異を適用する。
#     next_pop = []
#     while True:
#         # 交叉
#         pop_1, pop_2 = Crossover.one_point_crossover(select_pop, crossover_prob)
#         # 突然変異
#         # pop_1 = mutation(pop_1, mutation_prob)
#         # pop_2 = mutation(pop_2, mutation_prob)
#
#         next_pop.append(pop_1)
#         next_pop.append(pop_2)
#
#         if len(next_pop) >= pop_num - elite_select_num:
#             break
#
#     # エリート主義。優良個体を次世代へ継承。
#     next_pop.extend(elite_pop)
#
#     # 評価
#     evaluate_value = Evaluate.evaluate(next_pop, loop=loop + 1)
#     max_value, superior = save_optimize_pop(all_pop, evaluate_value)
#     each_generation_optimize_evaluation_value.append(int(max_value))
#     each_generation_optimize_gene.append(superior)
#
#     # 更新
#     all_pop = next_pop
#
#

# 結果をRhinoに描画
# loop = 0
# for each_pop_gene in each_generation_optimize_gene:
#     draw_result(each_pop_gene, loop)
#     loop += 1

# for i in range(len(points)):
#     point = Point.Point(points[i])
#     point.change_coordinate()
#
#     points_obj_list.append(point)
#     original_points.append(point)
#
#
# # ドロネー分割を行う。
# delaunay = Delaunay.Delaunay()
# delaunay.points_to_delaunay(points_obj_list)
# # delaunay.draw_delaunay()
#
#
# # ボロノイ図を作成。各領域のインスタンスを取得。
# voronoi = Voronoi.Voronoi()
# voronoi.delaunay_to_voronoi(original_points, delaunay.each_triangles)
#
#
# # 2Dの凸包図形作成。
# original_points_coordinate = [point.coordinate for point in original_points]
# convexhull_points = ConvexHull.convex_hull(original_points_coordinate)
# convexhull_line = ConvexHull.make_line(convexhull_points)
# ConvexHull.draw_rhino(convexhull_points)
#
#
# # 凸包図形を使用してボロノイをトリミング
# voronoi.rebuild_voronoi_by_convexhull(convexhull_line)
# voronoi.reculculate_voronoi_area()
# voronoi.draw_voronoi()
#
#
# # 遺伝的アルゴリズム開始。


# Time Fin
t_fin = time.time()
print('Evaluate Value : {}'.format(each_generation_optimize_evaluation_value))
print('Fin Time : {}'.format(t_fin - t_start))
