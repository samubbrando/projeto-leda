from time import time
from src.edas.rbtree import RedBlackTree
import os

setup_a = {
    "name": "setup-a",
    "start": int(os.getenv("START_A")),
    "end": int(os.getenv("END_A")),
    "step": int(os.getenv("STEP_A"))
}

setup_b = {
    "name": "setup-b",
    "start": int(os.getenv("START_B")),
    "end": int(os.getenv("END_B")),
    "step": int(os.getenv("STEP_B"))
}

setup_c = {
    "name": "setup-c",
    "start": int(os.getenv("START_C")),
    "end": int(os.getenv("END_C")),
    "step": int(os.getenv("STEP_C"))
}

setups = [setup_a, setup_b, setup_c]


def test_insert(data: list, test_rbtree: RedBlackTree) -> float:
    times = []
    for _ in range(25):  # 25 execuções
        test_rbtree = RedBlackTree()
        start = time() * 1000

        print("Teste de adicao rolando")
        for value in data:
            test_rbtree.insert(int(value))

        end = time() * 1000
        print(start, end)
        times.append(end - start)

    return sum(times) / len(times)  # média


def test_deletion(data: list, test_rbtree: RedBlackTree) -> float:
    times = []
    for _ in range(25):  # 25 execuções
        start = time() * 1000

        print("Teste de delecao rolando")
        for value in data:
            test_rbtree.delete(int(value))

        end = time() * 1000
        print(start, end)
        times.append(end - start)

    return sum(times) / len(times)


def test_search(data: list, test_rbtree: RedBlackTree) -> float:
    times = []
    for _ in range(25):  # 25 execuções
        start = time() * 1000

        print("Teste de procura rolando")
        for value in data:
            test_rbtree.search(int(value))

        end = time() * 1000
        print(start, end)
        times.append(end - start)

    return sum(times) / len(times)


# Calculando adição
for setup in setups:
    result_sequential_insertion = []
    result_random_insertion = []

    result_sequential_search = []
    result_random_search = []

    result_sequential_deletion = []
    result_random_deletion = []

    # SEQUENTIAL
    with open(f"src/samples/sequential-{setup['name']}-{setup['start']}-{setup['end']}-{setup['step']}.txt") as f:
        i = 1
        for data in f.readlines():
            print("Iniciando os testes", i)
            i += 1

            test_rbtree = RedBlackTree()

            result_sequential_insertion.append([len(data.split()), test_insert(data.split(), test_rbtree)])
            result_sequential_search.append([len(data.split()), test_search(data.split(), test_rbtree)])
            result_sequential_deletion.append([len(data.split()), test_deletion(data.split(), test_rbtree)])
        print()

    with open("measurements/RedBlackTree-insertion-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_insertion:
            f.write(str(i))
            f.write("\n")
    with open("measurements/RedBlackTree-search-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_search:
            f.write(str(i))
            f.write("\n")
    with open("measurements/RedBlackTree-deletion-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_deletion:
            f.write(str(i))
            f.write("\n")

    # RANDOM
    with open(f"src/samples/random-{setup['name']}-{setup['start']}-{setup['end']}-{setup['step']}.txt") as f:
        i = 1
        for data in f.readlines():
            print("Iniciando os testes", i)
            i += 1

            test_rbtree = RedBlackTree()

            result_random_insertion.append([len(data.split()), test_insert(data.split(), test_rbtree)])
            result_random_search.append([len(data.split()), test_search(data.split(), test_rbtree)])
            result_random_deletion.append([len(data.split()), test_deletion(data.split(), test_rbtree)])
        print()

    with open("measurements/RedBlackTree-insertion-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_insertion:
            f.write(str(i))
            f.write("\n")
    with open("measurements/RedBlackTree-search-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_search:
            f.write(str(i))
            f.write("\n")
    with open("measurements/RedBlackTree-deletion-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_deletion:
            f.write(str(i))
            f.write("\n")

    print("Terminou tudo")
