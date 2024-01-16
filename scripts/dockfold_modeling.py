import sys
import argparse
import logging
sys.path.append('/app/')
from src.run_alphafold_single import main
# Description and Configurations
logging.getLogger().setLevel(logging.INFO)
parser = argparse.ArgumentParser(description='Dockfold Modeling Wrapper')

# Add the arguments
parser.add_argument(
    '--num-ensemble',
    type=int,
    default=1,
    help='Number or structure ensembles (default: %(default)s)'
)

parser.add_argument(
    '--complex-id',
    type=str,
    required=True,
    help='Name of complex'
)

parser.add_argument(
    '--max-recycles',
    type=int,
    default=20,
    help='Number or optimization cycles (default: %(default)s)'
)

parser.add_argument(
    '--data-dir',
    type=str,
    default='/opt/data',
    help='Path to DockFold pre-trained models (default: %(default)s)'
)

parser.add_argument(
    '--msa-one',
    type=str,
    required=True,
    help='MSA one to compare against'
)

parser.add_argument(
    '--msa-two',
    type=str,
    required=True,
    help='MSA two to compare against'
)

parser.add_argument(
    '--output-dir',
    type=str,
    required=True,
    help='root data output path for temporary files'
)


if __name__ == '__main__':
    # Execute the parse_args() method
    args = parser.parse_args()

    msa_job = main(
        num_ensemble=args.num_ensemble,
        complex_id=args.complex_id,
        max_recycles=args.max_recycles,
        data_dir=args.data_dir,
        msa1=args.msa_one,
        msa2=args.msa_two,
        output_dir=args.output_dir
    )