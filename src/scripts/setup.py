import os
from generate_sample import generate_sample

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

for setup in setups:
    generate_sample(
        start=setup["start"],
        end=setup["end"],
        step=setup["step"],
        filename=setup["name"],
        path="src/scripts/samples"
    )