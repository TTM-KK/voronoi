# coding: utf-8
import Rhino
import scriptcontext
import rhinoscriptsyntax as rs
import Tetrahedron
import Point


points_obj_list = []  # Pointのオブジェクトを保持。
divide_tetrahedron_list = []  # このリストに三角形分割を保持していく。[p1, p2, p3]


# Rhino上の点群を取得し座標値を取得。
points = rs.GetObjects('select points to use 3D Delaunay', rs.filter.point)

for i in range(len(points)):
    point = Point.Point(points[i])
    point.system_guid_obj_to_coordinate()

    points_obj_list.append(point)


# ドロネー分割の前準備。
# はじめの外接円を構成する点のインスタンス作成。この範囲内に点群を収めておく必要あり。
P1 = Point.Point([0, 0, 800])
P1.change_coordinate()
P2 = Point.Point([0, 1000, -200])
P2.change_coordinate()
P3 = Point.Point([866.025, -500, -200])
P3.change_coordinate()
P4 = Point.Point([-866.025, -500, -200])
P4.change_coordinate()

tetrahedron = Tetrahedron.Tetrahedron(P1, P2, P3, P4)
tetrahedron.cul_center_p_and_radius()
divide_tetrahedron_list.append(tetrahedron)


# ドロネー分割のメインアルゴリズム
# for _ in range(len(points_obj_list)):
for _ in range(len(points_obj_list)):

    # 追加するポイントの選択。
    select_point = points_obj_list.pop(0)

    # 三角形の外接円内に追加したポイントが内包されていないか判定。内包されている場合はindexを保存。
    temp_divide_tetrahedron = []
    count = 0
    for i in range(len(divide_tetrahedron_list)):
        tri = divide_tetrahedron_list[i + count]
        check = tri.check_point_include_circumsphere(select_point)
        # print('chcek', check)
        if check:
            # 内包していた三角形の頂点を使用して再分割する。
            new_tetrahedron1 = Tetrahedron.Tetrahedron(tri.p1, tri.p2, tri.p3, select_point)
            new_tetrahedron2 = Tetrahedron.Tetrahedron(tri.p1, tri.p2, tri.p4, select_point)
            new_tetrahedron3 = Tetrahedron.Tetrahedron(tri.p1, tri.p3, tri.p4, select_point)
            new_tetrahedron4 = Tetrahedron.Tetrahedron(tri.p2, tri.p3, tri.p4, select_point)
            new_tetrahedron1.cul_center_p_and_radius()
            new_tetrahedron2.cul_center_p_and_radius()
            new_tetrahedron3.cul_center_p_and_radius()
            new_tetrahedron4.cul_center_p_and_radius()

            temp_divide_tetrahedron.append(new_tetrahedron1)
            temp_divide_tetrahedron.append(new_tetrahedron2)
            temp_divide_tetrahedron.append(new_tetrahedron3)
            temp_divide_tetrahedron.append(new_tetrahedron4)

            del divide_tetrahedron_list[i + count]
            count = count - 1
        else:
            pass

    # 重複している三角形を削除

    del_instances = []
    for tetra in temp_divide_tetrahedron:
        for tetra_check in temp_divide_tetrahedron:
            if tetra == tetra_check:
                continue
            if tetra.radius == tetra_check.radius and tetra.center_p == tetra_check.center_p:
                del_instances.append(tetra_check)
                del_instances.append(tetra)

    for del_instance in del_instances:
        if del_instance in temp_divide_tetrahedron:
            del temp_divide_tetrahedron[temp_divide_tetrahedron.index(del_instance)]

    # 重複三角形を削除した後にappend
    divide_tetrahedron_list.extend(temp_divide_tetrahedron)


# はじめに作成した四面体の母点をもつ四面体分割を削除
# del_instances = []
# for tetra_check in divide_tetrahedron_list:
#     if tetra_check.p1 == P1 or tetra_check.p1 == P2 or tetra_check.p1 == P3 or \
#             tetra_check.p1 == P4 or tetra_check.p2 == P1 or tetra_check.p2 == P2 or \
#             tetra_check.p2 == P3 or tetra_check.p2 == P4 or tetra_check.p3 == P1 or \
#             tetra_check.p3 == P2 or tetra_check.p3 == P3 or tetra_check.p3 == P4 or \
#             tetra_check.p4 == P1 or tetra_check.p4 == P2 or tetra_check.p4 == P3 or \
#             tetra_check.p4 == P4:
#         del_instances.append(tetra_check)
#
# for del_instance in del_instances:
#     if del_instance in divide_tetrahedron_list:
#         del divide_tetrahedron_list[divide_tetrahedron_list.index(del_instance)]


# ドロネー描画
for i in range(len(divide_tetrahedron_list)):
    divide_tetrahedron_list[i].draw_divide_tetrahedron()


# ボロノイ分割。
# for i in range(len(divide_tetrahedron_list)):
#     tri_1 = divide_tetrahedron_list[i]
#     for j in range(len(divide_tetrahedron_list)):
#         if i == j:
#             continue
#         tri_2 = divide_tetrahedron_list[j]
#
#         count = 0
#         if tri_1.p1 == tri_2.p1 or tri_1.p1 == tri_2.p2 or tri_1.p1 == tri_2.p3 or tri_1.p1 == tri_2.p4:
#             count += 1
#         if tri_1.p2 == tri_2.p1 or tri_1.p2 == tri_2.p2 or tri_1.p2 == tri_2.p3 or tri_1.p2 == tri_2.p4:
#             count += 1
#         if tri_1.p3 == tri_2.p1 or tri_1.p3 == tri_2.p2 or tri_1.p3 == tri_2.p3 or tri_1.p3 == tri_2.p4:
#             count += 1
#         if tri_1.p4 == tri_2.p1 or tri_1.p4 == tri_2.p2 or tri_1.p4 == tri_2.p3 or tri_1.p4 == tri_2.p4:
#             count += 1
#
#         if count == 3:
#             line = Rhino.Geometry.Line(tri_1.center_p[0], tri_1.center_p[1], tri_1.center_p[2], tri_2.center_p[0],
#                                        tri_2.center_p[1], tri_2.center_p[2])
#             scriptcontext.doc.Objects.AddLine(line)
