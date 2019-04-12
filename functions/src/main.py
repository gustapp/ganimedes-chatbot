import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS

import nltk
from nltk.stem import WordNetLemmatizer, SnowballStemmer, PorterStemmer
from nltk.tokenize import word_tokenize

def lemmatize_stemming(text):
    stemmer = PorterStemmer()
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize

class CourseSuggestion:
    def __init__(self, suggestions):
        self.suggestions = suggestions


def get_course_suggestion(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        interest_text = request.args.get('message')
    elif request_json and 'message' in request_json:
        interest_text = request_json['message']
    else:
        return f'Hello World!'

    from os import path
    root = path.dirname(path.abspath(__file__))

    """Load Document Embedding"""
    model_file = path.join(root, 'artifacts/d2v/d2v.model')
    model= Doc2Vec.load(model_file)

    """Redirects nltk_data directory path to local copy
    Important:
        Deploy the function whthout the local copy of nltk_data in artifacts
        will cause the app to FAIL
    """
    nltk_data_dir = path.join(root, 'artifacts/nltk_data/')
    nltk.data.path.append(nltk_data_dir)
    
    test_data = preprocess(interest_text)

    alpha = 0.025
    interest_infer_vector = model.infer_vector(test_data, alpha=alpha, min_alpha=0.00025, epochs=100)

    similar_to_interest = model.docvecs.most_similar(positive=[interest_infer_vector])

    """Wrap all return data into JSON"""
    from flask import jsonify, json
    suggestion = CourseSuggestion(similar_to_interest) 

    return jsonify(suggestion.__dict__)

from gensim.models import LdaModel 
from gensim.corpora import Dictionary
import numpy as np

class CourseSuggestionExplanation:
    def __init__(self, topic, score):
        self.topic = topic
        self.score = score

def get_course_suggestion_explanation(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and 'message' in request.args and 'suggestion' in request.args:
        interest_text = request.args.get('message')
        recommended_title = request.args.get('suggestion')
    elif request_json and 'message' in request_json:
        interest_text = request_json['message']
    else:
        return f'Course Suggestion Explanation'

    from os import path
    root = path.dirname(path.abspath(__file__))

    """Load Topic Model"""
    model_file = path.join(root, 'artifacts/lda_bow/lda_model')
    lda_model= LdaModel.load(model_file)

    """Load Dictionary"""
    dict_file = path.join(root, 'artifacts/lda_bow/lda_model.id2word')
    dictionary = Dictionary.load(dict_file)

    """Redirects nltk_data directory path to local copy
    Important:
        Deploy the function whthout the local copy of nltk_data in artifacts
        will cause the app to FAIL
    """
    nltk_data_dir = path.join(root, 'artifacts/nltk_data/')
    nltk.data.path.append(nltk_data_dir)
    
    """ TODO:
        Fetch article abstract from Firestore
    """
    if recommended_title == "reinforcement-learning based dialogue system for human-robot interactions with socially-inspired rewards":
        recom_article_abstract = "© 2015 Elsevier Ltd. All rights reserved. This paper investigates some conditions under which polarized user appraisals gathered throughout the course of a vocal interaction between a machine and a human can be integrated in a reinforcement learning-based dialogue manager. More specifically, we discuss how this information can be cast into socially-inspired rewards for speeding up the policy optimisation for both efficient task completion and user adaptation in an online learning setting. For this purpose a potential-based reward shaping method is combined with a sample efficient reinforcement learning algorithm to offer a principled framework to cope with these potentially noisy interim rewards. The proposed scheme will greatly facilitate the system's development by allowing the designer to teach his system through explicit positive/negative feedbacks given as hints about task progress, in the early stage of training. At a later stage, the approach will be used as a way to ease the adaptation of the dialogue policy to specific user profiles. Experiments carried out using a state-of-the-art goal-oriented dialogue management framework, the Hidden Information State (HIS), support our claims in two configurations: firstly, with a user simulator in the tourist information domain (and thus simulated appraisals), and secondly, in the context of man-robot dialogue with real user trials."
    else:
        recom_article_abstract = recommended_title

    """Preprocess text"""
    interest_text_clean = preprocess(interest_text)
    abstract_clean = preprocess(recom_article_abstract)
    
    """Vectorize to BoW both user statement and recommended title"""
    interest_bv = dictionary.doc2bow(interest_text_clean)
    recommended_bv = dictionary.doc2bow(abstract_clean)

    """Apply LDA topic model"""
    interest_topics = lda_model[interest_bv]
    recommended_topics = lda_model[recommended_bv]

    """Identify common topics
    Note:
        Apply topic model for both user statement and
        recommended article. Then select the most influential
        topics to explain the suggestion.
    TODO:
        Optimize the vector element-wise multiplication
    """
    topic_similarity = []
    for recom_index, recom_value in recommended_topics:
        for intrs_index, intrs_value in interest_topics:
            if intrs_index == recom_index:
                topic_similarity.append((intrs_index, recom_value * intrs_value))
    
    most_influential_topics = sorted(topic_similarity, key=lambda tup: -1*tup[1])
    index, score = most_influential_topics[0]

    reason = lda_model.print_topic(index)

    """Wrap all return data into JSON"""
    from flask import jsonify, json
    explanation = CourseSuggestionExplanation(reason, str(score)) 

    return jsonify(explanation.__dict__)


# (DEBUG ONLY) if __name__ == "main":
if __name__ == "main":
    """ Runs python 3.7 Cloud Functions locally
    Conditions:
        * __main__ : being run directly
        * main : being run on debugger

        Flask app wrapper
    """
    from flask import Flask, request
    app = Flask(__name__)

    @app.route('/course-suggestion')
    def course_suggestion():
        return get_course_suggestion(request)
    
    @app.route('/course-suggestion-explanation')
    def course_suggestion_explanation():
        return get_course_suggestion_explanation(request)

    app.run('localhost', 5000, debug=True)
