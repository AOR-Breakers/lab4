import numpy as np
from typing import List


name = 'Local search'


def calculate(distance: List[List[int]], flow: List[List[int]], res: List[int]):
    count = len(distance)
    sum_d = 0

    for i in range(count):
        for j in range(count):
            sum_d += distance[i][j] * flow[res[i]][res[j]]

    return sum_d


def swap_and_recalculate(distance: List[List[int]], flow: List[List[int]], res: List[int], k: int, m: int, sum_d: int):
    new_res = res.copy()
    new_res[k], new_res[m] = res[m], res[k]
    count = len(distance)

    delta = 0
    for i in range(count):
        if i != new_res[m] or i != new_res[k]:
            delta += (flow[new_res[m]][new_res[i]] - flow[new_res[k]][new_res[i]]) * (distance[m][i] - distance[k][i])

    return new_res, sum_d + 2 * delta


def local_search_func(distance: List[List[int]], flow: List[List[int]], result: List[int]):
    count = len(distance)

    value = calculate(distance, flow, result)
    dont_look_bits = [0] * count
    k = 0

    while k < count:
        if dont_look_bits[k] == 1:
            k += 1
            continue

        improvement = False
        for m in range(count):
            if m != k:
                new_result, new_value = swap_and_recalculate(distance, flow, result, k, m, value)

                if new_value < value:
                    result = new_result
                    value = new_value
                    improvement = True
                    dont_look_bits[k] = 0
                    k = 0
                    break

        if not improvement:
            dont_look_bits[k] = 1

        k += 1
    return value, result


def solve(distances: List[List[int]], flows: List[List[int]]):
    initial_ans = np.arange(len(distances))
    np.random.shuffle(initial_ans)

    return local_search_func(distances, flows, initial_ans)
