import time

import pandas as pd

# pylint: disable=missing-function-docstring, missing-module-docstring


# Define your AI function here (replace with your actual AI function)
def evaluate_position(position):
    # Replace this with your AI evaluation code
    return "score nodes_time"


def read_benchmark_file(file_path):
    positions = []
    scores = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            position, score = line.strip().split()
            positions.append(position)
            scores.append(int(score))

    return positions, scores


def evaluate_test_set(file_path, max_runtime):
    positions, scores = read_benchmark_file(file_path)
    total_time = 0
    total_nodes = 0

    start_time = time.time()
    for position, score in zip(positions, scores, strict=True):
        result = evaluate_position(position)
        end_time = time.time()

        eval_score, nodes, eval_time = result
        eval_score = int(eval_score)
        nodes = int(nodes)
        eval_time = float(eval_time)

        assert eval_score == score  # Check if the score matches the expected score

        total_time += eval_time
        total_nodes += nodes

        if end_time - start_time > max_runtime:
            print(f"Time limit exceeded for {file_path}. Exiting.")
            return None

    mean_time = total_time / len(positions)
    mean_nodes = total_nodes / len(positions)
    k_positions_per_second = len(positions) / (total_time * 1e-6)

    return mean_time, mean_nodes, k_positions_per_second


def main():
    benchmark_files = [
        ("PyConnect4/ai/benchmark/data/Test_L1_R1.txt", "End-Easy"),
        ("PyConnect4/ai/benchmark/data/Test_L1_R2.txt", "Middle-Easy"),
        ("PyConnect4/ai/benchmark/data/Test_L1_R3.txt", "Middle-Medium"),
        ("PyConnect4/ai/benchmark/data/Test_L2_R1.txt", "Begin-Easy"),
        ("PyConnect4/ai/benchmark/data/Test_L2_R2.txt", "Begin-Medium"),
        ("PyConnect4/ai/benchmark/data/Test_L3_R1.txt", "Begin-Hard"),
    ]

    max_runtime = 1 * 60  # 1 minute

    data = []

    for file_path, file_name in benchmark_files:
        print(f"Processing {file_path}...")

        data = evaluate_test_set(file_path, max_runtime)
        if not data:
            data.append([file_path, "N/A", "N/A", "N/A"])
        else:
            mean_time, mean_nodes, k_positions_per_second = data
            data.append([file_name, mean_time, mean_nodes, k_positions_per_second])

    df = pd.DataFrame(
        data,
        columns=[
            "Test Set Name",
            "Mean Time (microseconds)",
            "Mean Number of Nodes",
            "K Positions/s",
        ],
    )
    print(df)


if __name__ == "__main__":
    main()
