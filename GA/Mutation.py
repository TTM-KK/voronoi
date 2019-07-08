# coding: utf-8

import random as rnd


def mutation(pop, mutation_prob):
    """ 循環経路の順番をランダムで入れ替える """

    check_prob = rnd.randint(0, 100)

    if check_prob <= mutation_prob:
        select_num = [i for i in range(num)]
        select_index = rnd.sample(select_num, 2)

        a = pop[select_index[0]]
        b = pop[select_index[1]]
        pop[select_index[1]] = a
        pop[select_index[0]] = b

    return pop
