import random
from typing import List
from local_search import local_search_func

name = 'Iterated local search'


def stochastic_two_opt(ans: List[int], i: int, j: int):
    if i == 0:
        return ans[:i] + ans[j::-1] + ans[j + 1:]

    return ans[:i] + ans[j:i - 1:-1] + ans[j + 1:]


def solve(distance: List, flow: List):
    value, result = local_search_func(distance, flow, list(range(len(distance))))

    iteration = 0
    count = len(distance)

    while iteration < 10:
        iteration += 1

        i = random.randint(0, count - 2)
        rnd = i + random.randint(2, count // 2)
        j = rnd if rnd < count else count - 1
        new_result = stochastic_two_opt(result, i, j)
        new_value, new_result = local_search_func(distance, flow, new_result)

        if new_value < value:
            value = new_value
            result = new_result
            iteration = 0

    return value, result
