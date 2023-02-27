import json
import pprint
from Bio import Entrez

Entrez.email = 'arnaualbert2003@gmail.com'


handle = Entrez.einfo()
res = handle.read()
handle.close()
print(res)
# type(handle)
# file_handle = open('tikitaka.py', 'r')
# type(file_handle)
# file_handle.close()

with Entrez.einfo() as response:
    dbs_xml_bin = response.read()
print(dbs_xml_bin)

with Entrez.einfo() as response:
    dbs_dict = Entrez.read(response)

print(dbs_dict)
print(dbs_dict.keys())
print(dbs_dict['DbList'])

#json 
with Entrez.einfo(retmode='json') as response:
    dbs_json_str = response.read().decode('utf-8')

with open('dbs.json', 'w') as json_file:
    json_file.write(dbs_json_str)

with open('dbs.json', 'r') as json_file:
    dbs_dict_from_json = json.load(json_file)

#same but with xml
with Entrez.einfo(retmode='xml') as response:
    dbs_xml_bin_str = response.read()

with open('dbs.xml', 'wb') as xml_file:
    xml_file.write(dbs_xml_bin_str)

with open('dbs.xml', 'rb') as xml_file:
    dbs_dict_from_xml = Entrez.read(xml_file)

print(dbs_dict_from_json == dbs_dict_from_xml)
print(dbs_dict_from_json['einforesult']['dblist'])
print(dbs_dict_from_xml['DbList'])



with Entrez.einfo(db='nucleotide') as response:
    nuc_db_xmml_str = response.read()
    with open('nucleotide.xml', 'wb') as xml_file:
        xml_file.write(nuc_db_xmml_str)

with open('nucleotide.xml', 'rb') as xml_file:
    nuc_db = Entrez.read(xml_file)

print(type(nuc_db))
print(len(nuc_db))
print(nuc_db.keys())
print(nuc_db['DbInfo'].keys())
print(nuc_db['DbInfo']['Description'])
print(nuc_db['DbInfo']['Count'])
print(nuc_db['DbInfo']['LastUpdate'])

print(nuc_db['DbInfo']['FieldList'])
print(nuc_db['DbInfo']['FieldList'][0])

pp = pprint.PrettyPrinter(indent=4)
for field in nuc_db['DbInfo']['FieldList']:
    pp.pprint(field)
    print()