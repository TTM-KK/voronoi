# coding: utf-8

from . Point import Point
from . Triangle import Triangle


class Delaunay:
    def __init__(self):
        self.each_triangles = None
        self.original_point = None

    def points_to_delaunay(self, points):

        delaunay_triangles = []
        self.original_point = points

        p_1 = Point([-1000000, -1000000, 0])
        p_1.change_coordinate()
        p_2 = Point([1000000, -1000000, 0])
        p_2.change_coordinate()
        p_3 = Point([0, 730000, 0])
        p_3.change_coordinate()

        triangle = Triangle(p_1, p_2, p_3)
        triangle.cul_center_coordinate_and_radius()
        delaunay_triangles.append(triangle)

        for _ in range(len(points)):

            # 追加するポイントの選択。
            select_point = points.pop(0)

            # 三角形の外接円内に追加したポイントが内包されていないか判定。内包されている場合はindexを保存。
            temp_divide_triangle = []
            count = 0
            for i in range(len(delaunay_triangles)):
                tri = delaunay_triangles[i + count]
                check = tri.check_point_include_circumscribed_circle(select_point)
                if check:
                    # 内包していた三角形の頂点を使用して再分割する。
                    new_triangle1 = Triangle(tri.p1, tri.p2, select_point)
                    new_triangle2 = Triangle(tri.p2, tri.p3, select_point)
                    new_triangle3 = Triangle(tri.p1, tri.p3, select_point)
                    new_triangle1.cul_center_coordinate_and_radius()
                    new_triangle2.cul_center_coordinate_and_radius()
                    new_triangle3.cul_center_coordinate_and_radius()

                    temp_divide_triangle.append(new_triangle1)
                    temp_divide_triangle.append(new_triangle2)
                    temp_divide_triangle.append(new_triangle3)

                    del delaunay_triangles[i + count]
                    count = count - 1
                else:
                    pass

            # 重複している三角形を削除
            _count = 0
            for i in range(len(temp_divide_triangle)):
                triangle_check1 = temp_divide_triangle[i + _count]

                flag_del = False
                count = 0
                for j in range(len(temp_divide_triangle)):
                    if j <= i + _count:
                        continue
                    if len(temp_divide_triangle) - 1 < j + count:
                        break

                    triangle_check2 = temp_divide_triangle[j + count]
                    if triangle_check1.center_p == triangle_check2.center_p:
                        del temp_divide_triangle[j + count]
                        count = count - 1
                        flag_del = True

                if flag_del:
                    del temp_divide_triangle[i + _count]
                    _count = _count - 1

                if len(temp_divide_triangle) - 2 < i + _count:
                    break

            # 重複三角形を削除した後にappend
            delaunay_triangles.extend(temp_divide_triangle)

        self.each_triangles = delaunay_triangles

    def draw_delaunay(self):
        for triangle in self.each_triangles:
            triangle.draw_triangle()
