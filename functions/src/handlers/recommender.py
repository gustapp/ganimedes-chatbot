from datetime import datetime, date
from util.tools import format_entity, format_param, format_param_list
from helpers.firestore import FirestoreHelper
from model.kb.inference_engine import rank_content, explain_instance

""" Multi-task recommender system.
     - Learning-object suggestion:
      . Course
      . Article
"""

def teacher_constraint(course_ref, req_teachers):
    """ Check if at least one of course teachers is also
        present on the teachers requested by the user.
    """
    course_teachers = course_ref._data['docentes']
    for course_teacher in course_teachers:
        if course_teacher in req_teachers:
            return True

    return False

def class_datetime_constraint(course_ref, weekdays, start_time, end_time, da_helper):
    """ Check if at least one of the course 
        classes is in a feasible weekday and
        time interval.
    """

    class_helper = FirestoreHelper(course_ref.reference)
    classes = class_helper.get_collection('oferecimentos', ref=True)

    for class_ref in classes:
        for day in weekdays:
            schedule_helper = FirestoreHelper(class_ref.reference)
            filter_schedule = [
                ['dia', '==', '{}'.format(day)], # weekdays[0]
            ]
            schedules = schedule_helper.query('horarios', filter_schedule)

            for schedule in schedules:
                # no constraint on time
                if not start_time and not end_time:
                    return True
                # check if class meet schedule requirements
                if datetime.strptime(schedule['horario_fim'], "%H:%M") <= datetime.strptime(end_time, "%H:%M") and datetime.strptime(schedule['horario_inicio'], "%H:%M") >= datetime.strptime(start_time, "%H:%M"):
                    return True
    
    return False

def get_explanation(params, db):
    theme_raw = params['outputContexts'][0]['parameters']['theme']
    theme = format_entity(theme_raw)

    courses = [x.lower() for x in params['Course']]

    reasons = explain_instance(theme, 'subject', courses)

    return reasons # (DEBUG)

    if len(reasons) == 0: # Explanations not found 
        return "Desculpe, não sei explicar essa recomendação em particular."

    explanation_text = ""
    for reason in reasons:
        list.reverse(reason[0])
        path = reason[0]
        expls = reason[1]
        # Pattern 1
        if path == [3,-3,-1]:
            for expl in expls:
                expl = [x.replace('categoria:', '').replace('category:', '').replace('_', ' ') for x in expl]
                explanation_text += " {} é sobre {} e tanto {} como {} são temas de {}.".format(expl[3].upper(), expl[2], expl[0], expl[2], expl[1])
        # Pattern 2
        elif path == [-1,-2, 2]:
            for expl in expls:
                expl = [x.replace('categoria:', '').replace('category:', '').replace('_', ' ') for x in expl]
                explanation_text += " {} é sobre {} e tanto {} como {} são oferecidas pelo docente {}.".format(expl[3].upper(), expl[2], expl[0], expl[2], expl[1])
        else:
            raise Exception("Oops")


    return 'Recomendo a disciplina {}, pois {}'.format(courses, explanation_text)

    # return 'Recomendo a disciplina {}, pois {} é um tópico de {} assim como {}, que é um assunto da disciplina'.format(course, reasons[0][1][0][0], reasons[0][1][0][1], reasons[0][1][0][2], reasons[0][1][0][3])
    # return 'Recomendo a disciplina {}, pois {} é sobre {}'.format(course, theme_raw, ', '.join([x.split(':')[-1] for x in reasons[:3]]))

def get_course_recommendation(params, db):

    theme_raw = params['theme']
    theme = format_entity(theme_raw)
    
    k = int(params['suggestion_number']) # nº recommendations

    teachers = format_param_list(params['teachers'])
    weekdays = format_param_list(params['weekdays'])
    start_time = None
    end_time = None
    if format_param(params['time_period']):
        start_time = params['time_period']['startTime'][11:-9]
        end_time = params['time_period']['endTime'][11:-9]

    courses = rank_content(theme) # KGE link prediction 

    return courses # (DEBUG)

    da_helper = FirestoreHelper(db) # data access helper

    recommendations = []
    for course_id in courses[:10]: # Reduce search space
        # stop if enough recommendations have been found
        if len(recommendations) == k:
            break

        course_ref = da_helper.get_document('cursos', course_id, ref=True)

        # meet teacher requirement
        if len(teachers) > 0 and not teacher_constraint(course_ref, teachers):
            continue

        # meet date and time requirements
        if len(weekdays) > 0 and not class_datetime_constraint(course_ref, weekdays, start_time, end_time, da_helper):
            continue

        recommendations.append(course_id + ' - ' + course_ref._data['name'])

    if len(recommendations) > 1:
        return 'Recomendo as disciplinas: {}'.format(', '.join(recommendations))
    elif len(recommendations) == 1:
        return 'Recomendo a disciplina: {}'.format(', '.join(recommendations))
    else:
        return 'Desculpe, não encontrei disciplinas que atendam as requisitos levantados :('

def get_article_recommendation(params, db):
    
    return 'get_article_recommendation'
