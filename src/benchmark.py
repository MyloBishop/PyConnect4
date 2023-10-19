from multiprocessing import Process
from multiprocessing.pool import Pool

from tqdm import tqdm

from ai import negamax
from board import Board

TIME_LIMIT_SECONDS = 300


def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        cases = [line.strip().split() for line in lines]
    return cases


def process_case(case):
    position, expected_score = case
    b = Board(position=position)
    score, _ = negamax(b)
    assert score == int(expected_score)


def multiprocess_file(file_path):
    print(f"\nProcessing file {file_path}...")
    cases = process_file(file_path)
    print(f"Running {len(cases)} test cases...")
    with Pool() as pool:
        with tqdm(total=len(cases)) as pbar:
            for _ in pool.imap_unordered(process_case, cases):
                pbar.update()


def main():
    file_list = [
        "data/Test_L3_R1.txt",
        "data/Test_L2_R1.txt",
        "data/Test_L2_R2.txt",
        "data/Test_L1_R1.txt",
        "data/Test_L1_R2.txt",
        "data/Test_L1_R3.txt",
    ]

    for file_path in file_list:
        process = Process(target=multiprocess_file, args=(file_path,))
        process.start()
        process.join(TIME_LIMIT_SECONDS)
        if process.is_alive():
            print(f"\nTerminating {file_path}...")
            process.kill()
            process.join()
            break


if __name__ == "__main__":
    main()
