from src.utils.jobs import MsaJob
from typing import Dict

def _subprocess_hhblit_msa_from_task(
    task:Dict[str,str]):
    '''Subprocess HHblits MSA from job
    ---
    This function performs HHblits MSA (multiple sequence alignment) based on the provided job information.

    ### Parameters
    * `task` (Dict[str, str]): A dictionary containing the following keys:
        - `fasta` (str): Path to the input FASTA file.
        - `uniclust` (str): Path to the Uniclust database.
        - `msa_path` (str): Path to save the resulting MSA.
    '''
    import subprocess

    fasta = task['fasta']
    uniclust = task['uniclust']
    msa_path = task['msa_path']
    a3m = fasta.split('/')[-1].split('.')[0]

    # $HHBLITS -i $FASTA -d $UNICLUST -E 0.001 -all -oa3m $MSADIR/$ID'.a3m'
    cmd = [
        '/opt/hh-suite/bin/hhblits '
        f'-i {fasta} '
        f'-d {uniclust} '
        '-E 0.001 '
        '-all '
        f'-oa3m {msa_path}/{a3m}.a3m'
    ]

    subprocess.Popen(cmd, shell=True).wait()
    return



def _fasta_preprocess_from_msa_job(
    msa_job:MsaJob):
    '''Preprocess FASTA data using specified MSA Job
    ---
    This function preprocesses FASTA data based on the provided msa_job.

    ### Parameters
    * `msa_job` (dict): A dictionary containing the following keys:
        - `fasta_file` (str): Path to the interactome FASTA file.
        - `fasta_path` (str): Path to where dockfold fasta files are written to. Default = None.
        - `id_seq_file` (str): Path to where id_seq.csv file is written to. Default = None.
    '''

    import os
    import logging
    from src.utils.utils import create_directory
    from src.preprocess_fasta import (
        read_fasta,
        write_fasta
    )

    # Path to input fasta file
    fasta_file = msa_job.fasta_file

    # Path where individual coded fasta files are written to; required by DockFold
    fasta_path = "%s/__dockfold_fasta__"%(fasta_file.rsplit('/',1)[0])
    if msa_job.fasta_path is not None:
        fasta_path = msa_job.fasta_path
    create_directory(fasta_path)

    # Path to pairwise comparison csv file
    id_seq_file = "%s/id_seqs.csv"%(fasta_file.rsplit('/',1)[0])
    if msa_job.id_seq_file is not None:
        id_seq_file = msa_job.id_seq_file

    # Warn users of previous run
    if os.path.isfile(id_seq_file):
        logging.info("id_seqs already exists, to overwrite, remove original")

    # Create fasta dataframe
    fasta_df = read_fasta(fasta_file)

    # Save fasta dataframe
    fasta_df.to_csv(id_seq_file, index=None)
    
    # Write individual fastas
    write_fasta(fasta_df, fasta_path)

    return


def _hhblits_msa_from_msa_job(
    msa_job:MsaJob):
    '''HHblits Mutiple Sequence Alignments
    ---
    Generate multiple sequence alignment (MSA) using HHblits based on provided msa_job.

    ### Parameters
    * `msa_job` (Dict[str, str]): A dictionary containing the following keys:
        - `fasta` (str): Path to the input FASTA file.
        - `uniclust` (str): Path to the UniClust database.
        - `msa_path` (str): Path to save the resulting MSA.
    '''

    import os
    from src.utils.utils import create_directory, multicore
    import logging

    # HHblits uniclust sequence source
    uniclust = msa_job.uniclust

    # HHblits msa output path
    msa_path = msa_job.msa_path
    create_directory(msa_path)

    # List previously acquired msa paths
    cached_msa = [i.split('.')[0] for i in os.listdir(msa_path) if i.endswith('.a3m')]

    # Number of hhblits processes to parrallel
    hhblits_cores = 1 # 32gig or ram per thread
    if msa_job.hhblits_cores is not None:
        hhblits_cores = msa_job.hhblits_cores
    

    # Path where individual coded fasta files are written to; required by DockFold
    fasta_path = "%s/__dockfold_fasta__"%(msa_job.fasta_file.rsplit('/',1)[0])
    if msa_job.fasta_path is not None:
        fasta_path = msa_job.fasta_path
    
     # Create HHblits jobs for MSA analysis
    tasks = [
        {
            "fasta":f"{fasta_path}/{i}",
            "uniclust":uniclust,
            'msa_path':msa_path,
            'hhblits_cores':hhblits_cores
        } for i in os.listdir(fasta_path) if i.split('.')[0] not in cached_msa
    ]

    logging.info(
        "\n".join(
            [
                "Number of MSA tasks:",
                "%s"%(len(tasks)),
                "Number of cached MSA",
                "%s"%(len(cached_msa)),
            ]
        )
    )

    # Run MSA multicore
    multicore(
        func=_subprocess_hhblit_msa_from_task,
        jobs=tasks,
        cores=hhblits_cores
    )
    return


def hhblits_msa_from_msa_job(
    msa_job:MsaJob):

    # Fasta preprocessing
    _fasta_preprocess_from_msa_job(msa_job)

    # Run hhblits
    _hhblits_msa_from_msa_job(msa_job)

    return