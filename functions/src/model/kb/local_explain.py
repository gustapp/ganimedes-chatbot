# """ ENIAC 2019 : Faithfully Explaining Knowledge Embedding Predictions
#     Encontro Nacional de Inteligencia Artificial e Computational 2019

#     Posthoc model-agnostic explanation method for Knowledge Embeddings.
#     It is based on a Local-surrogate (Sparse Logistic Regression) model
#     trained with a noised set of data points artificially generated from
#     a given instance. Similar to LIME (Ribeiro et al, 2016) but adapted 
#     for multi-relational classifiers, such as KEs.
# """
# import numpy as np
# import pandas as pd

# class LocalSurrogate(object):
#     def __init__(self):
#         pass

# class Explainer(object):
#     def __init__(self):
#         pass
#     def explain_instance(self, head, relation, tail):
#         pass
    

# def explain_link_prediction(con, eh_id, r_id, res_id):
#     """ Explanation Engine
#     """
    
#     # load embedding
#     ke = con.get_parameters()

#     ke_ent = ke['ent_embeddings']
#     ke_rel = ke['rel_embeddings']

#     # head entity vector
#     eh_vec = ke_ent[eh_id]

#     # generate perturbed set of instances
#     e = eh_vec
#     n_instances = 500
#     dimension = 100
#     noise_rate = 0.03

#     e_hat = []
#     for i in range(0, n_instances):
#         noise = np.random.normal(0,noise_rate,dimension)
#         e_hat.append(e + noise)

#     # Minimize search area by choosing only the nearest neighbors
#     head_ent = eh_id
#     rel = r_id

#     k_nn = 5
#     feats_tb = []
#     # discover head entity features
#     for rel_id in [0, 3, 6, 12]:
#         feat_candidates_per_relation = con.predict_tail_entity(h=head_ent, r=rel_id, k=k_nn)
#         feats_tb.append((ke_rel[rel_id], [(ent_id, ke_ent[ent_id]) for ent_id in feat_candidates_per_relation]))

#     # discover interpretable features for noised set
#     e_hat_feats = []
#     for rel, k_tails in feats_tb:
#         labels = []
#         for e_fake in e_hat:
#             dist_per_inst = []
#             id_per_inst = []
#             # identify nearest entity to inference
#             for tail_id, tail_cand in k_tails:
#                 dist = np.mean(abs(e_fake + rel - tail_cand))
#                 dist_per_inst.append(dist)
#                 id_per_inst.append(tail_id)
#             # Hit @1
#             tail = id_per_inst[dist_per_inst.index(min(dist_per_inst))]
#             labels.append(tail)
#         e_hat_feats.append(labels)
#         print(str(len(e_hat_feats)))

#     # build local dataset
#     feats_names = ['religion', 'profession', 'nationality', 'ethnicity']
#     e_hat_feats_df = pd.DataFrame(data=list(map(list,zip(*e_hat_feats))), columns=feats_names)
    
#     # Train Local-Surrogate Model
    
#     target_rel = r
#     label = res_id[0]

#     # replace target tail
#     def replace_target(item, label=label):
#         if item == label:
#             return 1
#         else:
#             return 0

#     df = e_hat_feats_df

#     df[target_rel] = df[target_rel].apply(replace_target)
#     target = df.pop(target_rel)

#     # encode labels to categorical features
#     from sklearn.preprocessing import LabelEncoder

#     intrp_label = []
#     for column in df:
#         le = LabelEncoder()
#         df[column] = le.fit_transform(df[column])
#         intrp_label += map(lambda x: '{}:{}'.format(column, x), list(le.classes_))

#     # encode one hot 
#     from sklearn.preprocessing import OneHotEncoder

#     ohc = OneHotEncoder()
#     out = ohc.fit_transform(df)

#     # full set
#     X = out
#     y = target

#     from sklearn.metrics import mean_squared_error, accuracy_score
#     from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
#     from sklearn.linear_model import LogisticRegression
#     from sklearn.model_selection import train_test_split

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
#     logreg = LogisticRegression(C=0.1, penalty='l1')
#     # logreg = LogisticRegression()
#     logreg.fit(X_train, y_train)

#     y_pred = logreg.predict(X_test)
#     print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

#     from sklearn.metrics import confusion_matrix
#     confusion_matrix = confusion_matrix(y_test, y_pred)
#     print(confusion_matrix)

#     # Feature Importance (why jesus religion is judaism?)
#     weights = logreg.coef_
#     labels = intrp_label

#     exp_df = pd.DataFrame(data={'labels': labels, 'weights': weights[0]})
#     exp_df.sort_values('weights', inplace=True, ascending=False)
#     return exp_df.head(10)