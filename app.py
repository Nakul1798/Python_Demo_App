import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Task, User # Import User
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash # Required for registration/login

app = Flask(__name__)

# --- Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", 'sqlite:///tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", 'a_super_secret_key_for_dev') # MANDATORY for Flask-Login/Sessions
# Render requires you to set SECRET_KEY as an Environment Variable for production!

db.init_app(app)

# --- Flask-Login Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # The function name for the login route

@login_manager.user_loader
def load_user(user_id):
    """Callback function to load a user from the database given their ID."""
    return User.query.get(int(user_id))

# Ensure database tables exist (including the new User table)
with app.app_context():
    db.create_all()

# --- Authentication Routes ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            flash('Username already exists. Please choose a different one.', 'warning')
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
            
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
        
        login_user(user)
        return redirect(url_for('index'))
        
    return render_template('login.html')


@app.route('/logout')
@login_required # Requires user to be logged in to access this route
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# --- Protected Task Routes ---

@app.route('/')
@login_required # Protect the main task view
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
@login_required # Protect the add task function
def add_task():
    # ... (task logic remains the same)
    title = request.form['title']
    priority = request.form['priority']
    deadline = request.form['deadline']
    new_task = Task(title=title, priority=priority, deadline=deadline)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
@login_required # Protect the delete function
def delete_task(id):
    # ... (task logic remains the same)
    task = Task.query.get_or_404(id) # Use get_or_404 for robustness
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))
