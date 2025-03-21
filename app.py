################################################################################
# IMPORTS AND SETUP
################################################################################
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime, date
from flask_migrate import Migrate
from dateutil import parser
import sqlite3
from urllib.parse import quote


################################################################################
# FLASK APPLICATION CONFIGURATION
################################################################################
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# Get the DATABASE_URL from Heroku's environment variables
# Fall back to the SQLite database if not on Heroku
database_url = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite')

# Heroku's PostgreSQL URL starts with "postgres://" but SQLAlchemy needs "postgresql://"
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Only set debug mode in development, not in production
if os.environ.get('FLASK_ENV') == 'development':
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
else:
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False

db = SQLAlchemy(app)
Migrate = Migrate(app, db)


################################################################################
# DATABASE MODELS
################################################################################
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String)
    completed = db.Column(db.Boolean)
    date_str = db.Column(db.Date, nullable=True)


class RecentSearch(db.Model):
    __tablename__ = 'recentSearch'
    id = db.Column(db.Integer, primary_key=True)
    search_term = db.Column(db.String(100), nullable=False)


# Create database tables if they don't exist
with app.app_context():
    db.create_all()


################################################################################
# HELPER FUNCTIONS
################################################################################
def get_formatted_todos():
    """
    Retrieves all tasks from the database and formats their dates for display
    Returns a list of formatted tasks and the current date
    """
    Tasks_db = User.query.all()
    currentDateStr = date.today()
    currentDate = currentDateStr.strftime('%Y-%m-%d')
    formatted_todos = []
    
    for item in Tasks_db:
        if isinstance(item.date_str, str):
            formatted_dateStr = datetime.strptime(item.date_str, '%Y-%m-%d')
        elif item.date_str is not None:
            formatted_dateStr = item.date_str
        else:
            continue
            
        formatted_date = formatted_dateStr.strftime('%Y-%m-%d')
        display_date = formatted_dateStr.strftime('%b %d')
        formatted_todos.append({
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'date_str': formatted_date,
            'display_date': display_date
        })
    return formatted_todos, currentDate


def serialize(self):
    """
    Serializes a search object for JSON response
    """
    return {
        'id': self.id,
        'search_term': self.search_term
    }


################################################################################
# ROUTES - MAIN VIEWS
################################################################################
@app.route('/')
def home():
    """Home page - displays index template with all tasks"""
    formatted_todos, currentDate = get_formatted_todos()
    return render_template("index.html", task_list=formatted_todos, currentDate=currentDate)


@app.route('/inbox')
def inbox():
    """Inbox page - displays all tasks"""
    formatted_todos, currentDate = get_formatted_todos()
    return render_template("inbox.html", task_list=formatted_todos, currentDate=currentDate)


@app.route('/today')
def today():
    """Today page - displays tasks due today"""
    formatted_todos, currentDate = get_formatted_todos()
    return render_template("today.html", task_list=formatted_todos, currentDate=currentDate)


@app.route('/upcoming')
def upcoming():
    """Upcoming page - displays future tasks"""
    formatted_todos, currentDate = get_formatted_todos()
    return render_template("upcoming.html", task_list=formatted_todos, currentDate=currentDate)


################################################################################
# ROUTES - TASK MANAGEMENT
################################################################################
@app.route("/addNewTask", methods=['POST', 'GET'])
def add():
    """Add a new task to the database"""
    formatted_date = ''
    title = request.form.get('title')
    description = request.form.get('description')
    
    if request.method == 'POST':
        date_str = request.form.get('due_date')
        date_obj = parser.parse(date_str) if date_str else None
        
        if not date_str:
            flash('Due-date is required!', 'error')
            return redirect(url_for('add'))
            
        if not title:
            flash('Title is required!', 'error')
            return redirect(url_for('add'))
            
        flash('Task added successfully!', 'success')
       
        try:
            new_Task = User(title=title, description=description, completed=False, date_str=date_obj)
            db.session.add(new_Task)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    return_url = request.form.get('return_url', url_for('home'))
    return redirect(return_url)


@app.route("/delete/<int:task_id>", methods=['POST'])
def delete_task(task_id):
    """Delete a task from the database"""
    return_url = request.form.get('return_url', url_for('home'))
    
    try:
        task_to_delete = User.query.filter_by(id=task_id).first()
        if task_to_delete:
            db.session.delete(task_to_delete)
            db.session.commit()
            flash('Task deleted successfully!', 'success')
        else:
            flash('Task not found!', 'error')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the task: {}'.format(str(e)), 'error')

    if return_url == url_for('search'):
        return redirect(url_for('home'))
    else:
        return redirect(request.form.get('return_url', '/'))


@app.route("/update/<int:task_id>", methods=['POST', 'GET'])
def updateTask(task_id):
    """Update an existing task"""
    return_url = request.form.get('return_url', url_for('home'))
    task = User.query.get(task_id)
    
    if task is None:
        return "User not found!", 404
        
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        date_str = request.form['dueDate']
        
        if date_str:
            try:
                task.date_str = datetime.strptime(date_str, '%Y-%m-%d').date()
                db.session.commit()
            except Exception as e:
                flash(f"Invalid date format: {e}", 400)
            
    if return_url == url_for('search'):
        return redirect(url_for('home'))
    else:
        return redirect(request.form.get('return_url', '/'))


################################################################################
# ROUTES - SEARCH FUNCTIONALITY
################################################################################
@app.before_request
def load_recentSearches():
    """Load recent searches before each request for global access"""
    g.recent_searches = RecentSearch.query.order_by(RecentSearch.id.desc()).limit(3).all()


@app.route('/search', methods=['GET'])
def search():
    """Search for tasks by title"""
    results = []
    title_search = request.args.get('search_input')
    existing_search = None
    recent_searches = []
    
    try:
        if title_search and title_search.strip():
            existing_search = RecentSearch.query.filter_by(search_term=title_search).first()
            results = User.query.filter(User.title.contains(title_search)).all()
            
            if not existing_search:
                new_search = RecentSearch(search_term=title_search)
                db.session.add(new_search)
                
            recent_searches_count = RecentSearch.query.count()
            if recent_searches_count >= 4:
                oldest_search = RecentSearch.query.order_by(RecentSearch.id.asc()).first()
                if oldest_search:
                    db.session.delete(oldest_search)
                    
            db.session.commit()
            
            if results:
                flash(f'Search completed successfully. Found {len(results)} for "{title_search}"', 'success')
                
            recent_searches = RecentSearch.query.all()
            
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while searching. Please try again later.', 'error')

    return render_template(
        'search.html',
        results=results,
        title_search=title_search,
        recent_searches=recent_searches
    )


@app.route('/recent_Searches', methods=['GET'])
def get_recentSearches():
    """API endpoint to get recent searches as JSON"""
    recent_searches = RecentSearch.query.order_by(RecentSearch.id.desc()).limit(3).all()
    
    return jsonify([
        {
            'id': search.id,
            'search_term': search.search_term
        }
        for search in recent_searches
    ])


@app.route('/delete_search/<int:search_id>', methods=['POST'])
def delete_search(search_id):
    """Delete a search term from recent searches"""
    return_url = request.form.get('return_url', url_for('home'))
    search_to_delete = RecentSearch.query.get(search_id)
    
    if search_to_delete:
        db.session.delete(search_to_delete)
        db.session.commit()

    if return_url == url_for('search'):
        return redirect(url_for('home'))
    else:
        return redirect(request.form.get('return_url', '/'))


################################################################################
# APPLICATION ENTRY POINT
################################################################################
if __name__ == "__main__":
    # Use Heroku's PORT environment variable when available
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)