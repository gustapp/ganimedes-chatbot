#%% [markdown]
# # LDA Model

#%%
# Latent Dirichlet Allocation
import pandas as pd

df = pd.read_csv('./functions/models/dataset/chatbot-articles.csv', error_bad_lines=False)
data_text = df[['abstract']].dropna()
data_text['index'] = data_text.index
documents = data_text

print(len(documents))
df.head()

#%%
# Pre-processing
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer, PorterStemmer
import numpy as np
np.random.seed(2018)

import nltk
nltk.download('wordnet')

#%%
# Preprocessing methods
def lemmatize_stemming(text):
    stemmer = PorterStemmer()
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

#%%
# Preview a doc before prepocessing

# sample_number = 4310
sample_number = 100

doc_sample = documents[documents['index'] == sample_number].values[0][0]

print('original document: ')
words = []
for word in doc_sample.split(' '):
    words.append(word)
print(words)
print('\n\n tokenized and lemmatized document: ')
print(preprocess(doc_sample))

#%%
# Preprocess all documents
processed_docs = documents['abstract'].map(preprocess)
processed_docs[:10]


#%%
# Create a dictionary from ‘processed_docs’ containing the number of times a word appears in the training set

dictionary = gensim.corpora.Dictionary(processed_docs)

#%%
count = 0
for k, v in dictionary.iteritems():
    print(k, v)
    count += 1
    if count > 10:
        break

#%%
dictionary.token2id['tutor']

#%%
# Filter out tokens that appear in less than 5 docs or more than 0.7 docs
# Keep (at most) only the first 100000 most frequent
dictionary.filter_extremes(no_above=0.3)
len(dictionary.token2id)

#%%
# Gensim doc2bow
# For each document we create a dictionary reporting how many
# words and how many times those words appear
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
bow_corpus[sample_number]

#%%
# Preview BOW for our sample 
bow_doc_sample_number = bow_corpus[sample_number]

for i in range(len(bow_doc_sample_number)):
    print("Word {} (\"{}\") appears {} time.".format(bow_doc_sample_number[i][0], 
            dictionary[bow_doc_sample_number[i][0]], bow_doc_sample_number[i][1]))

#%%
# TF-IDF
# Preview TF-IDF scores for our first doc

from gensim import corpora, models

tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]

from pprint import pprint

for doc in corpus_tfidf:
    pprint(doc)
    break

#%%
# Running LDA using BOW
num_topics = 20
lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=num_topics, id2word=dictionary, \
        alpha=[0.01]*num_topics, eta=[0.01]*len(dictionary.keys()), passes=4, workers=4)

lda_model.save('./functions/src/artifacts/lda_bow/lda_model')

for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))

#%%
# Running LDA using TF-IDF
num_topics = 18
lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=num_topics, id2word=dictionary, \
        alpha=[0.01]*num_topics, eta=[0.01]*len(dictionary.keys()), passes=4, workers=4)

lda_model.save('./functions/src/artifacts/lda_tfidf/lda_model_tfidf')

for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))

#%%
processed_docs[sample_number]


#%%
# Evaluate LDA BOW using the doc example
processed_docs[sample_number]

for index, score in sorted(lda_model[bow_corpus[sample_number]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model.print_topic(index, 10)))

#%%
# Evaluate LDA TF-IDF using the doc example
for index, score in sorted(lda_model_tfidf[bow_corpus[sample_number]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model_tfidf.print_topic(index, 10)))

#%%
# Predict the unseen (medium article abstract)
unseen_document = "Most chatbots fail miserably at integrity and benevolence, whilst a large proportion seems to struggle with ability as well. The main problem with chatbot technology is the exponential speed at which it is advancing. The chatbot hype promised personalised in-channel experiences for everyone, but the current technology is really only suited to question and answer or FAQ type interactions. There are technical limitations which many bot creators are not necessarily aware of. Compounding this problem is a plethora of freely available online tools which allow anyone to build their own chatbot."
bow_vector = dictionary.doc2bow(preprocess(unseen_document))

for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, lda_model.print_topic(index, 5)))


#%%
# Data visualization with PyLDAvis
# BoW model
import pyLDAvis.gensim
lda_display = pyLDAvis.gensim.prepare(lda_model, bow_corpus, dictionary, sort_topics=False)
pyLDAvis.display(lda_display)

#%%
# TF-IDF model
lda_tf_idf_display = pyLDAvis.gensim.prepare(lda_model_tfidf, corpus_tfidf, dictionary, sort_topics=False)
pyLDAvis.display(lda_tf_idf_display)

