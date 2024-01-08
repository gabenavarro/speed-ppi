from typing import List, Dict, Callable

def create_directory(path:str):
    '''Create directory
    ---

    Create directory if missing

    ### Parameters
        * `path` (str): path to create

    ### Example
    >>> import os
    >>> path = '/new/path/including/new/subdirectories'
    >>> os.path.isdir(path)
    False
    >>> _create_directory(path)
    >>> os.path.isdir(path)
    True
    '''
    import os
    from pathlib import Path
    if not os.path.isdir(path):
        Path(path).mkdir(parents=True, exist_ok=True)
    return


def multicore(
    func: Callable,
    jobs: List,
    cores: int = None):
    from multiprocessing import Pool, cpu_count
    import logging

    # If the number of cores is not specified, use all available cores
    if cores is None:
        cores = cpu_count()
        
    logging.info("------------ Commencing Multicore Processing  -------------")
    logging.info(f'Initializing with {cores} cores')
    p = Pool(cores)
    results = p.map(func, jobs) # p.imap_unordered(func, jobs)
    logging.info("------------ Closing Multicore Processing     -------------")
    return results