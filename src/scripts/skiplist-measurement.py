from time import time

from src.edas.skiplist import SkipList

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

def test_insert(data: list, test_skiplist: SkipList) -> float:
    test_skiplist = SkipList()

    start = time() * 1000
    
    print("Teste de adicao rolando")

    for value in data:
        test_skiplist.insert(int(value), int(value))

    end = time() * 1000
    
    return end - start


def test_deletion(data: list, test_skiplist: SkipList) -> float:
    start = time() * 1000

    print("Teste de delecao rolando")
    for value in data:
        test_skiplist.delete(int(value))

    end = time() * 1000

    return end - start


def test_search(data: list, test_skiplist: SkipList) -> float:
    start = time() * 1000

    print("Teste de procura rolando")
    for value in data:
        test_skiplist.search(int(value))

    end = time() * 1000

    return end - start

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
        i = 0
        for data in f.readlines():
            print("Iniciando os testes", i)
            i += 1

            test_skiplist = SkipList()
            split_data = data.split()

            result_sequential_insertion.append([len(split_data), test_insert(split_data, test_skiplist)])
            result_sequential_search.append([len(split_data), test_search(split_data, test_skiplist)])
            result_sequential_deletion.append([len(split_data), test_deletion(split_data, test_skiplist)])
        print()


    with open(f"measurements/skiplist-{setup['name']}-insertion-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_insertion:
            f.write(f"{i[0]} {i[1]}")
            f.write("\n")
    with open(f"measurements/skiplist-{setup['name']}-search-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_search:
            f.write(f"{i[0]} {i[1]}")
            f.write("\n")
    with open(f"measurements/skiplist-{setup['name']}-deletion-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_deletion:
            f.write(f"{i[0]} {i[1]}")
            f.write("\n")

    # RANDOM
    with open(f"src/samples/random-{setup['name']}-{setup['start']}-{setup['end']}-{setup['step']}.txt") as f:
        i = 0
        for data in f.readlines():
            print("Iniciando os testes", i)
            i += 1

            test_skiplist = SkipList()
            split_data = data.split()

            result_random_insertion.append([len(split_data), test_insert(split_data, test_skiplist)])
            result_random_search.append([len(split_data), test_search(split_data, test_skiplist)])
            result_random_deletion.append([len(split_data), test_deletion(split_data, test_skiplist)])
        print()

    with open(f"measurements/skiplist-{setup['name']}-insertion-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_insertion:
            f.write(f"{i[0]} {i[1]}")
            f.write("\n")
    with open(f"measurements/skiplist-{setup['name']}-search-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_search:
            f.write(f"{i[0]} {i[1]}")
            f.write("\n")
    with open(f"measurements/skiplist-{setup['name']}-deletion-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_deletion:
            f.write(f"{i[0]} {i[1]}")
            f.write("\n")


