from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        errors = []
        if not email or not email.strip():
            errors.append("Email is required.")
        if not password or not password.strip():
            errors.append("Password is required.")

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validation Logic
        errors = []
        if not name or not name.strip():
            errors.append("Name is required.")
        if not email or not email.strip():
            errors.append("Email is required.")
        if not password or not password.strip():
            errors.append("Password is required.")
        elif len(password) < 6:
            errors.append("Password must be at least 6 characters long.")

        if not errors:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                errors.append("Email already registered. Please login.")

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')

        # If no errors, save user
        new_user = User(name=name, email=email, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('register.html')

    return render_template('register.html')

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
