import os
import time
import csv
from typing import List
from collections import deque

def measure_insertion(data: List[int]) -> float:
    """Mede o tempo para inserir todos os elementos de uma amostra em uma deque vazia."""
    start_time = time.perf_counter()
    
    # Usando a deque da biblioteca collections
    ll = deque()
    for item in data:
        ll.append(item)
        
    end_time = time.perf_counter()
    return (end_time - start_time) * 1000 # Retorna em milissegundos

def measure_search(data: List[int], populated_list: deque) -> float:
    """Mede o tempo para buscar todos os elementos de uma amostra em uma deque pré-populada."""
    start_time = time.perf_counter()
    
    for item in data:
        _ = item in populated_list
        
    end_time = time.perf_counter()
    return (end_time - start_time) * 1000 # Retorna em milissegundos

def measure_deletion(data: List[int], populated_list: deque) -> float:
    """Mede o tempo para deletar todos os elementos de uma amostra, usando uma cópia da lista."""
    list_to_delete = populated_list.copy()
    
    start_time = time.perf_counter()
    
    # iterando de tras pra frente para evitar que seja O(1). quando tentamos fzr de frente pra tras o próximo elemento procurado sempre era o próximo elemento da fila, sabotando os testes de certo modo
    for item in reversed(data):
        try:
            list_to_delete.remove(item)
        except ValueError:
            pass
            
    end_time = time.perf_counter()
    return (end_time - start_time) * 1000

def main():
    """
    Função principal que carrega as amostras, executa os testes e salva os resultados.
    """
    
    SAMPLE_PATH = os.getenv("SAMPLE_RELATIVE_PATH", "samples")
    MEASUREMENT_PATH = "measurements"
    SAMPLE_FILES = ["samples-sequential.txt", "samples-random.txt"]
    NUM_RUNS = 5 

    print("Iniciando medição de performance da PyLinkedList (collections.deque)...")

    # Garante que o diretório de medições exista
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
            
            populated_linkedlist = deque(data)

            for i in range(NUM_RUNS):
                print(f"   -> Execução {i+1}/{NUM_RUNS}...")
                insertion_times.append(measure_insertion(data))
                search_times.append(measure_search(data, populated_linkedlist))
                deletion_times.append(measure_deletion(data, populated_linkedlist))
     
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
        csv_path = os.path.join(MEASUREMENT_PATH, "PyLinkedList_results.csv")
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