'''
CSC3020 - Software Engineering Fundamentals
Instructor: Thyago Mota
Student(s):
Description: Project 1 - Schools
'''

from app import app, db, sp
from app.models import User, School, TransportationCost
from app.forms import SignUpForm, LoginForm, SchoolCreateForm, SchoolUpdateForm, SchoolDeleteForm, TransportationCostForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    return "Under development..."
    
@app.route('/users/login', methods=['GET', 'POST'])
def login():
    return "Under development..."

@login_required
@app.route('/users/signout', methods=['GET', 'POST'])
def signout():
    return "Under development..."

@login_required
@app.route('/schools')
@login_required
def list_schools(): 
    return "Under development..."

@login_required
@app.route('/schools/create', methods=['GET', 'POST'])
def create_school():
    return "Under development..."

@login_required
@app.route('/schools/<int:id>', methods=['GET', 'POST'])
def update_school(id): 
    return "Under development..."  

@login_required
@app.route('/schools/<int:id>/delete', methods=['GET', 'POST'])
def delete_school(id): 
    return "Under development..."

@login_required
@app.route('/schools/<int:id>/cost', methods=['GET', 'POST'])
def school_transportation_cost(id):
    return "Under development..."

@login_required
@app.route('/schools/<int:id>/routes', methods=['GET', 'POST'])
def school_routes(id):
    return "Under development..."