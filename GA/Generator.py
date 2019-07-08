# coding: utf-8
import random as rnd


def generator(num, x_range, y_range):
    """ ランダムな２次元座標値を出力 """

    # 範囲指定
    x_coordinate = [rnd.uniform(0, x_range) for _ in range(num + 50)]
    y_coordinate = [rnd.uniform(0, y_range) for _ in range(num + 50)]
    z_coordinate = [0 for _ in range(num + 50)]

    temp_coordinate = [[x_coordinate[i], y_coordinate[i], z_coordinate[i]] for i in range(num + 50)]

    coordinate = rnd.sample(temp_coordinate, num)

    # # keyが個体の番号、valueが座標値の辞書作成。
    # position_info = {}
    # for i in range(num):
    #     position_info[i] = coordinate[i]

    # 初期の巡回順序生成
    # select_num = [i for i in range(num)]
    # all_route = [rnd.sample(select_num, num) for _ in range(pop_num)]

    return coordinate
