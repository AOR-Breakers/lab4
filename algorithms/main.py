import time
import numpy as np
from tabulate import tabulate
import algorithms.iterated_local_search as IteratedLocalSearch
import algorithms.local_search as local_search


def read_file(name):
    with open(f"..//benchmarks//{name}", 'r') as bench_file:
        bench_data = bench_file.readlines()
    n = int(bench_data[0])
    distances = []
    for idx in range(n):
        distances.append(list(map(int, bench_data[idx + 1].split())))
    flows = []
    for idx in range(n + 1, 2 * n + 1):
        flows.append(list(map(int, bench_data[idx + 1].split())))
    return n, np.array(distances), np.array(flows)


def benchmark(function, name: str, iters: int = 100):
    n, distance, flows = read_file(name)
    time_sum = 0
    results = []
    for _ in range(iters):
        start_time = time.monotonic()
        results.append((function.solve(distance, flows)))
        end_time = time.monotonic()
        time_sum += end_time - start_time
    mean_time = time_sum / iters
    final_summary_dist, final_ans = sorted(results, key=lambda t: t[0])[0]

    answer_str = ' '.join(list(map(str, final_ans)))
    answer_lines = [answer_str[i:i + 80] for i in range(0, len(answer_str), 80)]
    answer_formatted = '\n'.join(answer_lines)

    table_row = [name, answer_formatted, final_summary_dist, mean_time]

    with open(f'..//answers//{function.name}_{name}.sol', 'a+') as file:
        print(' '.join(list(map(str, final_ans))), file=file)

    return table_row


if __name__ == '__main__':
    benchmark_names = ['tai20a', 'tai40a', 'tai60a', 'tai80a', 'tai100a']
    modules = [local_search, IteratedLocalSearch]
    headers = ["Bench", "Answer", "Summary distance", "Avg time"]

    for module in modules:
        print(module.name)
        table = [headers]
        for benchmark_name in benchmark_names:
            table.append(benchmark(module, benchmark_name, iters=10))
        print(tabulate(table, headers="firstrow", tablefmt="grid"))
        print("\n")
