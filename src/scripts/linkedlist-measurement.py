from time import time

from src.edas.linkedlist import LinkedList

import os

measurements_dir = os.path.join(os.path.dirname(__file__), "../../measurements")
os.makedirs(measurements_dir, exist_ok=True)

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

def test_insert(data: list, test_linkedlist: LinkedList) -> float:
    start = time() * 1000
    
    print("Teste de adicao rolando")

    for value in data:
        test_linkedlist.addLast(int(value))

    end = time() * 1000
    
    print(start, end)

    return end - start


def test_deletion(data: list, test_linkedlist: LinkedList) -> float:
    start = time() * 1000

    print("Teste de delecao rolando")
    for value in data:
        test_linkedlist.removeByValue(int(value))

    end = time() * 1000

    print(start, end)

    return int(end - start)


def test_search(data: list, test_linkedlist: LinkedList) -> float:
    start = time() * 1000

    print("Teste de procura rolando")
    for value in data:
        test_linkedlist.getByValue(int(value))

    end = time() * 1000

    print(start, end)

    return int(end - start)



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

            test_linkedlist = LinkedList()

            result_sequential_insertion.append([len(data), test_insert(data.split(), test_linkedlist)])
            result_sequential_search.append([len(data), test_search(data.split(), test_linkedlist)])
            result_sequential_deletion.append([len(data), test_deletion(data.split(), test_linkedlist)])
        print()

    # RANDOM
    with open(f"src/samples/random-{setup['name']}-{setup['start']}-{setup['end']}-{setup['step']}.txt") as f:
        i = 1
        for data in f.readlines():
            print("Iniciando os testes", i)
            i += 1

            test_linkedlist = LinkedList()

            result_random_insertion.append([len(data), test_insert(data.split(), test_linkedlist)])
            result_random_search.append([len(data), test_search(data.split(), test_linkedlist)])
            result_random_deletion.append([len(data), test_deletion(data.split(), test_linkedlist)])
        print()

    with open("measurements/linkedlist-insertion-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_insertion:
            f.write(str(i))
            f.write("\n")
    with open("measurements/linkedlist-search-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_search:
            f.write(str(i))
            f.write("\n")
    with open("measurements/linkedlist-deletion-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_deletion:
            f.write(str(i))
            f.write("\n")

    with open("measurements/linkedlist-insertion-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_insertion:
            f.write(str(i))
            f.write("\n")
    with open("measurements/linkedlist-search-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_search:
            f.write(str(i))
            f.write("\n")
    with open("measurements/linkedlist-deletion-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_deletion:
            f.write(str(i))
            f.write("\n")

    print("Terminou tudo")