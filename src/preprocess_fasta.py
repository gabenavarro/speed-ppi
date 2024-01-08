def read_fasta(
    fasta_file:str):
    """Read a fasta file int dataframe
    """

    from pandas import DataFrame

    ids = []
    seqs = []

    with open(fasta_file, 'r') as file:
        current_sequence = ''
        current_id = ''

        for line in file:
            line = line.strip()
            if line.startswith('>'):
                # Save the previous sequence and ID
                if current_sequence and current_id:
                    
                    ids.append(current_id)
                    seqs.append(current_sequence)

                # Get the new ID
                # Remove the '>' character
                # current_id = current_id 
                current_id = line[1:].split('|')[0].strip()  
                current_sequence = ''
            else:
                current_sequence += line

        # Append the last sequence and ID
        if current_sequence and current_id:
            ids.append(current_id)
            seqs.append(current_sequence)

    # Create a DataFrame
    fasta_df = DataFrame({'ID': ids, 'sequence': seqs})
    return fasta_df

def write_fasta(fasta_df, outdir):
    """Write individual fasta files
    """

    for _, row in fasta_df.iterrows():
        with open(f'{outdir}/{row.ID}.fasta', 'w') as file:
            file.write(f'>{row.ID}\n')
            file.write(row.sequence)


def write_fasta_file_from_fasta_df(fasta_df, fasta_file):
    """Write individual fasta files
    """
    with open(fasta_file, 'w') as file:
        for _, row in fasta_df.iterrows():
            file.write(f'>{row.ID}\n')
            file.write(f'{row.sequence}\n')