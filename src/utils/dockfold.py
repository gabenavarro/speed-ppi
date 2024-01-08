from src.utils.jobs import DockFoldJob


def _dockfold_modeling(
    dockfold_job:DockFoldJob):
    '''DockFold Modeling
    ---

    Runs dockfold modeling analysis from dockfold job.

    ### Parameters
        * `max_recycles` (int): Number of Dockfold re-runs. Default 20.
        * `data_dir` (str): Path to pre-trained dockfold models. Default `/opt/data`.
        * `msa_path` (str): Path to MSA files.
        * `msa_list_one` (str): List of MSAs to compare again. Will do all against all if no `msa_list_two` provided.
        * `msa_list_two` (str): List of MSAs to compare against `msa_list_one`. Default is None. If provided, will only do protein in list two againt proteins in list one.
        * `output_dir` (str): Path to where results are written to. 
    '''

    from src.run_alphafold_single import main
    from src.utils.utils import create_directory
    from itertools import combinations, product
    import os
    import logging
    logging.getLogger().setLevel(logging.INFO)    

    # Path to MSA files
    msa_path = dockfold_job.msa_path

    # Location of parent result files
    output_dir = dockfold_job.output_dir
    create_directory(output_dir)

    # Pretrain model path
    data_dir = dockfold_job.data_dir

    # Number of cycles to optimize structure
    max_recycles = dockfold_job.max_recycles

    msa_list_one = dockfold_job.msa_list_one
    msa_list_two = dockfold_job.msa_list_two

    # Determine if all on all or few againt all
    if msa_list_two is None:
        modeling_tasks = list(combinations(msa_list_one, 2))
    else:
        modeling_tasks = [(f"{a}",f"{b}") for a,b in product(msa_list_two, msa_list_one)]

    # Start Modeling job pairwise
    for task in modeling_tasks:
        msa_one = "%s/%s.a3m"%(msa_path,task[0])
        msa_two = "%s/%s.a3m"%(msa_path,task[1])
        if os.path.isfile(msa_one) and os.path.isfile(msa_two):
            complex_id = "%s-%s"%(task[0],task[1])
            result_path = f"{output_dir}/pred{complex_id}/"
            create_directory(result_path)
            try:
                main(
                    num_ensemble=1,
                    complex_id=complex_id,
                    max_recycles=max_recycles,
                    data_dir=data_dir,
                    msa1=msa_one,
                    msa2=msa_two,
                    output_dir=result_path
                )
            except Exception as e:
                logging.warning(
                    f"""
                    Could not process: {complex_id}
                    """
                )
    return



def _consolidate_dockfold_results(
    dockfold_job:DockFoldJob):

    import glob
    from pandas import read_csv
    from pandas import concat as dataframe_concat
    import logging
    import time    

    # Location of result file parent
    output_dir = dockfold_job.output_dir

    # Get user input for parquet_dir
    parquet_dir = dockfold_job.parquet_dir

    # Gather all 
    predictions = glob.glob(f'{output_dir}/pred*/*_metrics.csv')
    all_ppis = [read_csv(pred) for pred in predictions]
    ppi_net = dataframe_concat(all_ppis)

    
    # Save results to local output as CSV
    ppi_net.to_csv(f'{output_dir}/ppi_result.csv', index=None)
    logging.info(f'Saved all PPIs after filtering on pDockQ to {output_dir} ppis_filtered.csv')

    # Save results to parquet database
    if parquet_dir is not None:
        epoch_time = int(time.time())
        ppi_net.to_parquet(f'{parquet_dir}/{epoch_time}.parquet', index=None)
        logging.info(f'Saved all PPIs before filtering on pDockQ to {output_dir}all_ppis_unfiltered.csv')

    return


def _consolidate_dockfold_pdb_files(
    dockfold_job:DockFoldJob):

    from src.utils.utils import create_directory
    import subprocess

     # Location of result file parent
    output_dir = dockfold_job.output_dir

    # Location of result file parent
    pdb_dir = dockfold_job.pdb_dir

    if pdb_dir is not None:
        create_directory(pdb_dir)
        cmd = [
            'mv '
            f'{output_dir}/pred*/*.pdb '
            f'{pdb_dir}'
        ]
    else:
        local_pdb = f'{output_dir}/pdb_files'
        create_directory(local_pdb)
        cmd = [
            'mv '
            f'{output_dir}/pred*/*.pdb '
            f'{local_pdb}'
        ]

    subprocess.Popen(cmd, shell=True).wait()
    return


def dockfold_from_msa_job(
    dockfold_job:DockFoldJob):

    # GPU based folding model
    _dockfold_modeling(dockfold_job)

    # Consolidate result table
    _consolidate_dockfold_results(dockfold_job)

    # Consolidate PDB files
    _consolidate_dockfold_pdb_files(dockfold_job)
    
    return