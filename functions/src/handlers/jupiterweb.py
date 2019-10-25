from helpers.firestore import FirestoreHelper

def get_course_info(params, db):
    course_id = params['Course']

    da_helper = FirestoreHelper(db)
    course_info = da_helper.get_document('cursos', course_id)

    return 'A disciplina {} - {} possui a seguinte descrição: {}'.format(course_id, course_info['name'], course_info['objetivos'])

def get_course_requirements(params, db):
    course_id = params['Course']

    da_helper = FirestoreHelper(db)  
    course_info = da_helper.get_document('cursos', course_id)

    if len(course_info['requisitos']) > 0:
        return 'A disciplina possui os seguintes requisitos: {}'.format(', '.join(course_info['requisitos']))
    else:
        return 'A disciplina não possui requisitos!'

def get_course_workload(params, db):
    course_id = params['Course']

    da_helper = FirestoreHelper(db)  
    course_info = da_helper.get_document('cursos', course_id)

    return 'A disciplina possui {} horas por semestre!'.format(course_info['carga_horaria'])

def get_course_teachers(params, db):
    course_id = params['Course']

    da_helper = FirestoreHelper(db)  
    course_info = da_helper.get_document('cursos', course_id)

    if len(course_info['docentes']) > 0:
        return 'A disciplina possui os seguintes professores: {}'.format(', '.join(course_info['docentes']))
    else:
        return 'A disciplina não possui nenhum professor cadastrado no sistema!'

def get_course_credits(params, db):
    course_id = params['Course']

    da_helper = FirestoreHelper(db)  
    course_info = da_helper.get_document('cursos', course_id)

    return 'São {} créditos aula e {} créditos trabalho'.format(course_info['creditos']['aula'], course_info['creditos']['trabalho'])

def get_course_schedule(params, db):
    course_id = params['Course']

    da_helper = FirestoreHelper(db)  
    course_ref = da_helper.get_document('cursos', course_id, ref=True)

    class_helper = FirestoreHelper(course_ref.reference)
    classes = class_helper.get_collection('oferecimentos', ref=True)

    message_builder = []
    for class_ref in classes:
        class_code = class_ref._data['codigo_turma'][-2:] # slice
        message_builder.append('--> A turma {} tem os seguintes horários: \n'.format(class_code))

        schedule_helper = FirestoreHelper(class_ref.reference)
        schedules = schedule_helper.get_collection('horarios')

        for schedule in schedules:
            message_builder.append('-> {} às {} - {}\n'.format(schedule['dia'], schedule['horario_inicio'], schedule['horario_fim']))

    return ' '.join(message_builder)
