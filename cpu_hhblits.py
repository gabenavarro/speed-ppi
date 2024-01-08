import sys
import argparse
import logging
sys.path.append('/app/')
from src.utils.jobs import MsaJob
from src.utils.msa import hhblits_msa_from_msa_job
# Description and Configurations
logging.getLogger().setLevel(logging.INFO)
parser = argparse.ArgumentParser(description='Dockfold HHBlits')

# Add the arguments
parser.add_argument(
    '--fasta-file',
    type=str,
    required=True,
    help='Fasta file with proteins sequences for Dockfold analysis'
)

parser.add_argument(
    '--fasta-path',
    type=str,
    default=None,
    help='Chunk size (default: %(default)s)'
)

parser.add_argument(
    '--id-seq-file',
    type=str,
    default=None,
    help='Chunk size (default: %(default)s)'
)

parser.add_argument(
    '--uniclust',
    type=str,
    default='/opt/uniclust30_2018_08',
    help='Path to uniclust30 data (default: %(default)s). Change default value if in cloud environment.'
)

parser.add_argument(
    '--msa-path',
    type=str,
    default='/opt/dockfold_msa',
    help='Path to MSA files (default: %(default)s). Change default value if in cloud environment.'
)

parser.add_argument(
    '--hhblits-cores',
    type=int,
    default=None,
    help='Chunk size (default: %(default)s)'
)

if __name__ == '__main__':
    # Execute the parse_args() method
    args = parser.parse_args()

    msa_job = MsaJob(
        fasta_file=args.fasta_file,
        fasta_path=args.fasta_path,
        id_seq_file=args.id_seq_file,
        uniclust=args.uniclust,
        msa_path=args.msa_path,
        hhblits_cores=args.hhblits_cores
    )

    # Get jobs
    hhblits_msa_from_msa_job(msa_job)