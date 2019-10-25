from util.tools import format_entity
from helpers.firestore import FirestoreHelper

def get_concept_desc(params, db):

    concept_raw = params['Concept']
    concept_name = format_entity(concept_raw)

    da_helper = FirestoreHelper(db)
    concept_desc = da_helper.get_document('conceitos', concept_name)

    return concept_desc['descrição']
