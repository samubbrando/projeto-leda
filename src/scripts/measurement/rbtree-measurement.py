import os
import time
import copy
import csv
from typing import List
import sys

from src.data_structures.rbtree import RedBlackTree


def measure_insertion(data: List[int]) -> float:
    """Mede o tempo para inserir todos os elementos de uma amostra em uma RedBlackTree vazia."""
    start_time = time.perf_counter()
    
    rbt = RedBlackTree()
    for item in data:
        rbt.insert(item)
        
    end_time = time.perf_counter()
    return (end_time - start_time) * 1000 # Retorna em milissegundos

def measure_search(data: List[int], populated_tree: RedBlackTree) -> float:
    """Mede o tempo para buscar todos os elementos de uma amostra em uma RedBlackTree pré-populada."""
    start_time = time.perf_counter()
    
    for item in data:
        populated_tree.search(item)
        
    end_time = time.perf_counter()
    return (end_time - start_time) * 1000 # Retorna em milissegundos

def measure_deletion(data: List[int], populated_tree: RedBlackTree) -> float:
    """Mede o tempo para deletar todos os elementos de uma amostra, usando uma cópia da árvore."""
    tree_to_delete = populated_tree.copy()
    
    start_time = time.perf_counter()
    
    for item in data:
        tree_to_delete.delete(item)
        
    end_time = time.perf_counter()
    return (end_time - start_time) * 1000 # Retorna em milissegundos



def main():
    """
    Função principal que carrega as amostras, executa os testes e salva os resultados.
    """
    SAMPLE_PATH = os.getenv("SAMPLE_RELATIVE_PATH", "samples")
    MEASUREMENT_PATH = "measurements"
    SAMPLE_FILES = ["samples-sequential.txt", "samples-random.txt"]
    NUM_RUNS = 5 

    print("Iniciando medição de performance da RedBlackTree...")

    os.makedirs(MEASUREMENT_PATH, exist_ok=True)

    all_results = []

    for filename in SAMPLE_FILES:
        sample_type = "sequential" if "sequential" in filename else "random"
        filepath = os.path.join(SAMPLE_PATH, filename)
        
        print(f"\n{'='*50}")
        print(f"Processando arquivo de amostras: {filename}")
        print(f"{'='*50}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"ERRO: Arquivo de amostra não encontrado em '{filepath}'.")
            continue

        for line in lines:
            if not line.strip():
                continue
            
            data = [int(x) for x in line.strip().split()]
            sample_size = len(data)

            print(f"\n--- Medindo Amostra {sample_type.capitalize()} (Tamanho: {sample_size}) ---")
            
            insertion_times, search_times, deletion_times = [], [], []
            
            populated_rbtree = RedBlackTree()
            for item in data:
                populated_rbtree.insert(item)

            for i in range(NUM_RUNS):
                print(f"   -> Execução {i+1}/{NUM_RUNS}...")
                insertion_times.append(measure_insertion(data))
                search_times.append(measure_search(data, populated_rbtree))
                deletion_times.append(measure_deletion(data, populated_rbtree))
            
            avg_insertion = sum(insertion_times) / NUM_RUNS
            avg_search = sum(search_times) / NUM_RUNS
            avg_deletion = sum(deletion_times) / NUM_RUNS

            print(f"   -> Média Inserção: {avg_insertion:.4f} ms")
            print(f"   -> Média Busca:    {avg_search:.4f} ms")
            print(f"   -> Média Deleção:  {avg_deletion:.4f} ms")
            
            all_results.append({'sample_type': sample_type, 'size': sample_size, 'operation': 'insertion', 'time_ms': avg_insertion})
            all_results.append({'sample_type': sample_type, 'size': sample_size, 'operation': 'search', 'time_ms': avg_search})
            all_results.append({'sample_type': sample_type, 'size': sample_size, 'operation': 'deletion', 'time_ms': avg_deletion})

    if all_results:
        csv_path = os.path.join(MEASUREMENT_PATH, "rbtree_results.csv")
        print(f"\nSalvando resultados consolidados em '{csv_path}'...")
        
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=['sample_type', 'size', 'operation', 'time_ms'])
            writer.writeheader()
            writer.writerows(all_results)
        
        print("Resultados salvos com sucesso!")
    else:
        print("\nNenhum resultado foi gerado. Verifique os arquivos de amostra.")

    print("\nProcesso de medição finalizado!")


if __name__ == "__main__":
    main()