# coding: utf-8
from voronoi_module import Point
from voronoi_module import Voronoi
from voronoi_module import Delaunay
from convexhull_module import ConvexHull


def evaluate(all_pop, loop=0):
    """ ユークリッド距離の総和を計算し評価値とする。 """

    evaluate_value = []
    for pop in all_pop:
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

        # ボロノイ図を作成。各領域のインスタンスを取得。
        voronoi = Voronoi.Voronoi()
        voronoi.delaunay_to_voronoi(original_points, delaunay.each_triangles)
        # voronoi.draw_voronoi()

        # 2Dの凸包図形作成。
        original_points_coordinate = [point.coordinate for point in original_points]
        convexhull_points = ConvexHull.convex_hull(original_points_coordinate)
        convexhull_line = ConvexHull.make_line(convexhull_points)
        ConvexHull.draw_rhino(convexhull_points)

        # 凸包図形を使用してボロノイをトリミング
        voronoi.rebuild_voronoi_by_convexhull_2(convexhull_line)
        voronoi.reculculate_voronoi_area()
        voronoi.draw_voronoi()

        # 面積マックスの値を個体の評価値とする。
        voronoi_area_list = []
        for each_voronoi in voronoi.each_voronoi_instances:
            voronoi_area_list.append(each_voronoi.area)

        max_area = max(voronoi_area_list)

        evaluate_value.append(max_area)

    # 一番優秀な個体遺伝子をreturn
    # excellent_evaluate_value = max(evaluate_value)
    # draw_pop_index = evaluate_value.index(excellent_evaluate_value)
    #
    # show_route(position_info, all_route[draw_pop_index],int(excellent_evaluate_value), loop=loop + 1)

    return evaluate_value
