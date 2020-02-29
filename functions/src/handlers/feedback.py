from datetime import datetime

def store_evaluation(params, db):

    algo_type = params['algo_type']

    timestamp = datetime.now()

    scores = {
        'timestamp': str(timestamp),
        'effectiveness': params['Feedback'],
        'engagement': params['Engagement'],
        'feedback': params['Feedback'],
        'persuasion': params['Persuasion'],
        'transparency': params['Transparency'],
        'trust': params['Trust'],
        'comment': params['Comment'],
        'algo':algo_type
    }

    # Store feedback on Firestore
    if algo_type == "PRED":
        db.collection('avaliações').document().set(scores)
        return "Valeu! até a próxima!"
    elif algo_type == "TRUE":
        db.collection('avaliações-graph').document().set(scores)
        return "Valeu! até a próxima!"