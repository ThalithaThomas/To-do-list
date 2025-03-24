import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime, date
from flask_migrate import Migrate
from dateutil import parser

# Create Flask app
app = Flask(__name__)

# Configure database
database_url = os.environ.get('DATABASE_URL', 'sqlite:///todo.db')
# Fix for Heroku PostgreSQL URL format
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# App configuration
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False') == 'True'

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String)
    completed=db.Column(db.Boolean)
    date_str =db.Column(db.Date, nullable= True)

class RecentSearch(db.Model):
    __tablename__='recentSearch'
    id=db.Column(db.Integer, primary_key=True)
    search_term=db.Column(db.String(100), nullable=False)

# Rest of your existing route handlers remain the same...

def get_formatted_todos():
    Tasks_db=User.query.all()
    currentDateStr =date.today()
    currentDate= currentDateStr.strftime('%Y-%m-%d')
    formatted_todos=[]
    for item in Tasks_db:
        if isinstance(item.date_str,str):
            formatted_dateStr=datetime.strptime(item.date_str,'%Y-%m-%d')
        elif item.date_str is not None:
            formatted_dateStr=item.date_str
        else:
            continue
        formatted_date=formatted_dateStr.strftime('%Y-%m-%d')
        display_date=formatted_dateStr.strftime('%b %d')
        formatted_todos.append({
            'id':item.id,
            'title':item.title,
            'description':item.description,
            'date_str':formatted_date,
            'display_date':display_date
            })
    return formatted_todos,currentDate

# Your existing route handlers remain the same...

@app.route('/')
def home():
    formatted_todos,currentDate=get_formatted_todos()
    return render_template("index.html",task_list=formatted_todos,currentDate=currentDate)

# ... (rest of your existing routes)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)