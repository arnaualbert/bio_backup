"""
Mock Exam (2023-02-24)

Write your name, surname and dni.
"""

name:    str = 'John'
surname: str = 'Smith'
dni:     str = 123456789

assert name,    'Please write your name'
assert surname, 'Please write your surname'
assert dni,     'Please write your dni'


import re
import json
from   pathlib import Path

import pandas as pd

from Bio            import SeqIO
from Bio.SeqRecord  import SeqRecord
from Bio.SeqFeature import SeqFeature
from Bio.Align      import PairwiseAligner, PairwiseAlignments, PairwiseAlignment, substitution_matrices

from Bio.Align.substitution_matrices import Array


# Question 1
# - The "data/rs53576-snpedia.txt" file contains the text from https://www.snpedia.com/index.php/Rs53576
# - Extract all PubMed IDs and URLs and write them to a csv file called "q1.csv".
# - There must be no repeated PubMed IDs and IDs must be sorted alphabetically.
# - Notes:
#   - Only PubMed IDs and URLs. URLs must not contain the query part after the question mark.
#   - Look at the solution for the column names and format.
#   - Pytest will compare the results and they must be identical.
# ---------------------------------------------------------------------
def q1(snp_file: Path) -> pd.DataFrame:

    # Read  the file
    rs53576_str: str = snp_file.read_text()

    # Build regex
    txt: str        = rs53576_str
    reg: str        = r'\[PMID (\d{1,})\n<(https://www.ncbi.nlm.nih.gov/pubmed/\1)'
    pat: re.Pattern = re.compile(reg)

    # Get matches
    match_list:   list[re.Match] = list(pat.finditer(txt))
    id_list:      list[str]      = sorted(set([match.group(1) for match in match_list]))
    url_list:     list[str]      = sorted(set([match.group(2) for match in match_list]))
    #set quita duplicados
    # Build dict
    rs53576_dict: dict[str, str] = { 'id' : id_list,
                                     'url': url_list }

    # Put matches into a Pandas DataFrame
    rs53576_df: pd.DataFrame = pd.DataFrame(rs53576_dict)

    return rs53576_df


# Question 2
# - Read the following two files
#   - SARS-CoV-2 reference: NC_045512.2.genbank
#   - SARS-CoV-2 variant:   OL466363.1.genbank
# - Return the name of the genes in each file (two lists of strings)
# - Return if they have the same genes (bool)
# ---------------------------------------------------------------------
def q2(reference_file: Path, variant_file: Path) -> tuple[list, list, bool]:

    # Read files
    reference_record: SeqRecord = SeqIO.read(reference_file, 'genbank')
    variant_record:   SeqRecord = SeqIO.read(variant_file,   'genbank')

    # Filter features by type
    ref_gene_feat_list: list[SeqFeature] = [feature
                                            for feature
                                            in  reference_record.features
                                            if  feature.type == 'gene']

    var_gene_feat_list: list[SeqFeature] = [feature
                                            for feature
                                            in  variant_record.features
                                            if  feature.type == 'gene']

    ref_gene_list: list[str] = [feature.qualifiers['gene'][0]
                                for feature
                                in ref_gene_feat_list]

    var_gene_list: list[str] = [feature.qualifiers['gene'][0]
                                for feature
                                in var_gene_feat_list]

    same_genes: bool = (ref_gene_list == var_gene_list)

    return ref_gene_list, var_gene_list, same_genes



# ---------------------------------------------------------------------
def q3_align(reference_prot: str, variant_prot: str) -> PairwiseAlignment:

    # Create Global Aligner
    aligner: PairwiseAligner = PairwiseAligner()

    # Get BLOSUM62 matrix
    blosum62_matrix: Array = substitution_matrices.load('BLOSUM62')
    # PAM (PARA PROTEINAS BLOSUM)
    #(LOCAL PARA DOS PROTEINES CON LONGITUD MUY DIFERENTE)
    #GLOBAL PARA LONGITUD GLOBAL
    # Put the matrix in the aligner.
    aligner.substitution_matrix = blosum62_matrix
    
    # Get first global alignment
    alignments: PairwiseAlignments = aligner.align(reference_prot, variant_prot)
    alignment:  PairwiseAlignment  = alignments[0]

    return alignment


# Question 3
# - Read the same two files as in Q2:
#   - SARS-CoV-2 reference: NC_045512.2.genbank
#   - SARS-CoV-2 variant:   OL466363.1.genbank
# - Return a dict with the following contents:
#   - keys:   protein identifier
#   - values: protein alignment (reference vs variant)
# - Align proteins from the genes in Q2 whose length is less than 80 AA.
# ---------------------------------------------------------------------
def q3(reference_file: Path, variant_file: Path) -> dict[str, PairwiseAlignment]:

    # Read files
    reference_record: SeqRecord = SeqIO.read(reference_file, 'genbank')
    variant_record:   SeqRecord = SeqIO.read(variant_file,   'genbank')

    # Filter features by type
    ref_cds_feat_list: list[SeqFeature] = [ feature for feature in reference_record.features
                                            if (feature.type == 'CDS')
                                            and (len(feature.qualifiers['translation'][0]) < 80)]

    var_cds_feat_list: list[SeqFeature] = [ feature for feature in variant_record.features
                                            if feature.type == 'CDS'
                                            and (len(feature.qualifiers['translation'][0]) < 80)]

    # Extract protein names
    prot_names: list[str] = [   feature.qualifiers['protein_id'][0]
                                for feature
                                in  ref_cds_feat_list ]

    # Extract proteins
    ref_prot_list: list[str] = [feature.qualifiers['translation'][0]
                                for feature
                                in  ref_cds_feat_list ]

    var_prot_list: list[str] = [feature.qualifiers['translation'][0]
                                for feature
                                in var_cds_feat_list ]

    # Creat dict
    result: dict[str, PairwiseAlignment] = {prot_name: q3_align(ref_prot, var_prot)
                                            for prot_name, ref_prot, var_prot
                                            in  zip(prot_names, ref_prot_list, var_prot_list)
    }

    print(prot_names)
    print(ref_prot_list)
    print(ref_cds_feat_list)
    return result


# Main
# ---------------------------------------------------------------------
def main():

    # Constants
    current_dir: Path = Path(__file__).parent

    # Question 1
    q1_snp_file:  Path = current_dir/'data'/'rs53576-snpedia.txt'

    q1_result_df: pd.DataFrame = q1(q1_snp_file)

    q1_csv_file:  Path = current_dir/'answers'/'q1.csv'
    q1_result_df.to_csv(q1_csv_file, index=False)


    # Question 2
    q2_reference_file: Path = current_dir/'data'/'NC_045512.2.genbank'
    q2_variant_file:   Path = current_dir/'data'/'OL466363.1.genbank'

    q2_result: tuple[list, list, bool] = q2(q2_reference_file, q2_variant_file)

    json_str:     str  = json.dumps(q2_result, indent=4)
    q2_json_file: Path = current_dir/'answers'/'q2.json'
    q2_json_file.write_text(json_str)


    # Question 3
    q3_reference_file: Path = current_dir/'data'/'NC_045512.2.genbank'
    q3_variant_file:   Path = current_dir/'data'/'OL466363.1.genbank'

    q3_result: dict[str, PairwiseAlignment] = q3(q3_reference_file, q3_variant_file)

    alignments:     str  = ''.join( f"{prot_name}:\n{alignment}\n\n" for prot_name, alignment in q3_result.items() )
    q3_output_file: Path = current_dir/'answers'/'q3.alignments'
    q3_output_file.write_text(alignments)


# ---------------------------------------------------------------------
this_module: str = __name__
main_module: str = "__main__"

if (this_module == main_module): main()
# ---------------------------------------------------------------------
