'''
CSC3020 - Software Engineering Fundamentals
Instructor: Thyago Mota
Student(s):
Description: Project 1 - Schools
'''

from flask import Flask
import os

app = Flask('Schools Web App')
# app.secret_key = os.environ['SECRET_KEY']
app.secret_key = 'you will never know'

# db initialization
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools.db'
db = SQLAlchemy(app)

# models initialization
from app import models
with app.app_context(): 
    db.create_all()

# login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

# user_loader callback
@login_manager.user_loader
def load_user(id):
    try: 
        return db.session.query(User).filter(User.id==id).one()
    except: 
        return None

from app import routes