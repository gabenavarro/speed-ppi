from dataclasses import dataclass
from typing import OrderedDict, Optional, List

@dataclass
class MsaJob(OrderedDict):
    fasta_file: str
    fasta_path: Optional[str] = None
    id_seq_file: Optional[str] = None
    uniclust: Optional[str] = None
    msa_path: Optional[str] = None
    hhblits_cores: Optional[int] = None


@dataclass
class DockFoldJob(OrderedDict):
    output_dir: Optional[int]
    msa_list_one: Optional[List[str]]
    msa_list_two: Optional[List[str]] = None
    msa_path: Optional[str] = None
    pdb_dir: Optional[str] = None
    parquet_dir: Optional[str] = None
    data_dir: Optional[str] = '/opt/data'
    max_recycles: Optional[str] = 20