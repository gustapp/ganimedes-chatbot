import model.kb.OpenKE.config as config
import model.kb.OpenKE.models as models
import tensorflow as tf
import numpy as np
import json
import pandas as pd
import pickle
from collections import Counter
from flask import jsonify
from fuzzywuzzy import process
from time import time
import pandas as pd

""" Load TransE USPedia Knowledge Embedding """
from os import path
root = path.dirname(path.abspath(__file__))

con = config.Config()

kb_path = path.join(root, 'OpenKE/benchmarks/USPedia/')
ke_path =  path.join(root, 'artifacts/kge/model.vec.tf')

con.set_in_path(kb_path)
con.set_work_threads(8)
con.set_dimension(500)
con.set_import_files(ke_path)
con.init()
con.set_model(models.TransE)

# preprocessed dictionaries pickles
entity2id_pkl = path.join(root, 'artifacts/dicts/entity2id.pkl')
id2entity_pkl = path.join(root, 'artifacts/dicts/id2entity.pkl')
relation2id_pkl = path.join(root, 'artifacts/dicts/relation2id.pkl')

graph_pkl = path.join(root, 'artifacts/graph_con.pkl')

# load dictionaries
with open(entity2id_pkl, "rb") as input_file:
   entity2id = pickle.load(input_file)
with open(id2entity_pkl, "rb") as input_file:
   id2entity = pickle.load(input_file)
with open(relation2id_pkl, "rb") as input_file:
   relation2id = pickle.load(input_file)

entities_format = []
entities = []
for entity_name in entity2id.keys():
    if len(entity_name) < 40:
        entities.append(entity_name.replace('_', ' ').replace('category:', '').replace('categoria:', ''))
        entities_format.append(entity_name)

# # Load Graph
# with open(relation2id_pkl, "rb") as input_file:
#    relation2id = pickle.load(input_file)

# """ ***Experiment*** """
# id2relation = ['subject', 'involved', 'broader']
# graph_df = pd.read_csv('./functions/src/model/kb/OpenKE/benchmarks/USPedia/train2id.txt', sep='\t', header=None, skiprows=[0], names=['head', 'tail', 'relation'])
# # graph_df['head'] = graph_df['head'].apply(lambda x: id2entity[x])
# # graph_df['tail'] = graph_df['tail'].apply(lambda x: id2entity[x])
# # graph_df['rel'] = graph_df['rel'].apply(lambda x: id2relation[x])

# relations = [(x+1) for x in [x['id'] for x in relation2id.values()]]
# relations_inv = [-(x+1) for x in [x['id'] for x in relation2id.values()]]
# #entity_dict = dict(zip(id2entity.keys(), [[] for i in range(len(id2entity.keys()))]))
# graph_dict = dict(zip(relations + relations_inv, [dict(zip(id2entity.keys(), [[] for i in range(len(id2entity.keys()))])) for i in range(len(relations + relations_inv))]))

# for index, triple in graph_df.iterrows():
#     head, tail, relation = triple
#     graph_dict[relation+1][head].append(tail) # direct
#     graph_dict[-(relation+1)][tail].append(head) # inverse

class KnowledgeGraph(object):
    def __init__(self, graph_dict):
        self.graph = graph_dict

    def predict_head_entity(self, t, r, k):
        return self.graph[-(r+1)][t][:k]

    def predict_tail_entity(self, h, r, k):
        return self.graph[r+1][h][:k]

with open(graph_pkl, "rb") as input_file:
   graph_con = pickle.load(input_file)

# graph_con = KnowledgeGraph(graph_dict)
# # graph_con = KnowledgeGraph({})

# with open('./graph_con.pkl', 'wb') as output:  # Overwrites any existing file.
#     pickle.dump(graph_con, output, pickle.HIGHEST_PROTOCOL)

class InferenceEngine(object):
    """ Knowledge Embedding predictor.
    """
    def __init__(self, ke, entity2id, id2entity, relation2id, entities, entities_format):
        """ Constructor
            Args:
                ke (openKe config): knowledge embedding
                entity2id (dict): mapping from id to entity
                id2entity (dict): mapping from entity to id
                relation2id (dict): mapping from id to relation
        """
        self.ke = ke
        self.entity2id = entity2id
        self.id2entity = id2entity
        self.relation2id = relation2id
        self.entities = entities
        self.entities_format = entities_format

    def entity_name_recognition(self, name):
        """ Fuzzy name matching for user 
            query concept and KB entity.
        """
        return process.extract(name.replace('_', ' '), self.entities, limit=3)

    def predict_course_rank(self, concept, top_n=5000, relation=0):
        """ Predict plausibility scores for each learning-object (course and article)
            in the Knowledge Base and returns the top n.
        """
        concept_id = self.entity2id[concept]['id']
        predicted_ids = self.ke.predict_head_entity(t=concept_id, r=relation, k=top_n)

        # return courses only
        return [x.upper() for x in [self.id2entity[id]['entity'] for id in predicted_ids] if len(x) == 7]

# Initialize the knowledge graph embedding inference engine
ranker_kge = InferenceEngine(con, entity2id, id2entity, relation2id, entities, entities_format)

def rank_content(theme, ranker=ranker_kge):
    """ Logic behind the course ranking by theme. 
    """
    # concepts_cand = ranker_kge.entity_name_recognition(theme)

    # best_candidates = []
    # for candidate, score in concepts_cand:
    #     if score > 90:
    #         best_candidates.append(candidate)

    best_candidates = [theme]

    if len(best_candidates) == 1: # is resolved
        return ranker_kge.predict_course_rank(theme)
    elif len(best_candidates) > 1: # too many good candidates
        raise Exception('too many candidates')
    else: # no candidate
        return []

def embd_graph_walk(node, targets, path_ref, branch_factor, k, visited_nodes_ref=[], con=con):
    """ Depth-First Search
    """
    visited_nodes = [x for x in visited_nodes_ref]
    visited_nodes.append(node) # add actual node to visited list
    path = [x for x in path_ref]
    if len(path) == 0:
        # if node == target: # solution
        if node in targets: # solution
            k[targets.index(node)][0] -= 1
        return [[node, time()]] # elapsed time to find explanation
    if len(path) == 1: # explode leafs nodes
        branch_factor = 500
    rel = path.pop()
    if rel < 0: # inverse relation
        edges = con.predict_head_entity(t=node, r=abs(rel)-1, k=branch_factor)
        if len(path) == 0: # leaf branch (type constrained)
            edges = [entity2id[x]['id'] for x in [id2entity[id]['entity'] for id in edges] if len(x) == 7]
    else: # direct relation
        edges = con.predict_tail_entity(h=node, r=rel-1, k=branch_factor)

    merged = []
    for edge in edges:
        if edge not in visited_nodes and (edge not in targets or len(path) == 0): # avoid cycles
        # if edge != node:
            partial_paths = embd_graph_walk(edge, targets, path, branch_factor, k, visited_nodes, con=con)
            for partial_path in partial_paths:
                merged.append([node] + partial_path)
        # if k[0] == 0: # cutoff (number of explanations is satisfied)
        if all([x[0] == 0 for x in k]): # cutoff (number of explanations is satisfied)
            return merged
    return merged

def explain_instance(head, r, response, algo_type, con=con):
    """ Crossover """

    eh_id = entity2id[head]['id']
    r_id = relation2id[r]['id']
    res_id = [entity2id[x]['id'] for x in response]

    # Don't remove!!!
    con.restore_tensorflow()

    reasons = []
    # for algo in ['TRUE']:
    for algo in [algo_type]:
        start_time = time()
        # Search for crossover interactions
        expl_n = [[1] for i in range(len(res_id))]
        k_nn = 8
        expl_inst = []
        for expl_path in [[3,-3,-1], [-1,-2, 2]]:
            list.reverse(expl_path)
            if algo == 'PRED':
                paths = embd_graph_walk(eh_id, res_id, expl_path, k_nn, expl_n)
            elif algo == 'TRUE':
                paths = embd_graph_walk(eh_id, res_id, expl_path, k_nn, expl_n, con=graph_con)
            expl_res = []
            for path in paths:
                if any([x for x in res_id if x in path]):
                    elapsed_time = path.pop() - start_time
                    expl_res.append((elapsed_time, [id2entity[y]['entity'] for y in path]))
            #expl_res = [[id2entity[y]['entity'] for y in x] for x in paths if res_id in x]
            if len(expl_res) == 0: # empty
                continue
            expl_inst.append((expl_path, expl_res))
            if expl_n[0] == 0:
                break
        reasons.append((algo, expl_inst))
    return reasons
