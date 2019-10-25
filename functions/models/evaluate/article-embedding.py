#%%
#Import all the dependencies
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
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
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

#%%
from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize

model= Doc2Vec.load("./functions/src/artifacts/d2v/d2v.model")

#%%
#to find the vector of a document which is not in training data
interest_text = "Reinforcement Learning"
print(interest_text)
test_data = preprocess(interest_text)

max_epochs = 100
vec_size = 20
alpha = 0.025

interest_infer_vector = model.infer_vector(test_data, alpha=alpha, min_alpha=0.00025, epochs=100)
print("Interest", interest_infer_vector)

similar_to_interest = model.docvecs.most_similar(positive=[interest_infer_vector])
print(similar_to_interest)

#%%
# to find most similar doc using tags
similar_doc = model.docvecs.most_similar(positive=['food diary coaching chatbot'])
print(similar_doc)

# to find vector of doc in training data using tags or in other words, printing the vector of document at index 1 in training data
print(model.docvecs['food diary coaching chatbot'])
