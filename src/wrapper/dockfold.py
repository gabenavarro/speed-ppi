from typing import Optional, List


def wrapper_dockfold_modeling(
    num_ensemble:int,
    complex_id:str,
    max_recycles:int,
    data_dir:str,
    msa1:str,
    msa2:str,
    output_dir:str):
    
    import subprocess

    cmd = [
        'python /app/scripts/dockfold_modeling.py '
        f'--num-ensemble {num_ensemble} '
        f'--complex-id {complex_id} '
        f'--max-recycles {max_recycles} '
        f'--data-dir {data_dir} '
        f'--msa-one {msa1} '
        f'--msa-two {msa2} '
        f'--output-dir {output_dir} '
    ]

    subprocess.Popen(cmd, shell=True).wait()
    return None