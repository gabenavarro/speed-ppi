import sys
import argparse
import logging
from typing import List
from ast import literal_eval
sys.path.append('/app/')
from src.utils.datatype import DockFoldJob
from src.utils.dockfold import dockfold_from_msa_job
# Description and Configurations
logging.getLogger().setLevel(logging.INFO)
parser = argparse.ArgumentParser(description='Dockfold Modeling')

# Add the arguments
parser.add_argument(
    '--output-dir',
    type=str,
    required=True,
    help='root data output path for temporary files'
)

parser.add_argument(
    '--list-one',
    type=str,
    default=None,
    required=True,
    help='List of MSAs to compare again. Will do all against all if no `msa_list_two` provided.'
)

parser.add_argument(
    '--list-two',
    type=str,
    default=None,
    help='List of MSAs to compare against `msa_list_one`. Default is None. If provided, will only do protein in list two againt proteins in list one.'
)

parser.add_argument(
    '--msa-path',
    type=str,
    default=None,
    help='Path to MSA files'
)

parser.add_argument(
    '--pdb-dir',
    type=str,
    default=None,
    help='Path to output pdb files. If none, will auto-generate pdb path in output-dir'
)

parser.add_argument(
    '--parquet-dir',
    type=str,
    default=None,
    help='Path write Dockfold analysis result table.'
)

parser.add_argument(
    '--data-dir',
    type=str,
    default='/opt/data',
    help='Path to DockFold pre-trained models (default: %(default)s)'
)


parser.add_argument(
    '--max_recycles',
    type=int,
    default=10,
    help='Number or optimization cycles (default: %(default)s)'
)

if __name__ == '__main__':
    # Execute the parse_args() method
    args = parser.parse_args()

    # Clean up list arguments
    msa_list_one = args.list_one.split(",")
    msa_list_two = args.list_two if args.list_two == None else args.list_two.split(",")

    # Create DockFold Job
    msa_job = DockFoldJob(
        output_dir=args.output_dir,
        list_one=msa_list_one,
        list_two=msa_list_two,
        msa_path=args.msa_path,
        pdb_dir=args.pdb_dir,
        parquet_dir=args.parquet_dir,
        data_dir=args.data_dir,
        max_recycles=args.max_recycles,
    )
    # Get jobs
    dockfold_from_msa_job(msa_job)