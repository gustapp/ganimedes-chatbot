#%% [markdown]
# # Document Embedding (Doc2Vec)

#%%
# Load Data
import pandas as pd

df = pd.read_csv('./functions/models/dataset/chatbot-articles.csv', error_bad_lines=False)
data_text = df[['abstract']].dropna()
data_tags = df[['title']]
data_text['index'] = data_text.index
documents = data_text

print(len(documents))
df.head()

#%%
#Import all the dependencies
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS

import nltk
from nltk.stem import WordNetLemmatizer, SnowballStemmer, PorterStemmer
from nltk.tokenize import word_tokenize
nltk.download('wordnet')

#%%
# Preprocessing methods
def lemmatize_stemming(text):
    stemmer = PorterStemmer()
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) >= 3:
            result.append(lemmatize_stemming(token))
    return result

def preprocess_with_filter(text, dictionary):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) >= 3:
            lemmatized_stemmed_token = lemmatize_stemming(token) 
            if lemmatized_stemmed_token in dictionary.token2id:
                result.append(lemmatized_stemmed_token)
    return result

#%%
# Preprocess all docs
processed_docs = documents['abstract'].map(preprocess)

#%%
# Create a dictionary from ‘processed_docs’ containing the number of times a word appears in the training set
dictionary = gensim.corpora.Dictionary(processed_docs)

#%%
# Filter out tokens that appear in less than 15 docs or more than 0.5 docs
# Keep only the first 100000 most frequent
dictionary.filter_extremes(no_below=2, no_above=0.9)

#%%
# Tag documents (opt 1)
data = documents.values
tags = data_tags.values

tagged_data = [TaggedDocument(words=preprocess_with_filter(_d, dictionary), tags=tags[i]) for _d, i in data]

#%%
# Train
max_epochs = 100
vec_size = 20
alpha = 0.025

model = Doc2Vec(size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=1,
                dm =1)
  
model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease the learning rate
    model.alpha -= 0.0002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha

model.save("./functions/src/artifacts/d2v/d2v.model")
print("Model Saved")
