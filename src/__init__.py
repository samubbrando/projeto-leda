import time
from pathlib import Path
import csv
from edas.AvlTree import AVLTree
from edas.skiplist import SkipList

runs = 100
diretorio = Path("scripts/samples")
saida_csv = Path("resultados.csv")

# Cria/abre arquivo CSV para escrever
with saida_csv.open("w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Arquivo", "Sample", "Tamanho", "insertAVL(ns)", "insertSkipList(ns)"])  # cabeçalho

    for arquivo in diretorio.glob("*.txt"):
        with arquivo.open("r") as f:
            for idx, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                valores = list(map(int, line.split()))

                # ---------- AVL ----------
                avl_times = []
                for _ in range(runs):
                    avl = AVLTree()
                    start = time.perf_counter_ns()
                    for v in valores:
                        avl.insert_key_value(v, v)
                    end = time.perf_counter_ns()
                    avl_times.append(end - start)
                avl_media = sum(avl_times) / len(avl_times)

                # ---------- SkipList ----------
                skip_times = []
                for _ in range(runs):
                    skip = SkipList()
                    start = time.perf_counter_ns()
                    for v in valores:
                        skip.insert(v, v)
                    end = time.perf_counter_ns()
                    skip_times.append(end - start)
                skip_media = sum(skip_times) / len(skip_times)

                # Escreve linha no CSV
                writer.writerow([arquivo.name, idx, len(valores), int(avl_media), int(skip_media)])

print(f"Resultados salvos em {saida_csv}")