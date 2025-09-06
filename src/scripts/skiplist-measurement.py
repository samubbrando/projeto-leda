from time import time

from util.setup import setup
from src.edas.skiplist import SkipList

import os

targeted_path = os.getenv("SAMPLE_RELATIVE_PATH") 
setup(path=targeted_path)

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

# Calculando adição
for setup in setups:
    test_skiplist = SkipList()
    with open(f"{setup['name']}-{setup['start']}-{setup['end']}.txt") as f:
        for line in f.readlines():
            test_skiplist.