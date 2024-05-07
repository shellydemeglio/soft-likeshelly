from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ProgressData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Define fields to track progress data, such as user_id, flashcards_completed, quizzes_completed, etc.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flashcards_completed = db.Column(db.Integer, default=0)
    quizzes_completed = db.Column(db.Integer, default=0)
    
    
    user = db.relationship('User', backref=db.backref('progress_data', lazy=True))
