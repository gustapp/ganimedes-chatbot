""" Load Dictionaries: 
    * relation2id
    * entity2id
"""
entity2id_path = './benchmarks/USPedia/entity2id.txt'
relation2id_path = './benchmarks/USPedia/relation2id.txt'

import pandas as pd
e2i_df = pd.read_csv(entity2id_path, sep='\t', header=None, skiprows=[0])
e2i_df.columns = ['entity', 'id']

entity2id = e2i_df.set_index('entity').T.to_dict()
id2entity = e2i_df.set_index('id').T.to_dict()

# entities = [(x, x.replace('_', ' ').replace('category', '').replace('categoria', '')) for x in entity2id.keys()]

# entities_format = []
# entities = []
# for entity_name in entity2id.keys():
#     if len(entity_name) < 40:
#         entities.append(entity_name.replace('_', ' ').replace('category:', '').replace('categoria:', ''))
#         entities_format.append(entity_name)

r2i_df = pd.read_csv(relation2id_path, sep='\t', header=None, skiprows=[0])
r2i_df.columns = ['relation', 'id']

relation2id = r2i_df.set_index('relation').T.to_dict()

import pickle
with open('../artifacts/dicts/entity2id.pkl', 'wb') as output:  # Overwrites any existing file.
    pickle.dump(entity2id, output, pickle.HIGHEST_PROTOCOL)
with open('../artifacts/dicts/id2entity.pkl', 'wb') as output:  # Overwrites any existing file.
    pickle.dump(id2entity, output, pickle.HIGHEST_PROTOCOL)
with open('../artifacts/dicts/relation2id.pkl', 'wb') as output:  # Overwrites any existing file.
    pickle.dump(relation2id, output, pickle.HIGHEST_PROTOCOL)
    