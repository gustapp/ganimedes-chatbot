import model.kb.OpenKE.config as config
import model.kb.OpenKE.models as models
import tensorflow as tf
import numpy as np
import json
import pandas as pd
import pickle
from flask import jsonify
from fuzzywuzzy import process

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

def explain_instance(head, r, response, con=con):
    """ Explanation Engine
    """
    eh_id = entity2id[head]['id']
    r_id = relation2id[r]['id']
    res_id = entity2id[response]['id']
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
    noise_rate = 0.03

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
    for rel_id in list(map(lambda x: x['id'], relation2id.values())):
        feat_candidates_per_relation = con.predict_tail_entity(h=head_ent, r=rel_id, k=k_nn)
        feats_tb.append((ke_rel[rel_id], [(ent_id, ke_ent[ent_id]) for ent_id in feat_candidates_per_relation]))

    # discover interpretable features for noised set
    e_hat_feats = []
    for rel, k_tails in feats_tb:
        labels = []
        for e_fake in e_hat:
            dist_per_inst = []
            id_per_inst = []
            # identify nearest entity to inference
            for tail_id, tail_cand in k_tails:
                dist = np.mean(abs(e_fake + rel - tail_cand))
                dist_per_inst.append(dist)
                id_per_inst.append(tail_id)
            # Hit @1
            tail = id_per_inst[dist_per_inst.index(min(dist_per_inst))]
            labels.append(tail)
        e_hat_feats.append(labels)
        print(str(len(e_hat_feats)))

    # build local dataset
    feats_names = relation2id.keys()
    e_hat_feats_df = pd.DataFrame(data=list(map(list,zip(*e_hat_feats))), columns=feats_names)
    intrp_df = e_hat_feats_df.applymap(lambda x: id2entity[x]['entity']) # DEBUG

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
        intrp_label += map(lambda x: '{}:{}'.format(column, x), list(le.classes_))

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
    logreg = LogisticRegression(C=0.1, penalty='l1')
    # logreg = LogisticRegression()
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
    return exp_df.head(10)
