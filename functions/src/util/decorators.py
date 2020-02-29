import logging
from google.cloud.exceptions import NotFound

DEFAULT_FALLBACK_MESSAGE = "Desculpe, houve um erro na aplicação. Tente novamente."
NOT_FOUND_MESSAGE = "Desculpe, não encontrei no sistema."

def fault_message(function):
    def protect_boundary(class_self, intent, params):
        try:
            func = function(class_self, intent, params)
            return func
        except NotFound:
            logging.warning("not found in firestore: {intent} | {params}")
            return NOT_FOUND_MESSAGE
        except Exception as e:
            logging.error("unexpected exception", exc_info=True)
            return DEFAULT_FALLBACK_MESSAGE

    return protect_boundary

def response(function):
    def format_response(class_self, intent, params):
        res = function(class_self, intent, params)
        return '{{"fulfillmentText":"{}","outputContexts":[]}}'.format(res)

    return format_response
