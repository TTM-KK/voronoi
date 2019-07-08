# coding: utf-8

import random as rnd
import copy


def selection(all_route, evaluate_value, tournament_select_num, tournament_size, elite_select_num, ascending=False):
    """ トーナメント選択とエリート保存を行う"""

    select_pop = []
    elite_pop = []
    # トーナメント選択
    while True:
        select = rnd.sample(evaluate_value, tournament_size)
        select.sort(reverse=ascending)
        for i in range(tournament_select_num):
            value = select[i]
            index = evaluate_value.index(value)
            select_pop.append(all_route[index])

        # 個体数の半数個選択するまで実行
        if len(select_pop) >= len(all_route) / 2:
            break

    # エリート保存
    sort_evaluate_value = copy.deepcopy(evaluate_value)
    sort_evaluate_value.sort(reverse=ascending)
    for i in range(elite_select_num):
        value = sort_evaluate_value[i]
        index = evaluate_value.index(value)
        elite_pop.append(all_route[index])

    return select_pop, elite_pop
