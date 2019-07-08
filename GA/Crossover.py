# coding: utf-8
import random as rnd


def order_crossover(select_pop, crossover_prob):
    ''' 確率的に順序交叉を実行する '''

    cross_pop = rnd.sample(select_pop, 2)
    pop_1 = cross_pop[0]
    pop_2 = cross_pop[1]

    check_prob = rnd.randint(0, 100)
    if check_prob <= crossover_prob:

        # 順序交叉
        new_pop_1 = []
        cut_index = rnd.randint(1, len(pop_1) - 2)
        new_pop_1.extend(pop_1[:cut_index])
        for i in range(len(pop_1)):
            if pop_2[i] not in new_pop_1:
                new_pop_1.append(pop_2[i])

        new_pop_2 = []
        new_pop_2.extend(pop_1[cut_index:])
        for i in range(len(pop_1)):
            if pop_2[i] not in new_pop_2:
                new_pop_2.append(pop_2[i])

        return new_pop_1, new_pop_2

    else:
        return pop_1, pop_2


def one_point_crossover(select_pop, crossover_prob):
    '''1点交叉'''

    cross_pop = rnd.sample(select_pop, 2)
    pop_1 = cross_pop[0]
    pop_2 = cross_pop[1]

    if len(pop_1) < 10:
        raise Exception('pop 1 gene strange reduce')

    if len(pop_2) < 10:
        raise Exception('pop 2 gene strange reduce')

    gene_length = len(pop_1)

    check_prb = rnd.randint(0, 100)
    if check_prb > crossover_prob:
        return pop_1, pop_2

    else:
        # 1点交叉
        cut_index = rnd.randint(1, len(pop_2) - 2)
        new_pop_1 = []
        new_pop_2 = []

        new_pop_1.extend(pop_1[:cut_index])
        new_pop_2.extend(pop_2[:cut_index])

        # 座標値がかぶらないようにpop_2の遺伝子を継承させる。
        temp_gene = []
        temp_gene.extend(pop_2[cut_index:])
        temp_gene.extend(pop_2[:cut_index])
        count = 0
        while True:
            if len(new_pop_1) == gene_length:
                break

            if temp_gene[count] not in new_pop_1:
                new_pop_1.append(temp_gene[count])
            else:
                pass

            count += 1
            if count >= len(temp_gene) - 1:
                raise Exception('Gene Renewal Fail')

        temp_gene = []
        temp_gene.extend(pop_1[cut_index:])
        temp_gene.extend(pop_1[:cut_index])
        count = 0
        while True:
            if len(new_pop_2) == gene_length:
                break

            if temp_gene[count] not in new_pop_2:
                new_pop_2.append(temp_gene[count])
            else:
                pass

            count += 1
            if count >= len(temp_gene) - 1:
                raise Exception('Gene Renewal Fail')
        return new_pop_1, new_pop_2
