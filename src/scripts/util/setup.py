import os

from generate_sample import generate_sample, generate_random_sequence_sample, generate_sequence_sample

def setup(path: str = "src/scripts/samples"):
    """
    Gera os arquivos de sample usando os atributos definidos em .env
    
    Args:
        path (str): Local onde os arquivos de sample ficarão armazenados.
    """
    
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

    try: 
        os.mkdir(path)
        print("Diretório criado com sucesso!")
    except FileExistsError:
        print("Diretório já foi criado.")
    except Exception as e:
        print(f"Erro inesperado ocorreu durante o processo de criação do diretório: {e}")

    for each_setup in setups:
        print(f"Fazendo o setup referente ao: {each_setup}")
        generate_sample(
            start=each_setup["start"],
            end=each_setup["end"],
            step=each_setup["step"],
            filename=each_setup["name"],
            path=path
        )
        generate_random_sequence_sample(
            start=each_setup["start"],
            end=each_setup["end"],
            step=each_setup["step"],
            filename=each_setup["name"],
            path=path
        )
        generate_sequence_sample(
            start=each_setup["start"],
            end=each_setup["end"],
            step=each_setup["step"],
            filename=each_setup["name"],
            path=path
        )
        print()


if __name__ == "__main__":
    setup()