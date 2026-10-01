'''
CSC3020 - Software Engineering Fundamentals
Instructor: Thyago Mota
Student(s): Juvia Archuleta, Leigha Lennon
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
    form = SignUpForm()
    if form.validate_on_submit():
        # Check if the passwords match
        if form.passwd.data != form.passwd_confirm.data:
            return render_template('signup.html', form=form)
        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(form.passwd.data.encode('utf-8'), bcrypt.gensalt())
        user = User(id=form.id.data, name=form.name.data, about=form.about.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)
    
@app.route('/users/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.get(User, form.id.data)
        if user is not None:
            password_matches = bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.password)
            if password_matches:
                login_user(user)
                return redirect(url_for('list_schools'))
            
    return render_template('login.html', form=form)
       
@login_required
@app.route('/users/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/schools')
@login_required
def list_schools(): 
    schools = db.session.query(School).all() # Retrieve all schools from the database
    return render_template('schools.html', schools=schools)

@login_required
@app.route('/schools/create', methods=['GET', 'POST'])
def create_school():
    form = SchoolCreateForm()
    if form.validate_on_submit():
        # convert the school type to a number for storage in the database
        if form.type.data == 'elementary':
            school_type = 0
        elif form.type.data == 'middle':
            school_type = 1
        elif form.type.data == 'high school':
            school_type = 2
        #convert the school status to a number for storage in the database
        if form.status.data == 'Open':
            school_status = 1
        elif form.status.data == 'Closed':
            school_status = 0

        school = School(name=form.name.data, address= form.address.data, type=school_type, status=school_status)
        db.session.add(school)
        db.session.commit()
        return redirect(url_for('list_schools'))
    return render_template('school_crud.html', form=form)

@login_required
@app.route('/schools/<int:id>', methods=['GET', 'POST'])
def update_school(id): 
    return "Under development..."  

@login_required
@app.route('/schools/<int:id>/delete', methods=['GET', 'POST'])
def delete_school(id): 
    school = db.session.get(School, id)
    if school is not None:
        return redirect(url_for('list_schools'))
    db.session.delete(school)
    db.session.commit()
    return redirect(url_for('list_schools'))

@login_required
@app.route('/schools/<int:id>/cost', methods=['GET', 'POST'])
def school_transportation_cost(id):
    return "Under development..."

@login_required
@app.route('/schools/<int:id>/routes', methods=['GET', 'POST'])
def school_routes(id):
    return "Under development..."
