from datetime import datetime

def store_evaluation(params, db):

    timestamp = datetime.now()

    scores = {
        'timestamp': str(timestamp),
        'effectiveness': params['Feedback'],
        'engagement': params['Engagement'],
        'feedback': params['Feedback'],
        'persuasion': params['Persuasion'],
        'transparency': params['Transparency'],
        'trust': params['Trust'],
        'comment': params['Comment']
    }

    # Store feedback on Firestore
    db.collection('avaliações').document().set(scores)

    return "Valeu, até a próxima!"