from time import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.edas.avl import AVLTree

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

def test_insert(data: list, test_avltree: AVLTree) -> float:
    times = []

    print("Teste de adicao rolando")

    for _ in range(25):
        test_avltree = AVLTree()

        start = time() * 1000
        
        for value in data:
            test_avltree.add(int(value))
        end = time() * 1000

        times.append(end - start)

    return sum(times) / len(times)


def test_deletion(data: list, test_avltree: AVLTree) -> float:
    times = []

    print("Teste de delecao rolando")

    for _ in range(25):
        start = time() * 1000
        
        for value in data:
            test_avltree.remove(int(value))
        end = time() * 1000

        times.append(end - start)

    return sum(times) / len(times)


def test_search(data: list, test_avltree: AVLTree) -> float:
    times = []

    print("Teste de procura rolando")
    
    for _ in range(25):
        start = time() * 1000
        
        for value in data:
            test_avltree.search(int(value))
        end = time() * 1000

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

            test_avltree = AVLTree()
            split_data = data.split()

            result_sequential_insertion.append([len(split_data), test_insert(split_data, test_avltree)])
            result_sequential_search.append([len(split_data), test_search(split_data, test_avltree)])
            result_sequential_deletion.append([len(split_data), test_deletion(split_data, test_avltree)])
        print()
        
    with open(f"measurements/AVLTree-{setup['name']}-insertion-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_insertion:
            f.write(f"{i[0]} {i[1]}")
            f.write("\n")
    with open(f"measurements/AVLTree-{setup['name']}-search-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_search:
            f.write(f"{i[0]} {i[1]}")
            f.write("\n")
    with open(f"measurements/AVLTree-{setup['name']}-deletion-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_deletion:
            f.write(f"{i[0]} {i[1]}")
            f.write("\n")

    # RANDOM
    with open(f"src/samples/random-{setup['name']}-{setup['start']}-{setup['end']}-{setup['step']}.txt") as f:
        i = 1
        for data in f.readlines():
            print("Iniciando os testes", i)
            i += 1

            test_avltree = AVLTree()
            split_data = data.split()

            result_random_insertion.append([len(split_data), test_insert(split_data, test_avltree)])
            result_random_search.append([len(split_data), test_search(split_data, test_avltree)])
            result_random_deletion.append([len(split_data), test_deletion(split_data, test_avltree)])
            
        print()

    with open(f"measurements/AVLTree-{setup['name']}-insertion-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_insertion:
            f.write(f"{i[0]} {i[1]}")
            f.write("\n")
    with open(f"measurements/AVLTree-{setup['name']}-search-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_search:
            f.write(f"{i[0]} {i[1]}")
            f.write("\n")
    with open(f"measurements/AVLTree-{setup['name']}-deletion-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_deletion:
            f.write(f"{i[0]} {i[1]}")
            f.write("\n")

    print("Terminou tudo")
