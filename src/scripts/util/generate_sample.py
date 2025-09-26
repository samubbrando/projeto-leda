import os
import random

def generate_sequential_sample(size: int) -> list[int]:

    return list(range(1, size + 1))

def generate_random_sample(size: int) -> list[int]:
    
    return [random.randint(1, size * 10) for _ in range(size)]

def main():
    
    print("Iniciando a geração de amostras para o experimento.")

    output_path = os.getenv("SAMPLE_RELATIVE_PATH", "samples")
    
    # se n tem variavel de ambiente, usa esses aq
    default_sizes = "1000 5000 10000 20000 50000"
    sizes_str = os.getenv("SAMPLE_SIZES", default_sizes)
    try:
        sample_sizes = [int(s) for s in sizes_str.split()]
        print(f"Tamanhos das amostras a serem geradas: {sample_sizes}")
    except ValueError:
        print("Erro: A variável SAMPLE_SIZES contém valores não numéricos.")
        return

    os.makedirs(output_path, exist_ok=True)
    print(f"As amostras serão salvas em: '{output_path}/'")

    sequential_filepath = os.path.join(output_path, "samples-sequential.txt")
    random_filepath = os.path.join(output_path, "samples-random.txt")

    print("\nGerando amostras sequenciais...")
    try:
        with open(sequential_filepath, "w", encoding="utf-8") as f:
            for size in sample_sizes:
                data = generate_sequential_sample(size)
                line = ' '.join(map(str, data))
                f.write(line + '\n')
                print(f"   -> Amostra sequencial de tamanho {size} gerada.")
        print(f"Arquivo de amostras sequenciais salvo em: {sequential_filepath}")
    except IOError as e:
        print(f"Erro ao escrever o arquivo sequencial: {e}")
        return

    print("\nGerando amostras aleatórias...")
    try:
        with open(random_filepath, "w", encoding="utf-8") as f:
            for size in sample_sizes:
                data = generate_random_sample(size)
                line = ' '.join(map(str, data))
                f.write(line + '\n')
                print(f"   -> Amostra aleatória de tamanho {size} gerada.")
        print(f"arquivo de amostras aleatórias salvo em: {random_filepath}")
    except IOError as e:
        print(f"Erro ao escrever o arquivo aleatório: {e}")
        return
        
    print("\nProcesso finalizado. Todas as amostras foram geradas com sucesso.")


if __name__ == "__main__":
    main()