# coding: utf-8
import rhinoscriptsyntax as rs


def signed_area(p1, p2, p3):
    '''
    符号付き面積を計算
    :param p1:
    :param p2:
    :param p3:
    :return:
    '''
    area = (((p2[0] - p1[0]) * (p3[1] - p1[1])) - ((p3[0] - p1[0]) * (p2[1] - p1[1]))) / 2
    return area


def convex_hull(p_list):
    '''
    グラハムの凸包走査
    :param p_list:
    :return:
    '''

    p_sort = []
    for i in p_list:
        p_sort.append(i[0])

    # x座標が最小のものをリストの先頭に配置。
    min_index = p_sort.index(min(p_sort))
    min_p = p_list.pop(min_index)
    p_list.insert(0, min_p)

    # 座標最小の点と他の点との角度順にソート ソートアルゴリズムに選択の余地が有る。
    p_length = len(p_list)
    count = 0
    index = 0
    while True:
        count += 1
        index += 1

        area_sign = signed_area(p_list[0], p_list[index], p_list[index + 1])

        # 符号付き面積が負ならば点を入れ替え
        if area_sign < 0:
            p_list[index], p_list[index + 1] = p_list[index + 1], p_list[index]
            count = 0

        if count == p_length - 1:
            break

        if index == p_length - 2:
            index = 0

    # 凹部の点を削除する。
    index = -1
    count = 0
    while True:
        index += 1
        count += 1

        area_sign = signed_area(p_list[index], p_list[index + 1], p_list[index + 2])
        if area_sign < 0:
            del p_list[index + 1]
            count = 0

        if count == len(p_list):
            break

        if index >= len(p_list) - 3:
            index = -1
    return p_list


def draw_rhino(p_list):
    line_list = []
    for i in range(len(p_list)):
        j = i + 1
        if i == len(p_list) - 1:
            j = 0

        line = rs.AddLine([p_list[i][0], p_list[i][1], 0], [p_list[j][0], p_list[j][1], 0])
        line_list.append(line)

    rs.JoinCurves(line_list)

    for i in line_list:
        rs.DeleteObject(i)


def make_line(points_list):
    '''point to line'''
    line_list = []
    for i in range(len(points_list)):
        j = i + 1
        if i == len(points_list) - 1:
            j = 0

        line_list.append([[points_list[i][0], points_list[i][1], 0], [points_list[j][0], points_list[j][1], 0]])




    # line_list = []
    # for i in range(len(points_list)):
    #     point = []
    #     if i == len(points_list) - 1:
    #         point.append(points_list[i])
    #         point.append(points_list[0])
    #
    #     else:
    #         point.append(points_list[i])
    #         point.append(points_list[i + 1])
    #
    #     line_list.append(point)

    return line_list
