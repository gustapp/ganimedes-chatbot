from main import get_dialogflow_fulfillment

if __name__ == "main_emulate":
    """ Runs python 3.7 Cloud Functions locally
    Conditions:
        * __main__ : being run directly
        * main : being run on debugger

        Flask app wrapper
    """
    from flask import Flask, request
    app = Flask(__name__)

    @app.route('/dialogflow-fulfillment', methods = ['GET', 'POST'])
    def dialogflow_fulfillment():
        return get_dialogflow_fulfillment(request)

    app.run('localhost', 5000, debug=True)