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

""" ***Experiment*** """
id2relation = ['subject', 'involved', 'broader']
graph_df = pd.read_csv('./functions/src/model/kb/OpenKE/benchmarks/USPedia/train2id.txt', sep='\t', header=None, skiprows=[0], names=['head', 'tail', 'relation'])
# graph_df['head'] = graph_df['head'].apply(lambda x: id2entity[x])
# graph_df['tail'] = graph_df['tail'].apply(lambda x: id2entity[x])
# graph_df['rel'] = graph_df['rel'].apply(lambda x: id2relation[x])

relations = [(x+1) for x in [x['id'] for x in relation2id.values()]]
relations_inv = [-(x+1) for x in [x['id'] for x in relation2id.values()]]
#entity_dict = dict(zip(id2entity.keys(), [[] for i in range(len(id2entity.keys()))]))
graph_dict = dict(zip(relations + relations_inv, [dict(zip(id2entity.keys(), [[] for i in range(len(id2entity.keys()))])) for i in range(len(relations + relations_inv))]))

for index, triple in graph_df.iterrows():
    head, tail, relation = triple
    graph_dict[relation+1][head].append(tail) # direct
    graph_dict[-(relation+1)][tail].append(head) # inverse

class KnowledgeGraph(object):
    def __init__(self, graph_dict):
        self.graph = graph_dict

    def predict_head_entity(self, t, r, k):
        return self.graph[-(r+1)][t][:k]

    def predict_tail_entity(self, h, r, k):
        return self.graph[r+1][h][:k]

graph_con = KnowledgeGraph(graph_dict)

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

def graph_walk(node, path_ref, k, con=con):
    path = [x for x in path_ref]
    if len(path) == 0:
        return [node]
    rel = path.pop()
    if rel < 0: # inverse relation
        edges = con.predict_head_entity(t=node, r=abs(rel)-1, k=k)
    else: # direct relation
        edges = con.predict_tail_entity(h=node, r=rel-1, k=k)

    merged = []
    for edge in edges:
        if edge != node:
            merged += graph_walk(edge, path, k)

    return list(set(merged))

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
    if len(path) == 1: # 3-times leafs nodes
        branch_factor = 3*branch_factor
    rel = path.pop()
    if rel < 0: # inverse relation
        edges = con.predict_head_entity(t=node, r=abs(rel)-1, k=branch_factor)
    else: # direct relation
        edges = con.predict_tail_entity(h=node, r=rel-1, k=branch_factor)

    merged = []
    for edge in edges:
        if edge not in visited_nodes and (edge not in targets or len(path) == 0): # avoid cycles
        # if edge != node:
            partial_paths = embd_graph_walk(edge, targets, path, branch_factor, k, visited_nodes)
            for partial_path in partial_paths:
                merged.append([node] + partial_path)
        # if k[0] == 0: # cutoff (number of explanations is satisfied)
        if all([x[0] == 0 for x in k]): # cutoff (number of explanations is satisfied)
            return merged
    return merged

def explain_instance(head, r, response, con=con):
    """ Crossover """

    eh_id = entity2id[head]['id']
    r_id = relation2id[r]['id']
    res_id = [entity2id[x]['id'] for x in response]

    # Don't remove!!!
    con.restore_tensorflow()

    reasons = []
    for algo in ['TRUE', 'PRED']:
        start_time = time()
        # Search for crossover interactions
        expl_n = [[9] for i in range(len(res_id))]
        k_nn = 7
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

def explain_instance_local(head, r, response, con=con):
    """ Explanation Engine
    """
    eh_id = entity2id[head]['id']
    r_id = relation2id[r]['id']
    res_id = entity2id[response]['id']

    # Don't remove!!!
    con.restore_tensorflow()

    # load embedding
    ke = con.get_parameters()

    ke_ent = ke['ent_embeddings']
    ke_rel = ke['rel_embeddings']

    # head entity vector
    eh_vec = ke_ent[eh_id]

    # generate perturbed set of instances
    e = eh_vec
    n_instances = 1000
    dimension = 500
    noise_rate = 0.045
    # noise_rate = 0 # (DEBUG)

    e_hat = []
    for i in range(0, n_instances):
        noise = np.random.normal(0,noise_rate,dimension)
        e_hat.append(e + noise)

    # Minimize search area by choosing only the nearest neighbors
    head_ent = eh_id
    rel = r_id

    k_nn = 5
    feats_tb = []
    # discover head entity features
    for rel_id in [0, [3], [3,-3,-1], [-1,-2]]:
        if rel_id == 0: # subject
            feat_candidates_per_relation = [x for x in con.predict_head_entity(t=head_ent, r=rel_id, k=5000) if len(id2entity[x]['entity']) == 7][:15]
            feat_vec = ke_rel[rel_id]
        else:
            feat_candidates_per_relation = graph_walk(head_ent, rel_id, k_nn)
            feat_vec = [0] * 500
            for feat_rel in rel_id:
                if feat_rel > 0:
                    feat_vec += ke_rel[feat_rel-1]
                else:
                    feat_vec -= ke_rel[abs(feat_rel)-1]
        feats_tb.append((rel_id, feat_vec, [(ent_id, ke_ent[ent_id]) for ent_id in feat_candidates_per_relation]))

    # discover interpretable features for noised set
    e_hat_feats = []
    for rel_id, rel, k_tails in feats_tb:
        labels = []
        # labels = pool.map(feature_extraction, e_hat)
        for e_fake in e_hat:
            dist_per_inst = []
            id_per_inst = []
            # identify nearest entity to inference
            for tail_id, tail_cand in k_tails:
                if rel_id == 0: # subject
                    dist = np.mean(abs(tail_cand + rel - e_fake))
                else:
                    dist = np.mean(abs(e_fake + rel - tail_cand))
                dist_per_inst.append(dist)
                id_per_inst.append(tail_id)
            # Hit @1
            tail = id_per_inst[dist_per_inst.index(min(dist_per_inst))]
            labels.append(tail)
        e_hat_feats.append(labels)
        print(str(len(e_hat_feats)))

    # build local dataset
    feats_names = ['subject', 'broader', 'broader-^broader-^subject', '^subject-^involved-involved']
    e_hat_feats_df = pd.DataFrame(data=list(map(list,zip(*e_hat_feats))), columns=feats_names)
    #intrp_df = e_hat_feats_df.applymap(lambda x: id2entity[x]['entity']) # DEBUG

    # Train Local-Surrogate Model
    
    target_rel = r
    label = res_id

    # replace target tail
    def replace_target(item, label=label):
        if item == label:
            return 1
        else:
            return 0

    df = e_hat_feats_df

    df[target_rel] = df[target_rel].apply(replace_target)
    target = df.pop(target_rel)

    # encode labels to categorical features
    from sklearn.preprocessing import LabelEncoder

    intrp_label = []
    for column in df:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        intrp_label += map(lambda x: '{}:{}'.format(column, x), [id2entity[x]['entity'] for x in le.classes_])

    # encode one hot 
    from sklearn.preprocessing import OneHotEncoder

    ohc = OneHotEncoder()
    out = ohc.fit_transform(df)

    # full set
    X = out
    y = target

    from sklearn.metrics import mean_squared_error, accuracy_score
    from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    # logreg = LogisticRegression(C=0.1, penalty='l1')
    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)

    y_pred = logreg.predict(X_test)
    print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

    from sklearn.metrics import confusion_matrix
    confusion_matrix = confusion_matrix(y_test, y_pred)
    print(confusion_matrix)

    # Feature Importance (why jesus religion is judaism?)
    weights = logreg.coef_
    labels = intrp_label

    exp_df = pd.DataFrame(data={'labels': labels, 'weights': weights[0]})
    exp_df.sort_values('weights', inplace=True, ascending=False)
    return [x[0] for x in exp_df.values]
