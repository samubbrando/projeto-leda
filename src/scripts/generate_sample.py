
def generate_sample(start: int, end: int, step: str, filename: str = "sample", path: str = "."):
    """
    Gera uma sample de dados que será utilizada para mensurar as estruturas 
    que vamos compararar.

    Args:
        start (int): Número mínimo
        end (int): Número máximo
        step (int): Intervalo que define granularidade
        filename (str): Nome do arquivo sample, sem extensão .txt, segue
        o formato "filename-start-step.txt"
        path (str): Local onde o arquivo sample ficará criado.
    """

    with open(f"{path}/{filename}-{start}-{end}-{step}.txt", "w", encoding="utf-8") as file:
        for i in range(start, end + 1, step):
            file.write(f"{i}\n")


if __name__ == "__main__":
    start = int(input())
    end = int(input())
    sample_name = input()

    generate_sample(start, end, sample_name)