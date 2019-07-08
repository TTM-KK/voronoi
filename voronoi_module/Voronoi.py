# coding: utf-8
import rhinoscriptsyntax as rs
import Rhino
import scriptcontext
import math
import copy


class Voronoi:
    def __init__(self):
        self.each_voronoi_instances = None
        self.original_point = None
        self.delaunay_triangle = None
        self.center_coordinate = [1000, 1000, 0]

    def delaunay_to_voronoi(self, original_point, delaunay_triangles):
        '''
        ドロネー三角分割の三角形からボロノイを作成。個々のインスタンスも作成する。
        :param original_point:
        :param delaunay_triangles:
        :return: voronoi_instances 各ボロノイ領域のインスタンス。
        '''
        voronoi_instances = []
        for point in original_point:
            have_common_p_triangle = []
            for triangle in delaunay_triangles:
                if triangle.p1 == point or triangle.p2 == point or triangle.p3 == point:
                    have_common_p_triangle.append(triangle)

            # 共有点を持つ三角形を使用してボロノイ図形を作成する。
            voronoi_lines = []
            for i in range(len(have_common_p_triangle)):
                tri_1 = have_common_p_triangle[0]
                for tri_2 in have_common_p_triangle:
                    if tri_1 == tri_2:
                        continue

                    count = 0
                    if tri_1.p1 == tri_2.p1 or tri_1.p1 == tri_2.p2 or tri_1.p1 == tri_2.p3:
                        count += 1
                    if tri_1.p2 == tri_2.p1 or tri_1.p2 == tri_2.p2 or tri_1.p2 == tri_2.p3:
                        count += 1
                    if tri_1.p3 == tri_2.p1 or tri_1.p3 == tri_2.p2 or tri_1.p3 == tri_2.p3:
                        count += 1

                    if count == 2:
                        # TODO RhinoCommonで隠蔽する必要あり。
                        line = [[tri_1.center_p[0], tri_1.center_p[1], tri_1.center_p[2]],
                                [tri_2.center_p[0], tri_2.center_p[1], tri_2.center_p[2]]]

                        voronoi_lines.append(line)

                del have_common_p_triangle[0]

            # ボロノイを解析するためのインスタンス作成。初期メソッドの実行
            voronoi_instance = VoronoiEach(voronoi_lines)
            voronoi_instance.cul_voronoi_area()
            voronoi_instance.voronoi_point = point.coordinate
            voronoi_instances.append(voronoi_instance)

        self.each_voronoi_instances = voronoi_instances

    def draw_voronoi(self):
        for voronoi_each in self.each_voronoi_instances:
            voronoi_each.draw_voronoi()

    def draw_voronoi_loop(self, loop, xrange):
        for voronoi_each in self.each_voronoi_instances:
            voronoi_each.draw_voronoi_loop(loop, xrange)

    def rebuild_voronoi_by_convexhull(self, convexhull_crvs):

        # for con in convexhull_crvs:
        #     rs.AddLine(con[0], con[1])

        # ひとつひとつのボロノイ領域に対して順に計算していく。
        for voronoi_each in self.each_voronoi_instances:
            # 凸包とボロノイ領域を構成する線の交点の有無を計算
            # [intersect_point_list, intersect_crv_list, intersect_convex_crv_list, flag_one_crv]
            results = voronoi_each.crv_crv_intersection_trim(convexhull_crvs)

            # for point in intersect_point_list:
            #     rs.AddPoint(point)
            # for inter_crv in intersect_crv_list:
            #     rs.AddLine(inter_crv[0], inter_crv[1])
            # for inter_con in intersect_convex_crv_list:
            #     rs.AddLine(inter_con[0], inter_con[1])

            # 交点の有無を利用して再構成。
            result_count = -1
            for result in results:
                result_count += 1

                if not result[0]:
                    pass
                else:
                    if result[3] is True:  # 一片の凸包を構成する線分で、ボロノイが分割されている場合。

                        for j in range(len(result[1])):
                            intersect_voronoi_crv = result[1][j]
                            intersect_point = result[0][j]

                            # 以下の２点の内外判定を行う。両方が外に出ている場合は条件分岐が異なる。
                            out_count = 0
                            count = 0
                            for convex_crv in convexhull_crvs:
                                re = self.intersection(convex_crv, [intersect_voronoi_crv[0], [10000, 0, 0]])
                                if re is True:
                                    count += 1
                            if count == 1:
                                pass
                            else:
                                out_count += 1

                            count = 0
                            for convex_crv in convexhull_crvs:
                                re = self.intersection(convex_crv, [intersect_voronoi_crv[1], [10000, 0, 0]])
                                if re is True:
                                    count += 1
                            if count == 1:
                                pass
                            else:
                                out_count += 1

                            if out_count == 2:
                                flag_break = False
                                for k in range(len(results)):
                                    if k == result_count:
                                        continue

                                    for l in range(len(results[k][1])):
                                        print(intersect_voronoi_crv)
                                        print(result[k][1][l])
                                        if intersect_voronoi_crv[0] == results[k][1][l][0] or intersect_voronoi_crv[0] == results[k][1][l][1]:
                                            print('check')
                                            if intersect_voronoi_crv[1][0] == results[k][1][l][0] or intersect_voronoi_crv[1][0] == results[k][1[l]][1]:
                                                print('OK')
                                                preserve_point = results[k][0][l]
                                                flag_break = True
                                                break
                                    if flag_break is True:
                                        break

                                for i in range(len(voronoi_each.voronoi_lines)):
                                    if voronoi_each.voronoi_lines[i] == intersect_voronoi_crv:
                                        voronoi_each.voronoi_lines[i] = [intersect_point, preserve_point]
                                        print('voronoi_p', voronoi_each.voronoi_lines[i])
                                        break
                                    else:
                                        continue

                            else:


                                # インターセクションを使用して、どちら側をトリムするか決定する。
                                crv_1 = [intersect_voronoi_crv[0], self.center_coordinate]
                                crv_2 = [intersect_voronoi_crv[1], self.center_coordinate]

                                intersect_check_1 = self.intersection(result[2][0], crv_1)
                                intersect_check_2 = self.intersection(result[2][0], crv_2)

                                if intersect_check_1[0] is True:
                                    preserve_point = intersect_voronoi_crv[1]
                                elif intersect_check_2[0] is True:
                                    preserve_point = intersect_voronoi_crv[0]
                                else:
                                    raise Exception('something strange')

                                # rs.AddPoint(preserve_point)

                                # ボロノイ線をトリムのイメージで再構成する。
                                for i in range(len(voronoi_each.voronoi_lines)):
                                    if voronoi_each.voronoi_lines[i] == intersect_voronoi_crv:
                                        if voronoi_each.voronoi_lines[i][0] == preserve_point:
                                            voronoi_each.voronoi_lines[i] = [preserve_point, intersect_point]
                                        else:
                                            voronoi_each.voronoi_lines[i] = [intersect_point, preserve_point]
                                    else:
                                        continue

                        # 新しくできたボロノイを構成する線を追加。
                        voronoi_each.voronoi_lines.append([result[0][0], result[0][1]])

                    else:
                        pass
                        # for j in range(len(result[1])):
                        #     intersect_voronoi_crv = result[1][j]
                        #     intersect_point = result[0][j]
                        #
                        #     # インターセクションを使用して、どちら側をトリムするか決定する。
                        #
                        #     # crv_1 = [intersect_crv[0], inner_voronoi[0].voronoi_point]
                        #     crv_1 = [intersect_voronoi_crv[0], self.center_coordinate]
                        #     crv_2 = [intersect_voronoi_crv[1], self.center_coordinate]
                        #
                        #     intersect_check_1 = False
                        #     for convexhull_crv in convexhull_crvs:
                        #         intersect_check_1 = self.intersection(convexhull_crv, crv_1)
                        #         if intersect_check_1[0] is True:
                        #             break
                        #         else:
                        #             continue
                        #
                        #     intersect_check_2 = False
                        #     for convexhull_crv in convexhull_crvs:
                        #         intersect_check_2 = self.intersection(convexhull_crv, crv_2)
                        #         if intersect_check_2[0] is True:
                        #             break
                        #         else:
                        #             continue
                        #
                        #     if intersect_check_1[0] is True:
                        #         preserve_point = intersect_voronoi_crv[1]
                        #     elif intersect_check_2[0] is True:
                        #         preserve_point = intersect_voronoi_crv[0]
                        #     else:
                        #         raise Exception('something strange')
                        #
                        #     rs.AddPoint(preserve_point)
                        #     # rs.AddPoint(intersect_point)
                        #
                        #     # elif intersect_check_2[0] is True:
                        #     #     preserve_point = intersect_crv[0]
                        #
                        #     # ボロノイ線をトリムのイメージで再構成する。
                        #     for i in range(len(voronoi_each.voronoi_lines)):
                        #         if voronoi_each.voronoi_lines[i] == intersect_voronoi_crv:
                        #             if voronoi_each.voronoi_lines[i][0] == preserve_point:
                        #                 voronoi_each.voronoi_lines[i] = [preserve_point, intersect_point]
                        #             else:
                        #                 voronoi_each.voronoi_lines[i] = [intersect_point, preserve_point]
                        #         else:
                        #             continue
                        #
                        # # 新しくできたボロノイを構成する線を追加。
                        # if len(result[0]) == 2:
                        #     voronoi_each.voronoi_lines.append([result[0][0], voronoi_each.voronoi_point])
                        #     voronoi_each.voronoi_lines.append([result[0][1], voronoi_each.voronoi_point])
                        # else:
                        #     voronoi_each.voronoi_lines.append([result[0][0], voronoi_each.voronoi_point])

            count = 0
            index = 0
            while True:
                line = voronoi_each.voronoi_lines[index]
                p_1 = line[0]
                p_2 = line[1]

                flag_1 = False
                flag_2 = False
                for voronoi_line in voronoi_each.voronoi_lines:
                    if line == voronoi_line:
                        continue

                    if p_1 in voronoi_line:
                        flag_1 = True
                    if p_2 in voronoi_line:
                        flag_2 = True

                    if flag_1 and flag_2:
                        break

                if not flag_1 or not flag_2:
                    del voronoi_each.voronoi_lines[index]
                    index = 0
                    count = 0
                else:
                    count += 1
                    index += 1

                if count >= len(voronoi_each.voronoi_lines) - 1:
                    break

    def rebuild_voronoi_by_convexhull_2(self, convexhull_crvs):
        for voronoi_each in self.each_voronoi_instances:
            # 凸包とボロノイ領域を構成する線の交点の有無を計算
            # [intersect_point_list, intersect_voronoi_crvs_list, convexhull_merge_point]
            results = voronoi_each.crv_crv_intersection_trim_2(convexhull_crvs)
            for loop in range(len(results)):

                # ２つの凸包を構成する辺がボロノイ領域を分割している場合。
                # print(results[loop][2])

                # # print('check 00')
                # #
                # # 一辺のボロノイ辺が交点を２つ保持している場合。
                if len(results[loop][0]) == 2:
                    print('check 01')
                    for j in range(len(voronoi_each.voronoi_lines)):
                        if voronoi_each.voronoi_lines[j] == results[loop][1][0]:
                            pass
                        else:
                            continue

                        print('result_3', results[loop][3])
                        print('point', voronoi_each.voronoi_point)
                        # rs.AddPoint(voronoi_each.voronoi_point)

                        # ボテンが凸包の外側にあるかどうかの判定。
                        if voronoi_each.voronoi_point in results[loop][3][0] or voronoi_each.voronoi_point in results[loop][3][1]:
                            print('voronoi_point IN')
                            new_point_1 = results[loop][0][0]
                            new_point_2 = results[loop][0][1]


                            voronoi_each.voronoi_lines[j] = [new_point_1, new_point_2]
                            voronoi_each.voronoi_lines.append([new_point_1, voronoi_each.voronoi_point])
                            voronoi_each.voronoi_lines.append([new_point_2, voronoi_each.voronoi_point])
                        else:

                            new_point_1 = results[loop][0][0]
                            new_point_2 = results[loop][0][1]
                            if new_point_1[0] < new_point_2[0]:
                                pass
                            else:
                                new_point_1, new_point_2 = new_point_2, new_point_1

                            non_preserve_point_1 = results[loop][1][0][0]
                            non_preserve_point_2 = results[loop][1][0][1]

                            if non_preserve_point_1[0] < non_preserve_point_2[0]:
                                pass
                            else:
                                a = non_preserve_point_1
                                b = non_preserve_point_2
                                non_preserve_point_1 = b
                                non_preserve_point_2 = a

                            print('non1', non_preserve_point_1)
                            print('non2', non_preserve_point_2)

                            for i in range(len(results)):
                                if i == loop:
                                    continue

                                if non_preserve_point_1 == results[i][1][0][1] or non_preserve_point_1 == results[i][1][0][0]:
                                    if len(results[i][0]) == 1:
                                        get_point = results[i][0][0]
                                        rs.AddPoint(get_point)
                                    else:
                                        raise Exception('Error')

                                    voronoi_each.voronoi_lines.append([get_point, new_point_1])
                                    print('check_non 01')

                                if non_preserve_point_2 == results[i][1][0][0] or non_preserve_point_2 == results[i][1][0][1]:
                                    if len(results[i][0]) == 1:
                                        get_point = results[i][0][0]
                                        rs.AddPoint(get_point)
                                    else:
                                        raise Exception('Error')

                                    voronoi_each.voronoi_lines.append([get_point, new_point_2])
                                    print('check_non 02')

                            # 一度の生成で十分。
                            voronoi_each.voronoi_lines[j] = [new_point_1, new_point_2]

                        break
                    break

                # １つの凸包を構成する辺がボロノイ領域を分割している場合。
                elif len(results[loop][0]) == 1:

                    # 共有のボロノイ辺を保有しているか判定。 TODO 個々を拡張する必要あり。
                    if len(results) - 1 == loop:
                        pass
                    else:
                        if results[loop][3][0] == results[loop + 1][3][0]:
                            flag_straight = True
                        else:
                            flag_straight = False

                    # 内外判定。どちらの端点を残すかを決定する。
                    print('check 03')
                    print(results[loop][1][0][0])

                    include_flag = self.point_include(convexhull_crvs, results[loop][1][0][0])
                    print('include', include_flag)
                    if include_flag is True:

                        preserve_point_1 = results[loop][1][0][0]
                        new_point_1 = results[loop][0][0]

                        rs.AddPoint(preserve_point_1)

                        for j in range(len(voronoi_each.voronoi_lines)):
                            if voronoi_each.voronoi_lines[j] == results[loop][1][0]:

                                if flag_straight is True:
                                    voronoi_each.voronoi_lines[j] = [new_point_1, preserve_point_1]
                                    if loop == len(results) - 1:
                                        voronoi_each.voronoi_lines[j] = [new_point_1, preserve_point_1]
                                    else:
                                        voronoi_each.voronoi_lines.append([new_point_1, results[loop + 1][0][0]])
                                        voronoi_each.voronoi_lines[j] = [new_point_1, preserve_point_1]
                                else:
                                    voronoi_each.voronoi_lines[j] = [new_point_1, preserve_point_1]
                                    voronoi_each.voronoi_lines.append([new_point_1, voronoi_each.voronoi_point])

                                break
                            else:
                                pass

                    elif include_flag is False:

                        preserve_point_1 = results[loop][1][0][1]
                        new_point_1 = results[loop][0][0]

                        for j in range(len(voronoi_each.voronoi_lines)):
                            if voronoi_each.voronoi_lines[j] == results[loop][1][0]:

                                if flag_straight is True:
                                    voronoi_each.voronoi_lines[j] = [new_point_1, preserve_point_1]
                                    if loop == len(results) - 1:
                                        flag_straight = False
                                        voronoi_each.voronoi_lines[j] = [new_point_1, preserve_point_1]
                                    else:
                                        voronoi_each.voronoi_lines.append([new_point_1, results[loop + 1][0][0]])
                                        voronoi_each.voronoi_lines[j] = [new_point_1, preserve_point_1]
                                else:
                                    voronoi_each.voronoi_lines[j] = [new_point_1, preserve_point_1]
                                    voronoi_each.voronoi_lines.append([new_point_1, voronoi_each.voronoi_point])
                                break
                            else:
                                pass

                    else:
                        raise Exception('Error')

                    # self.rebuid_other_end_point(non_preserve_point_1, non_preserve_point_2, preserve_point_1,
                    #                                 new_point_1, new_point_2, voronoi_each)
                else:
                    raise Exception('Error')

    def rebuid_other_end_point(self, non_pre_p_1, non_pre_p_2, pre_p, new_p_1, new_p_2, voronoi_each):
        if non_pre_p_2 is None:
            if new_p_2 is None:
                for i in range(len(voronoi_each.voronoi_lines)):
                    # 保存しない点を保持しているボロノイ辺を探し、新しく使用する点に置き換える。
                    if voronoi_each.voronoi_lines[i][0] == non_pre_p_1:
                        voronoi_each.voronoi_lines[i] = [voronoi_each.voronoi_lines[i][1], new_p_1]

                    elif voronoi_each.voronoi_lines[i][1] == non_pre_p_1:
                        voronoi_each.voronoi_lines[i] = [voronoi_each.voronoi_lines[i][0], new_p_1]
                    else:
                        pass

                        # raise Exception('Error')
            else:
                raise Exception('Error')

        elif pre_p is None:
            if new_p_1[0] > new_p_2[0]:
                new_p_1, new_p_2 = new_p_2, new_p_1

            if non_pre_p_1[0] > non_pre_p_2[0]:
                non_pre_p_1, non_pre_p_2 = non_pre_p_2, non_pre_p_1

            if non_pre_p_1 > new_p_1 or new_p_2 > non_pre_p_2:
                raise Exception('Error')

            for i in range(len(voronoi_each.voronoi_lines)):
                # 保存しない点を保持しているボロノイ辺を探し、新しく使用する点に置き換える その１。
                if voronoi_each.voronoi_lines[i][0] == non_pre_p_1:
                    voronoi_each.voronoi_lines[i] = [voronoi_each.voronoi_lines[i][1], new_p_1]

                elif voronoi_each.voronoi_lines[i][1] == non_pre_p_1:
                    voronoi_each.voronoi_lines[i] = [voronoi_each.voronoi_lines[i][0], new_p_1]
                else:
                    # print('check', voronoi_each.voronoi_lines[i][0])
                    # raise Exception('Error')
                    pass

            for i in range(len(voronoi_each.voronoi_lines)):
                # 保存しない点を保持しているボロノイ辺を探し、新しく使用する点に置き換える　その２。
                if voronoi_each.voronoi_lines[i][0] == non_pre_p_2:
                    voronoi_each.voronoi_lines[i] = [voronoi_each.voronoi_lines[i][1], new_p_2]

                elif voronoi_each.voronoi_lines[i][1] == non_pre_p_1:
                    voronoi_each.voronoi_lines[i] = [voronoi_each.voronoi_lines[i][0], new_p_2]
                else:
                    # raise Exception('Error')
                    pass

        else:
            raise Exception('Error')

    def point_include(self, curves, point):
        count = 0
        for curve in curves:
            result = self.intersection(curve, [point, [100000, 0, 0]])
            if result[0] is True:
                count += 1

        if count == 1:
            return True

        elif count == 2 or count == 0:
            return False

        else:
            raise Exception('Something Happen')



    def distance(self, p1, p2):
        distance = math.sqrt(pow((p1[0] - p2[0]), 2) + pow((p1[1] - p2[1]), 2))
        return distance

    def intersection(self, crv1, crv2):

        a_1 = (crv1[1][1] - crv1[0][1]) / (crv1[1][0] - crv1[0][0])
        b_1 = ((crv1[0][1] * crv1[1][0]) - (crv1[1][1] * crv1[0][0])) / (crv1[1][0] - crv1[0][0])

        if crv1[0][0] > crv1[1][0]:
            x_1 = crv1[1][0]
            x_2 = crv1[0][0]
        else:
            x_1 = crv1[0][0]
            x_2 = crv1[1][0]

        if crv1[0][1] > crv1[1][1]:
            y_1 = crv1[1][1]
            y_2 = crv1[0][1]
        else:
            y_1 = crv1[0][1]
            y_2 = crv1[1][1]

        a_2 = (crv2[1][1] - crv2[0][1]) / (crv2[1][0] - crv2[0][0])
        b_2 = ((crv2[0][1] * crv2[1][0]) - (crv2[1][1] * crv2[0][0])) / (crv2[1][0] - crv2[0][0])

        if crv2[0][0] > crv2[1][0]:
            x_3 = crv2[1][0]
            x_4 = crv2[0][0]
        else:
            x_3 = crv2[0][0]
            x_4 = crv2[1][0]

        if crv2[0][1] > crv2[1][1]:
            y_3 = crv2[1][1]
            y_4 = crv2[0][1]
        else:
            y_3 = crv2[0][1]
            y_4 = crv2[1][1]

        intersect_point_x = (b_2 - b_1) / (a_1 - a_2)
        intersect_point_y = ((a_1 * b_2) - (a_2 * b_1)) / (a_1 - a_2)

        intersection_flag = False
        intersect_flag_count = 0
        if (x_1 <= intersect_point_x) and (intersect_point_x <= x_2):
            intersect_flag_count += 1

        if (x_3 <= intersect_point_x) and (intersect_point_x <= x_4):
            intersect_flag_count += 1

        if (y_1 <= intersect_point_y) and (intersect_point_y <= y_2):
            intersect_flag_count += 1

        if (y_3 <= intersect_point_y) and (intersect_point_y <= y_4):
            intersect_flag_count += 1

        if intersect_flag_count == 4:
            intersection_flag = True
            intersection_point = [intersect_point_x, intersect_point_y, 0]
            # rs.AddPoint(intersection_point)
        else:
            intersection_point = []

        return intersection_flag, intersection_point

    def intersection_trim(self, crv1, crv2):

        a_1 = (crv1[1][1] - crv1[0][1]) / (crv1[1][0] - crv1[0][0])
        b_1 = ((crv1[0][1] * crv1[1][0]) - (crv1[1][1] * crv1[0][0])) / (crv1[1][0] - crv1[0][0])

        if crv1[0][0] > crv1[1][0]:
            x_1 = crv1[1][0]
            x_2 = crv1[0][0]
        else:
            x_1 = crv1[0][0]
            x_2 = crv1[1][0]

        if crv1[0][1] > crv1[1][1]:
            y_1 = crv1[1][1]
            y_2 = crv1[0][1]
        else:
            y_1 = crv1[0][1]
            y_2 = crv1[1][1]

        a_2 = (crv2[1][1] - crv2[0][1]) / (crv2[1][0] - crv2[0][0])
        b_2 = ((crv2[0][1] * crv2[1][0]) - (crv2[1][1] * crv2[0][0])) / (crv2[1][0] - crv2[0][0])

        if crv2[0][0] > crv2[1][0]:
            x_3 = crv2[1][0]
            x_4 = crv2[0][0]
        else:
            x_3 = crv2[0][0]
            x_4 = crv2[1][0]

        if crv2[0][1] > crv2[1][1]:
            y_3 = crv2[1][1]
            y_4 = crv2[0][1]
        else:
            y_3 = crv2[0][1]
            y_4 = crv2[1][1]

        intersect_point_x = (b_2 - b_1) / (a_1 - a_2)
        intersect_point_y = ((a_1 * b_2) - (a_2 * b_1)) / (a_1 - a_2)

        intersection_flag = False
        intersect_flag_count = 0
        if (x_1 <= intersect_point_x) and (intersect_point_x <= x_2):
            intersect_flag_count += 1

        if (x_3 <= intersect_point_x) and (intersect_point_x <= x_4):
            intersect_flag_count += 1

        if (y_1 <= intersect_point_y) and (intersect_point_y <= y_2):
            intersect_flag_count += 1

        if (y_3 <= intersect_point_y) and (intersect_point_y <= y_4):
            intersect_flag_count += 1

        if intersect_flag_count == 4:
            intersection_flag = True
            intersection_point = [intersect_point_x, intersect_point_y, 0]
            rs.AddPoint(intersection_point)
        else:
            intersection_point = []

        return intersection_flag, intersection_point

    def reculculate_voronoi_area(self):
        for voronoi in self.each_voronoi_instances:
            voronoi.cul_voronoi_area()


class VoronoiEach():
    def __init__(self, voronoi_line):
        self.voronoi_lines = voronoi_line  # それぞれのボロノイを構成する線が２点の座標値がリスト形式で格納されている。
        self.area = None
        self.voronoi_point = None  # ボロノイの母点

    def cul_voronoi_area(self):
        '''ボロノイの面積を計算する。'''

        # 端点を重複なく順に抽出。
        coordinate_list = []
        count = 0
        for _ in range(len(self.voronoi_lines)):
            if count == 0:
                line = self.voronoi_lines[0]
                start = line[0]
                end = line[1]
                count += 1

            for line_check in self.voronoi_lines:
                if line == line_check:
                    continue

                if line_check[0] == end:
                    start = line_check[0]
                    end = line_check[1]
                    line = line_check
                    break
                elif line_check[1] == end:
                    start = line_check[1]
                    end = line_check[0]
                    line = line_check
                    break

            coordinate_list.append(start)

        # 端点を使用し、面積を計算。
        sum_list = []
        for i in range(len(coordinate_list)):
            if i == len(coordinate_list) - 1:
                p_1 = coordinate_list[i]
                p_2 = coordinate_list[0]
            else:
                p_1 = coordinate_list[i]
                p_2 = coordinate_list[i + 1]

            cross = (p_1[0] * p_2[1]) - (p_1[1] * p_2[0])  # 外積計算
            sum_list.append(cross)

        area = abs(sum(sum_list)) / 2

        self.area = area

    def show_area(self):
        return self.area

    def draw_voronoi(self):
        for line in self.voronoi_lines:
            rs.AddLine(line[0], line[1])

    def draw_voronoi_loop(self, loop, xrange):
        '''Rhinoに描画。X方向に重ならないように描画する。'''
        crvs = []
        for line in self.voronoi_lines:
            # line[0][0] = line[0][0] + (xrange*2*loop)
            # line[1][0] = line[1][0] + (xrange*2*loop)
            crv = Rhino.Geometry.Line(line[0][0], line[0][1], line[0][2], line[1][0], line[1][1], line[1][2])
            crvs.append(crv)

        for crv in crvs:
            scriptcontext.doc.Objects.AddLine(crv)

    def crv_crv_intersection_trim(self, curves):
        result = []
        for crv in curves:
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

            one_crv_count = 0  # 凸包を構成する１つの辺でボロノイが切り取られているかを判定する。
            intersect_count = 0
            intersect_point_list = []
            intersect_crv_list = []
            intersect_convex_crv_list = []
            for voronoi_line in self.voronoi_lines:

                a_2 = (voronoi_line[1][1] - voronoi_line[0][1]) / (voronoi_line[1][0] - voronoi_line[0][0])
                b_2 = ((voronoi_line[0][1] * voronoi_line[1][0]) - (voronoi_line[1][1] * voronoi_line[0][0])) / (voronoi_line[1][0] - voronoi_line[0][0])

                # 傾きが同じだということは重なっているということなのでスキップ
                # if a_1 - a_2 == 0:
                #     continue

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
                if (x_1 <= intersect_point_x) and (intersect_point_x <= x_2):
                    intersect_flag_count += 1

                if (x_3 <= intersect_point_x) and (intersect_point_x <= x_4):
                    intersect_flag_count += 1

                if (y_1 <= intersect_point_y) and (intersect_point_y <= y_2):
                    intersect_flag_count += 1

                if (y_3 <= intersect_point_y) and (intersect_point_y <= y_4):
                    intersect_flag_count += 1

                if intersect_flag_count == 4:
                    # print('y1 : {} y2 : {}'.format(y_1, y_2))
                    # print('y3 : {} y4 : {}'.format(y_3, y_4))
                    # print('intersect_point : {}'.format(intersect_point_y))
                    intersect_count += 1
                    one_crv_count += 1
                    intersect_point_list.append([intersect_point_x, intersect_point_y, 0])
                    intersect_crv_list.append(voronoi_line)
                    intersect_convex_crv_list.append(crv)

            if intersect_count == 2 and one_crv_count == 2:
                flag_one_crv = True
                result.append([intersect_point_list, intersect_crv_list, intersect_convex_crv_list, flag_one_crv])
            elif intersect_count >= 1:
                flag_one_crv = False
                result.append([intersect_point_list, intersect_crv_list, intersect_convex_crv_list, flag_one_crv])

        return result

    def crv_crv_intersection_trim_2(self, convexhull_crvs):
        result = []
        for voronoi_line in self.voronoi_lines:
            a_1 = (voronoi_line[1][1] - voronoi_line[0][1]) / (voronoi_line[1][0] - voronoi_line[0][0])
            b_1 = ((voronoi_line[0][1] * voronoi_line[1][0]) - (voronoi_line[1][1] * voronoi_line[0][0])) / (voronoi_line[1][0] - voronoi_line[0][0])

            if voronoi_line[0][0] > voronoi_line[1][0]:
                x_1 = voronoi_line[1][0]
                x_2 = voronoi_line[0][0]
            else:
                x_1 = voronoi_line[0][0]
                x_2 = voronoi_line[1][0]

            if voronoi_line[0][1] > voronoi_line[1][1]:
                y_1 = voronoi_line[1][1]
                y_2 = voronoi_line[0][1]
            else:
                y_1 = voronoi_line[0][1]
                y_2 = voronoi_line[1][1]

            intersect_point_list = []
            intersect_voronoi_crvs_list = []
            convexhull_merge_point = []

            temp_convexhull_list = []
            for convexhull_crv in convexhull_crvs:

                a_2 = (convexhull_crv[1][1] - convexhull_crv[0][1]) / (convexhull_crv[1][0] - convexhull_crv[0][0])
                b_2 = ((convexhull_crv[0][1] * convexhull_crv[1][0]) - (convexhull_crv[1][1] * convexhull_crv[0][0])) / (
                            convexhull_crv[1][0] - convexhull_crv[0][0])

                # 傾きが同じだということは重なっているということなのでスキップ
                # if a_1 - a_2 == 0:
                #     continue

                intersect_point_x = (b_2 - b_1) / (a_1 - a_2)  # 傾きが同じだとまずい。
                intersect_point_y = ((a_1 * b_2) - (a_2 * b_1)) / (a_1 - a_2)

                if convexhull_crv[0][0] > convexhull_crv[1][0]:
                    x_3 = convexhull_crv[1][0]
                    x_4 = convexhull_crv[0][0]
                else:
                    x_3 = convexhull_crv[0][0]
                    x_4 = convexhull_crv[1][0]

                if convexhull_crv[0][1] > convexhull_crv[1][1]:
                    y_3 = convexhull_crv[1][1]
                    y_4 = convexhull_crv[0][1]
                else:
                    y_3 = convexhull_crv[0][1]
                    y_4 = convexhull_crv[1][1]

                # インターセクトを判定。
                intersect_flag_count = 0
                if (x_1 <= intersect_point_x) and (intersect_point_x <= x_2):
                    intersect_flag_count += 1

                if (x_3 <= intersect_point_x) and (intersect_point_x <= x_4):
                    intersect_flag_count += 1

                if (y_1 <= intersect_point_y) and (intersect_point_y <= y_2):
                    intersect_flag_count += 1

                if (y_3 <= intersect_point_y) and (intersect_point_y <= y_4):
                    intersect_flag_count += 1

                if intersect_flag_count == 4:
                    intersect_point_list.append([intersect_point_x, intersect_point_y, 0])
                    intersect_voronoi_crvs_list.append(voronoi_line)

                    temp_convexhull_list.append(convexhull_crv)
                    # print('convex_crv', convexhull_crv)

            if len(intersect_point_list) >= 1:
                # 凸包を構成する辺の交差点を見つける。
                if len(temp_convexhull_list) == 2:
                    line_1 = temp_convexhull_list[0]
                    line_2 = temp_convexhull_list[1]
                    # print('line', temp_convexhull_list)
                    if line_1[0] == line_2[0]:
                        convexhull_merge_point.append(line_1[0])
                    elif line_1[0] == line_2[1]:
                        convexhull_merge_point.append(line_1[0])
                    elif line_1[1] == line_2[0]:
                        convexhull_merge_point.append(line_1[1])
                    elif line_1[1] == line_2[1]:
                        convexhull_merge_point.append(line_1[1])
                    else:
                        raise Exception('3 convexhull line intersection.... maybe')
                elif len(temp_convexhull_list) == 1:
                    pass
                elif len(temp_convexhull_list) == 0:
                    pass
                else:
                    raise Exception('Error')

                result.append([intersect_point_list, intersect_voronoi_crvs_list, convexhull_merge_point, temp_convexhull_list])
            elif len(intersect_point_list) == 0:
                pass
            else:
                raise Exception('Error')

        return result
