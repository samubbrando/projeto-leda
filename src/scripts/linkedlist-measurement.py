from time import time
from src.edas.linkedlist import LinkedList

import threading
import os

measurements_dir = os.path.join(
    os.path.dirname(__file__), "../../measurements")
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


def test_insert(data: list, test_linkedlist: LinkedList, filename: str) -> float:
    times = []
    for _ in range(25):
        test_linkedlist = LinkedList()

        start = time() * 1000

        print("Teste de adicao rolando")
        for value in data:
            test_linkedlist.addLast(int(value))

        end = time() * 1000
        print(start, end)

        times.append(end - start)

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{len(data)} {sum(times) / len(times):.2f}")


def test_deletion(data: list, test_linkedlist: LinkedList, filename: str) -> float:
    times = []

    for _ in range(25):
        test_linkedlist_copy = test_linkedlist

        start = time() * 1000
        
        print("Teste de delecao rolando")
        for value in data:
            test_linkedlist_copy.removeByValue(int(value))
        
        end = time() * 1000
        print(start, end)

        times.append(end - start)

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{len(data)} {sum(times) / len(times):.2f}\n")


def test_search(data: list, test_linkedlist: LinkedList, filename: str) -> float:
    times = []
    for _ in range(25):
        test_linkedlist_copy = test_linkedlist
        
        start = time() * 1000
        
        print("Teste de procura rolando")
        for value in data:
            test_linkedlist_copy.getByValue(int(value))
        
        end = time() * 1000
        print(start, end)

        times.append(end - start)

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{len(data)} {sum(times) / len(times):.2f}\n")


# Criando arquivos onde os resultados serão armazenados
for setup in setups:
    with open(f"measurements/linkedlist-{setup['name']}-insertion-sequential.txt", "w", encoding="utf-8") as f:
        f.write('\n')
    with open(f"measurements/linkedlist-{setup['name']}-search-sequential.txt", "w", encoding="utf-8") as f:
        f.write('\n')
    with open(f"measurements/linkedlist-{setup['name']}-deletion-sequential.txt", "w", encoding="utf-8") as f:
        f.write('\n')
    with open(f"measurements/linkedlist-{setup['name']}-insertion-random.txt", "w", encoding="utf-8") as f:
        f.write('\n')
    with open(f"measurements/linkedlist-{setup['name']}-search-random.txt", "w", encoding="utf-8") as f:
        f.write('\n')
    with open(f"measurements/linkedlist-{setup['name']}-deletion-random.txt", "w", encoding="utf-8") as f:
        f.write('\n')

working_threads = []

# Calculando adição
for setup in setups:
    # SEQUENTIAL
    with open(f"src/samples/sequential-{setup['name']}-{setup['start']}-{setup['end']}-{setup['step']}.txt") as f:
        i = 1
        for data in f.readlines():
            print("Iniciando os testes", i)
            i += 1

            test_linkedlist = LinkedList()
            split_data = data.split()

            thread_to_add = threading.Thread(target=test_insert, args=(
                split_data, test_linkedlist, f"measurements/linkedlist-{setup['name']}-insertion-sequential.txt"))
            thread_to_add.start()
            working_threads.append(thread_to_add)

            thread_to_add = threading.Thread(target=test_search, args=(
                split_data, test_linkedlist, f"measurements/linkedlist-{setup['name']}-insertion-sequential.txt"))
            thread_to_add.start()
            working_threads.append(thread_to_add)

            thread_to_add = threading.Thread(target=test_deletion, args=(
                split_data, test_linkedlist, f"measurements/linkedlist-{setup['name']}-deletion-sequential.txt"))
            thread_to_add.start()
            working_threads.append(thread_to_add)
        print()

    # RANDOM
    with open(f"src/samples/random-{setup['name']}-{setup['start']}-{setup['end']}-{setup['step']}.txt") as f:
        i = 1
        for data in f.readlines():
            print(f"Iniciando os testes setup: {setup["name"]} linked-list", i)
            i += 1

            test_linkedlist = LinkedList()
            split_data = data.split()

            thread_to_add = threading.Thread(target=test_insert, args=(
                split_data, test_linkedlist, f"measurements/linkedlist-{setup['name']}-insertion-random.txt"))
            thread_to_add.start()
            working_threads.append(thread_to_add)

            thread_to_add = threading.Thread(target=test_search, args=(
                split_data, test_linkedlist, f"measurements/linkedlist-{setup['name']}-insertion-random.txt"))
            thread_to_add.start()
            working_threads.append(thread_to_add)

            thread_to_add = threading.Thread(target=test_deletion, args=(
                split_data, test_linkedlist, f"measurements/linkedlist-{setup['name']}-deletion-random.txt"))
            thread_to_add.start()
            working_threads.append(thread_to_add)

        print()

    print("Terminado a designação das threads de trabalho")

for thread in working_threads:
    thread.join()
