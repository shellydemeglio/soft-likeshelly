from datetime import datetime, timedelta

def get_flashcard_to_study():
    now = datetime.utcnow()

    
    if 'last_studied' in session and 'next_review' in session:
        last_studied = session['last_studied']
        next_review = session['next_review']

        
        if now >= next_review:
            return flashcards[0]  

 
    return None
