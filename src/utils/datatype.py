from typing import Optional, Any
from pydantic import BaseModel, field_validator, model_validator
from os.path import exists, isfile
from os import listdir
import logging

class MsaJob(BaseModel):
    fasta_file: str
    fasta_path: Optional[str] = None
    id_seq_file: Optional[str] = None
    uniclust: Optional[str] = None
    msa_path: Optional[str] = None
    hhblits_cores: Optional[int] = None


    field_validator('fasta_file')
    @classmethod
    def fasta_file_validation(cls, value:str)->str:
        if not isfile(value):
            raise ValueError(f"Provided fasta files does not exist: {value}")
        return value

    field_validator('msa_path')
    @classmethod
    def msa_path_validation(cls, value:str)->str:
        if not exists(value):
            raise ValueError(f"Provided msa_path does not exist: {value}")
        return value
    
    field_validator('uniclust')
    @classmethod
    def uniclust_validation(cls, value:str)->str:
        if not exists(value.rsplit("/",1)[[0]]):
                raise ValueError(f"Provided uniclust path does not exist: {value}")
        if not isfile(f"{value}.cs219"):
                return ValueError(f"Provided uniclust path does not have data: {value}.cs219")
        return value
        

class DockFoldJob(BaseModel):
    output_dir: Optional[str]
    list_one: Optional[str]
    list_two: Optional[str] = None
    msa_path: Optional[str] = None
    pdb_dir: Optional[str] = None
    parquet_dir: Optional[str] = None
    data_dir: Optional[str] = '/opt/data'
    max_recycles: Optional[str] = 10

    field_validator('msa_path')
    @classmethod
    def msa_path_validation(cls, value:str)->str:
        if not exists(value):
            raise ValueError(f"Provided msa_path does not exist: {value}")
        return value
    
    field_validator('data_dir')
    @classmethod
    def data_dir_validation(cls, value:str)->str:
        if not exists(value.rsplit("/",1)[[0]]):
            raise ValueError(f"Provided data_dir path does not exist: {value}")
        if not isfile(f"{value}/params/params_model_1.npz"):
            return ValueError(f"Provided data_dir path does not have model: {value}/params/params_model_1.npz")
        return value

    model_validator(mode="after")
    def list_one_model_validation(self)->'DockFoldJob':
        path = self.msa_path
        proteins = self.list_one.split(',')
        validated_proteins = [i for i in proteins if isfile(f"{path}/{i}.a3m")]
        missing_proteins = [i for i in proteins if i not in validated_proteins]
        # Raise error if no proteins have MSA files
        if not validated_proteins:
            raise ValueError(f"None of list one proteins have msa files, please run hhblist first:\n{proteins}")
        # Raise warning if some proteins have no MSA files
        if missing_proteins:
            logging.warning("Following proteins missing msa file and will be excluded: %s"%(",".join(missing_proteins)))
        self.list_one = ','.join(validated_proteins)
        return self
    
    model_validator(mode="after")
    def list_two_model_validation(self)->'DockFoldJob':
        path = self.msa_path
        if self.list_two:
            proteins = self.list_two.split(',')
            validated_proteins = [i for i in proteins if isfile(f"{path}/{i}.a3m")]
            missing_proteins = [i for i in proteins if i not in validated_proteins]
            # Raise error if no proteins have MSA files
            if not validated_proteins:
                raise ValueError(f"None of list two proteins have msa files, please run hhblist first:\n{proteins}")
            # Raise warning if some proteins have no MSA files
            if missing_proteins:
                logging.warning("Following list two proteins missing msa file and will be excluded: %s"%(",".join(missing_proteins)))
            self.list_two = ','.join(validated_proteins)
        return self