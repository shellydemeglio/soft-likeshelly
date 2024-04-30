from flask import Flask, render_template, request, redirect, url_for, session
from flask_SQLAlchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcard_app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Define a relationship with the User model
    user = db.relationship('User', backref=db.backref('decks', lazy=True))

    def __repr__(self):
        return f'<Deck {self.name}>'

# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcard_app.db'
db = SQLAlchemy(app)

# Define Deck model
class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Define routes for deck management
@app.route('/decks')
def list_decks():
    decks = Deck.query.all()
    return render_template('decks.html', decks=decks)

@app.route('/decks/create', methods=['GET', 'POST'])
def create_deck():
    if request.method == 'POST':
        name = request.form['name']
        new_deck = Deck(name=name)
        db.session.add(new_deck)
        db.session.commit()
        return redirect(url_for('list_decks'))
    return render_template('create_deck.html')

@app.route('/decks/<int:deck_id>/delete', methods=['POST'])
def delete_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    db.session.delete(deck)
    db.session.commit()
    return redirect(url_for('list_decks'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/create_flashcard', methods=['GET', 'POST'])
def create_flashcard():
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        deck_id = request.form.get('deck_id')
        
        # Check if the deck_id is provided and valid
        if deck_id:
            deck = Deck.query.get(deck_id)
            if deck:
                # Create a new flashcard associated with the selected deck
                flashcard = Flashcard(question=question, answer=answer, deck_id=deck_id)
                db.session.add(flashcard)
                db.session.commit()
                return 'Flashcard created successfully'

        # If deck_id is not provided or invalid, create a flashcard without association to a deck
        flashcard = Flashcard(question=question, answer=answer)
        db.session.add(flashcard)
        db.session.commit()
        return 'Flashcard created successfully'

    # If the request method is GET, render the template with a list of decks
    decks = Deck.query.all()
    return render_template('create_flashcard.html', decks=decks)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
