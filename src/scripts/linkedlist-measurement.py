from time import time
import threading

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

setups = [
    [setup_a, {
        "result-sequential": {
            "insertion": [],
            "search": [],
            "deletion": []
        }, 
        "result-random": {
            "insertion": [],
            "search": [],
            "deletion": []
        }}
    ], 
    [setup_b, {
        "result-sequential": {
            "insertion": [],
            "search": [],
            "deletion": []
        }, 
        "result-random": {
            "insertion": [],
            "search": [],
            "deletion": []
        }}
    ], 
    [setup_c, {
        "result-sequential": {
            "insertion": [],
            "search": [],
            "deletion": []
        }, 
        "result-random": {
            "insertion": [],
            "search": [],
            "deletion": []
        }}
    ]
    ]

def test_insert(data: list, test_linkedlist: LinkedList) -> float:
    start = time() * 1000
    
    print("Teste de adicao rolando")

    for value in data:
        test_linkedlist.addLast(int(value))

    end = time() * 1000
    
    return end - start


def test_deletion(data: list, test_linkedlist: LinkedList) -> float:
    start = time() * 1000

    print("Teste de delecao rolando")
    for value in data:
        test_linkedlist.removeByValue(int(value))

    end = time() * 1000

    return end - start


def test_search(data: list, test_linkedlist: LinkedList) -> float:
    start = time() * 1000

    print("Teste de procura rolando")
    for value in data:
        test_linkedlist.getByValue(int(value))

    end = time() * 1000

    return end - start

# =========================

def complete_test_sequential(data: str, results: dict):
    linkedlist_instance = LinkedList()
    split_data = data.split()

    results["insertion"] = [len(split_data), test_insert(split_data, linkedlist_instance)]
    results["search"] = [len(split_data), test_search(split_data, linkedlist_instance)]
    results["deletion"] = [len(split_data), test_deletion(split_data, linkedlist_instance)]

def complete_test_random(data: str, results: dict):
    linkedlist_instance = LinkedList()
    split_data = data.split()

    results["insertion"] = [len(split_data), test_insert(split_data, linkedlist_instance)]
    results["search"] = [len(split_data), test_search(split_data, linkedlist_instance)]
    results["deletion"] = [len(split_data), test_deletion(split_data, linkedlist_instance)]

# =========================

def write_results(data: list, filename: str):
    with open(f"measurements/{filename}.txt") as archive:
        for measurement in data: 
            archive.write(f"{measurement[0]} {measurement[1]} \n")
        

threads = {
    setup_a["name"]: {
        "sequential": [], 
        "random": []
    },
    setup_b["name"]: {
        "sequential": [], 
        "random": []
    },
    setup_c["name"]: {
        "sequential": [],
        "random": []
    }
}
# Calculando adição
for setup in setups:

    # SEQUENTIAL
    with open(f"src/samples/sequential-{setup[0]['name']}-{setup[0]['start']}-{setup[0]['end']}-{setup[0]['step']}.txt") as f:
        i = 1
        for data in f.readlines():
            print("Iniciando os testes", i)
            i += 1

            thread_to_add = threading.Thread(target=complete_test_sequential, args=(data, setup[1]["result-sequential"])) 
            thread_to_add.start()

            threads[setup[0]["name"]]["sequential"].append(thread_to_add)


    # RANDOM
    with open(f"src/samples/random-{setup[0]['name']}-{setup[0]['start']}-{setup[0]['end']}-{setup[0]['step']}.txt") as f:
        i = 1
        for data in f.readlines():
            print("Iniciando os testes", i)
            i += 1

            thread_to_add = threading.Thread(target=complete_test_sequential, args=(data, setup[1]["result-random"])) 
            thread_to_add.start()

            threads[setup[0]["name"]]["random"].append(thread_to_add)

    print(f"Terminou as threads para {setup[0]['name']}")

write_threads = {
    setup_a["name"]: {
    },
    setup_b["name"]: {
    },
    setup_c["name"]: {
    }
}

# TODO Implementar a escrita de arquivos