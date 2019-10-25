import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./auth/ganimedes-d9ecd-d860c9b7caa9.json')
firebase_admin.initialize_app(cred)

# Retrieve Firestore
db = firestore.client()

import pandas as pd

def fill_concept_description():
    desc_df = pd.read_csv('./scripts/data/desc_entities.csv')
    desc_df = desc_df.dropna()

    for index, row in desc_df.iterrows():
        db.collection('conceitos').document(row['pt-concept']).set({'descrição': row['description']})

import json

def fill_courses_data():
    with open('./db_poli_v2.json') as f:
        data = json.load(f)

    for course in data:
        course_classes = course['oferecimento']
        del course['oferecimento']

        db.collection('cursos').document(course['sigla']).set(course) # Add course document
        course_doc = db.collection('cursos').document(course['sigla']).get()

        for course_class in course_classes:
            schedules = course_class['horario']
            del course_class['horario']

            course_ref = course_doc.reference
            course_ref.collection('oferecimentos').document(course_class['codigo_turma']).set(course_class) # Add classes
            class_doc = course_ref.collection('oferecimentos').document(course_class['codigo_turma']).get()

            for schedule in schedules:
                class_ref = class_doc.reference
                class_ref.collection('horarios').document().set(schedule) # Add schedule

def update_doc():
    docs = db.collection('cursos').stream()

    for doc in docs:
        doc.reference.update({'name': '-'.join(doc._data['name'].split('-')[1:]).strip()})
        # doc.reference.update({'docentes': ['-'.join(x.split('-')[1:]).strip() for x in doc._data['docentes']]})

with open('./db_poli_v2.js
on') as f:
    data = json.load(f)

for course in data:
    
    # docentes_updt = ['-'.join(x.split('-')[1:]).strip() for x in course['docentes']]
    docentes_updt = '-'.join(course['name'].split('-')[1:]).strip()
    coll_ref = db.collection('cursos')
    doc = coll_ref.document(course['sigla'])
    doc.update({'name': docentes_updt})
    

print('success')