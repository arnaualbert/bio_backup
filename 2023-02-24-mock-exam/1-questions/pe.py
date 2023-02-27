"""
Mock Exam (2023-02-24)

Write your name, surname and dni.
"""

name:    str = 'Arnau'
surname: str = 'Albert'
dni:     str = '49949066N'

assert name,    'Please write your name'
assert surname, 'Please write your surname'
assert dni,     'Please write your dni'


# Question 1
# - The "data/rs53576-snpedia.txt" file contains the text from https://www.snpedia.com/index.php/Rs53576
# - Extract all PubMed IDs and URLs and write them to a csv file called "q1.csv".
# - There must be no repeated PubMed IDs and IDs must be sorted alphabetically.
# - Notes:
#   - Only PubMed IDs and URLs. URLs must not contain the query part after the question mark.
#   - Look at the solution for the column names and format.
#   - Pytest will compare the results and they must be identical.
# ---------------------------------------------------------------------
from pathlib import Path
import pandas as pd
import re
import json
def q1(snp_file: Path) -> pd.DataFrame:
  # parse the snp_file  
  read_snp = snp_file.read_text()
  urllist = re.findall(r'<(https://www.ncbi.nlm.nih.gov/pubmed/.+)\?dopt=Abstract>', read_snp)
  # also works: idlist = re.findall(r'<https://www.ncbi.nlm.nih.gov/pubmed/(.+)\?dopt=Abstract>',read_snp)
  idlist = re.findall(r'\[PMID (\d{1,})\n',read_snp)
  sorted_idlist = sorted(set(idlist))
  sorted_urllist = sorted(set(urllist))
  dataframe_id_url = pd.DataFrame({'id': sorted_idlist, 'url': sorted_urllist})
  return dataframe_id_url




# Question 2
# - Read the following two files
#   - SARS-CoV-2 reference: NC_045512.2.genbank
#   - SARS-CoV-2 variant:   OL466363.1.genbank
# - Return the name of the genes in each file (two lists of strings)
# - Return if they have the same genes (bool)
# ---------------------------------------------------------------------
from   Bio      import Entrez
from Bio.Entrez.Parser import DictionaryElement, ListElement
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Entrez.Parser import DictionaryElement, ListElement
from Bio.SeqIO.InsdcIO import GenBankIterator

from Bio.Seq        import Seq
from Bio.SeqFeature import SeqFeature
from Bio.Align      import PairwiseAligner, PairwiseAlignments, PairwiseAlignment, substitution_matrices
from Bio.Align.substitution_matrices import Array
def q2(reference_file: Path, variant_file: Path) -> tuple[list, list, bool]:
  record_reference = SeqIO.parse(reference_file, 'genbank')
  record_variant = SeqIO.parse(variant_file, 'genbank')
  gene_reference = []
  for record in record_reference:
     if record.features:
        for feature in record.features:
          if feature.type == "gene":
            gene = feature.qualifiers["gene"][0]
            gene_reference.append(gene)
  gene_variant = []
  for record in record_variant:
     if record.features:
        for feature in record.features:
          if feature.type == "gene":
            gene = feature.qualifiers["gene"][0]
            gene_variant.append(gene)
  # check if 2 arrrays are the same
  # merged_reference = []
  # merged_variant = []

  # for l in gene_reference:
  #    += l

  # for l in gene_variant:
  #   merged_variant += l
  # same = merged_reference == merged_variant
  same = gene_reference == gene_variant
  # return merged_reference, merged_variant, same

  return gene_reference, gene_variant, same



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
  
  record_reference = SeqIO.parse(reference_file, 'genbank')
  record_variant = SeqIO.parse(variant_file, 'genbank')

  proteine_names = []
  reference_translation = []
  variant_translation = []

  for record in record_reference:
     if record.features:
        for feature in record.features:
          if feature.type == "CDS":
            prot_name = feature.qualifiers["protein_id"][0]
            translation = feature.qualifiers["translation"][0]
            if len(translation) < 80:
              proteine_names.append(prot_name)
          if feature.type == "CDS":
            translation = feature.qualifiers["translation"][0]
            if len(translation) < 80:
              reference_translation.append(translation)

  for record in record_variant:
    if record.features:
      for feature in record.features:
        if feature.type == "CDS":
          translation = feature.qualifiers["translation"][0]
          if len(translation) < 80:
            variant_translation.append(translation)

  aligner: PairwiseAligner = PairwiseAligner()
  ## NEW 
  blosum62_matrix: Array = substitution_matrices.load('BLOSUM62')
  aligner.substitution_matrix = blosum62_matrix
  ###
  result = {}

  for name, seq1,seq2 in zip(proteine_names, reference_translation, variant_translation):
    alignments = aligner.align(seq1, seq2)
    result[name] = alignments[0]



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
