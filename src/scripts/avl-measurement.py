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
    test_avltree = AVLTree()

    start = time() * 1000
    
    print("Teste de adicao rolando")

    for value in data:
        test_avltree.add(int(value))

    end = time() * 1000
    
    print(start, end)

    return end - start


def test_deletion(data: list, test_avltree: AVLTree) -> float:
    start = time() * 1000

    print("Teste de delecao rolando")
    for value in data:
        test_avltree.remove(int(value))

    end = time() * 1000

    print(start, end)

    return end - start


def test_search(data: list, test_avltree: AVLTree) -> float:
    start = time() * 1000

    print("Teste de procura rolando")
    for value in data:
        test_avltree.search(int(value))

    end = time() * 1000

    print(start, end)

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
        i = 1
        for data in f.readlines():
            print("Iniciando os testes", i)
            i += 1

            test_avltree = AVLTree()

            result_sequential_insertion.append([len(data), test_insert(data.split(), test_avltree)])
            result_sequential_search.append([len(data), test_search(data.split(), test_avltree)])
            result_sequential_deletion.append([len(data), test_deletion(data.split(), test_avltree)])
        print()
        
    with open("measurements/AVLTree-insertion-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_insertion:
            f.write(str(i))
            f.write("\n")
    with open("measurements/AVLTree-search-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_search:
            f.write(str(i))
            f.write("\n")
    with open("measurements/AVLTree-deletion-sequential.txt", "w", encoding="utf-8") as f:
        for i in result_sequential_deletion:
            f.write(str(i))
            f.write("\n")

    # RANDOM
    with open(f"src/samples/random-{setup['name']}-{setup['start']}-{setup['end']}-{setup['step']}.txt") as f:
        i = 1
        for data in f.readlines():
            print("Iniciando os testes", i)
            i += 1

            test_avltree = AVLTree()

            result_random_insertion.append([len(data), test_insert(data.split(), test_avltree)])
            result_random_search.append([len(data), test_search(data.split(), test_avltree)])
            result_random_deletion.append([len(data), test_deletion(data.split(), test_avltree)])
            
        print()

    with open("measurements/AVLTree-insertion-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_insertion:
            f.write(str(i))
            f.write("\n")
    with open("measurements/AVLTree-search-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_search:
            f.write(str(i))
            f.write("\n")
    with open("measurements/AVLTree-deletion-random.txt", "w", encoding="utf-8") as f:
        for i in result_random_deletion:
            f.write(str(i))
            f.write("\n")


    print("Terminou tudo")

