from util.decorators import fault_message, response
from handlers.jupiterweb import get_course_info, get_course_schedule, get_course_requirements, get_course_workload, get_course_teachers, get_course_credits
from handlers.dbpedia import get_concept_desc
from handlers.recommender import get_course_recommendation, get_explanation
from handlers.feedback import store_evaluation

class IntentHandler(object):
    """ Facade class that wraps all handlers."""
    def __init__(self, db):
        """ (Constructor) 
            Args:
                db (Firestore): Database connection.
        """
        self.db = db

    def uninplemented_feature(self, x, y):
        return "Desculpe, ainda não consigo fazer isso :/"

    @response
    @fault_message
    def handle_intent(self, intent, params):
        """Switch intent to correspondent handler function.
        Args:
            intent (string): Dialogflow intent id.
            params (object): Fulfillment parameters.
        Return:
            Fulfillment answer text.
        """
        default_intent = self.uninplemented_feature
        intents = {
            'GetCourseInfo': get_course_info,
            'GetCourseRequirements': get_course_requirements,
            'GetCourseWorkload': get_course_workload,
            'GetCourseTeacher': get_course_teachers,
            'GetCourseCredit': get_course_credits,
            'GetCourseSchedule': get_course_schedule,
            'GetConceptDescription': get_concept_desc,
            'GetCourseSuggestion': get_course_recommendation,
            'GetCourseSuggestion - explain': get_explanation,
            'Feedback': store_evaluation
        }
        intent_handler = intents.get(intent, default_intent)
        return intent_handler(params, self.db)
    