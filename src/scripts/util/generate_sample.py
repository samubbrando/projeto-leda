from random import randint

def generate_sample(start: int, end: int, step: str, filename: str = "sample", path: str = "."):
    """
    Gera uma sample de dados que será utilizada para mensurar as estruturas 
    que vamos compararar.
    
    Args:
        start (int): Número mínimo
        end (int): Número máximo
        step (int): Intervalo que define granularidade
        filename (str): Nome do arquivo sample, sem extensão .txt, segue
        o formato "<filename>-<start>-<step>.txt"
        path (str): Local onde o arquivo sample ficará criado.
    """

    print(f"Criando o arquivo de sample {path}/{filename}-{start}-{end}-{step}.txt")
    try:
        with open(f"{path}/{filename}-{start}-{end}-{step}.txt", "w", encoding="utf-8") as file:
            for i in range(start, end + 1, step):
                file.write(f"{i}\n")
        print("Arquivo criado com sucesso!")
    except Exception as e:
        print(f"PROCESSO DE CRIAÇÃO DE SAMPLE OCORREU UM IMPREVISTO.")
        print(f"Erro: {e}")

def generate_random_sequence_sample(start: int, end: int, step: int, filename: str = "sample", path: str = "."):
    """
    Gera uma sample de dados que será utilizada para mensurar as estruturas 
    que vamos compararar. Números aleatórios gerados em sequência baseado no
    start e end definido no arquivo .env.

    Args:
        start (int): Número mínimo
        end (int): Número máximo
        step (int): Intervalo que define granularidade
        filename (str): Nome do arquivo sample, sem extensão .txt, segue
        o formato "random-<filename>-<start>-<step>.txt"
        path (str): Local onde o arquivo sample ficará criado.
    """

    print(f"Criando o arquivo de sample {path}/random-{filename}-{start}-{end}-{step}.txt")
    try:
        with open(f"{path}/random-{filename}-{start}-{end}-{step}.txt", "w", encoding="utf-8") as file:
            
            for i in range(start + step, end, step):
                file.write(f"{randint(start, end)}")
                
                for _ in range(start + step, i - 1):
                    file.write(f" {randint(start, end)}")
                file.write("\n")

        print("Arquivo criado com sucesso!")
    except Exception as e:
        print(f"PROCESSO DE CRIAÇÃO DE SAMPLE OCORREU UM IMPREVISTO.")
        print(f"Erro: {e}")

def generate_sequence_sample(start: int, end: int, step: int, filename: str = "sample", path: str = "."):
    """
    Gera uma sample de dados que será utilizada para mensurar as estruturas 
    que vamos compararar. Números gerados em sequência baseado no start
    e end definido no arquivo .env.

    Args:
        start (int): Número mínimo
        end (int): Número máximo
        step (int): Intervalo que define granularidade
        filename (str): Nome do arquivo sample, sem extensão .txt, segue
        o formato "sequential-<filename>-<start>-<step>.txt"
        path (str): Local onde o arquivo sample ficará criado.
    """

    print(f"Criando o arquivo de sample {path}/sequential-{filename}-{start}-{end}-{step}.txt")
    try:
        with open(f"{path}/sequential-{filename}-{start}-{end}-{step}.txt", "w", encoding="utf-8") as file:
            
            for i in range(start + step, end, step):
                file.write(f"{start}")
                
                for d in range(start + step, i - 1):
                    file.write(f" {d}")
                file.write("\n")

        print("Arquivo criado com sucesso!")
    except Exception as e:
        print(f"PROCESSO DE CRIAÇÃO DE SAMPLE OCORREU UM IMPREVISTO.")
        print(f"Erro: {e}")


if __name__ == "__main__":
    start = int(input())
    end = int(input())
    sample_name = input()

    generate_sample(start, end, sample_name)
