import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS

import nltk
from nltk.stem import WordNetLemmatizer, SnowballStemmer, PorterStemmer
from nltk.tokenize import word_tokenize
# nltk.download('wordnet')

def lemmatize_stemming(text):
    stemmer = PorterStemmer()
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            # result.append(lemmatize_stemming(token))
            result.append(token)
    return result

from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize

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

    # nltk.download('wordnet')

    from os import path
    root = path.dirname(path.abspath(__file__))

    model_file = path.join(root, 'artifacts/d2v/d2v.model')
    model= Doc2Vec.load(model_file)
    
    test_data = preprocess(interest_text)

    alpha = 0.025
    interest_infer_vector = model.infer_vector(test_data, alpha=alpha, min_alpha=0.00025, epochs=100)

    similar_to_interest = model.docvecs.most_similar(positive=[interest_infer_vector])

    return 'Suggestions: {}'.format(similar_to_interest)


if __name__ == "__main__":
    """ Runs python 3.7 Cloud Functions locally
    Conditions:
        * __main__ : being run directly
        * main : being run on debugger

        Flask app wrapper
    """
    from flask import Flask, request
    app = Flask(__name__)

    @app.route('/course_suggestion')
    def course_suggestion():
        return get_course_suggestion(request)

    app.run('localhost', 8000, debug=True)
