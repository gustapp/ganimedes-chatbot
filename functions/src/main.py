import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from intent_handler import IntentHandler

logging.basicConfig(format='%(asctime)s - %(name)s | %(levelname)s | %(message)s', datefmt='%d-%b-%y %H:%M:%S')

project_id = 'ganimedes-d9ecd'

# # Use the application default credentials
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred, {
#   'projectId': project_id,
# })

# (DEBUG ONLY)
cred = credentials.Certificate('./auth/ganimedes-d9ecd-d860c9b7caa9.json')
firebase_admin.initialize_app(cred)

# Retrieve Firestore
db = firestore.client()

# Initialize intent handler facade 
agent = IntentHandler(db)

def get_dialogflow_fulfillment(request, agent=agent):
    """Responds to Dialogflow fulfillment webhook request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        JSON object with response text.
    """
    logging.info('dialogflow request headers: {}'.format(request.headers))
    logging.info('dialogflow request body: {}'.format(request.data))

    request_json = request.get_json()
    query_result = request_json['queryResult']

    intent = query_result['intent']['displayName']
    params = query_result['parameters']
    context = None
    if 'outputContexts' in query_result:
        context = query_result['outputContexts']
    params['outputContexts'] = context

    res = agent.handle_intent(intent, params)

    return res
