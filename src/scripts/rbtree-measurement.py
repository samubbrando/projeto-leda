from time import time
from src.edas.rbtree import RedBlackTree

import threading
import copy
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

results = []

def test_insert(data: list, test_rb_tree: RedBlackTree, filename: str) -> float:
    insertion_threads = []

    def isolated_task(data: list):
        test_rb_tree_empty = RedBlackTree()
        start = time() * 1000

        print("Teste de adicao rolando")
        for value in data:
            test_rb_tree_empty.insert(int(value))
            
        end = time() * 1000
        print(start, end)

        with open(filename, "a", encoding="utf-8") as f: 
            f.write(f"{len(data)} {end-start:.2f}")
            f.write('\n')

    for _ in range(25):
        ins_thread = threading.Thread(target=isolated_task, args=(data,))
        ins_thread.start()
        insertion_threads.append(ins_thread)

    for ins_thread in insertion_threads:
        ins_thread.join()

    # Para manter na original
    for value in data:
        test_rb_tree.insert(int(value), int(value))



def test_deletion(data: list, test_rb_tree: RedBlackTree, filename: str) -> float:
    deletion_threads = []

    def isolated_task(test_rb_tree: RedBlackTree, data: list):
        test_rb_tree_copy = copy.copy(test_rb_tree)

        start = time() * 1000

        print("Teste de delecao rolando")
        for value in data:
            test_rb_tree_copy.delete(int(value))

        end = time() * 1000
        print(start, end)

        with open(filename, "a", encoding="utf-8") as f: 
            f.write(f"{len(data)} {end-start:.2f}")
            f.write('\n')

    for _ in range(25):
        del_thread = threading.Thread(target=isolated_task, args=(test_rb_tree, data))
        del_thread.start()
        deletion_threads.append(del_thread)

    for del_thread in deletion_threads:
        del_thread.join()



def test_search(data: list, test_rb_tree: RedBlackTree, filename: str) -> float:
    search_threads = []

    def isolated_task(test_rb_tree: RedBlackTree, data: list):
        start = time() * 1000

        print("Teste de procura rolando")
        for value in data:
            test_rb_tree.search(int(value))

        end = time() * 1000
        print(start, end)

        with open(filename, "a", encoding="utf-8") as f: 
            f.write(f"{len(data)} {end-start:.2f}")
            f.write('\n')

    for _ in range(25):
        src_thread = threading.Thread(target=isolated_task, args=(test_rb_tree, data))
        src_thread.start()
        search_threads.append(src_thread)

    for src_thread in search_threads:
        src_thread.join()



# Criando arquivos onde os resultados serão armazenados
for setup in setups:
    with open(f"measurements/RedBlackTree-{setup['name']}-insertion-sequential.txt", "w", encoding="utf-8") as f:
        f.write('\n')
    with open(f"measurements/RedBlackTree-{setup['name']}-search-sequential.txt", "w", encoding="utf-8") as f:
        f.write('\n')
    with open(f"measurements/RedBlackTree-{setup['name']}-deletion-sequential.txt", "w", encoding="utf-8") as f:
        f.write('\n')
    with open(f"measurements/RedBlackTree-{setup['name']}-insertion-random.txt", "w", encoding="utf-8") as f:
        f.write('\n')
    with open(f"measurements/RedBlackTree-{setup['name']}-search-random.txt", "w", encoding="utf-8") as f:
        f.write('\n')
    with open(f"measurements/RedBlackTree-{setup['name']}-deletion-random.txt", "w", encoding="utf-8") as f:
        f.write('\n')


def test(data: list, setup_name: str, type_files: str):

    test_rb_tree = RedBlackTree()

    test_insert(
        data, test_rb_tree, f"measurements/RedBlackTree-{setup_name}-insertion-{type_files}.txt")

    test_search(
        data, test_rb_tree, f"measurements/RedBlackTree-{setup_name}-search-{type_files}.txt")
    
    test_deletion(
        data, test_rb_tree, f"measurements/RedBlackTree-{setup_name}-deletion-{type_files}.txt")


working_threads = []

# Calculando adição
for setup in setups:
    # SEQUENTIAL
    with open(f"src/samples/sequential-{setup['name']}-{setup['start']}-{setup['end']}-{setup['step']}.txt") as f:
        i = 1
        for data in f.readlines():
            print(f"Iniciando os testes sequential setup: {setup["name"]} RedBlackTree", i)
            thread_to_add = threading.Thread(target=test, args=(data.split(), setup['name'], 'sequential'))
            thread_to_add.start()
            working_threads.append(thread_to_add)

            i += 1

        print()

    # RANDOM
    with open(f"src/samples/random-{setup['name']}-{setup['start']}-{setup['end']}-{setup['step']}.txt") as f:
        i = 1
        for data in f.readlines():
            print(f"Iniciando os testes random setup: {setup["name"]} RedBlackTree", i)
            thread_to_add = threading.Thread(target=test, args=(data.split(), setup['name'], 'random'))
            thread_to_add.start()
            working_threads.append(thread_to_add)

            i += 1

        print()

    print("Terminado a designação das threads de trabalho")

for thread in working_threads:
    thread.join()
