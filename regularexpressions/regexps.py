import re
from pathlib import Path

def finiter_example():
    
    txt:str = 'Hola\nAdios\nPep\nTiki'
    reg:str = r'(\w+)\n(\w+)'
    pat: re.Pattern = re.compile(reg)
    pat.finditer(txt)

    match_list: list[re.Match] = list(pat.finditer(txt))
    #: re.Match = match_list[0]

    for match in match_list:
        print(f'start: {match.start()}')
        print(f'end: {match.end()}')
        print(f'whole match: \n{match.group(0)}')
        print(f'first group: {match.group(1)}')
        print(f'second group: {match.group(2)}')
        print('---------------------')

def sub_example():

    txt:str = 'Hola\nAdios\nPep\nTiki'
    reg:str = r'(\w+)\n(\w+)'
    pat: re.Pattern = re.compile(reg)
    new_txt = pat.sub('buenas',txt)

    print(new_txt)


def fasta():
    txt = Path('/bio/data/example.fasta').read_text()
    reg:str = r'.{0,}'
    pat: re.Pattern = re.compile(reg)

    match_list: list[re.Match] = list(pat.finditer(txt))

    match_list.pop(0)

    line_list: list[str] = [match.group(0) for match in match_list]

    seq = ''.join(line_list)
    
    print(seq)



def main():
    
    finiter_example()
    sub_example()
    fasta()



if __name__ == '__main__':

    main()