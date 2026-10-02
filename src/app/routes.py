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
        user = User(id=form.id.data, name=form.name.data, about=form.about.data, passwd=hashed_password)
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
            password_matches = bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd)
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
    for school in schools:
        if school._type == 0:
            school._type = 'elementary'
        elif school._type == 1:
            school._type = 'middle'
        elif school._type == 2:
            school._type = 'high school'

        if school.status == 1:
            school.status = 'Open'
        elif school.status == 0:
            school.status = 'Closed'

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

        school = School(name=form.name.data, address= form.address.data, _type=school_type, status=school_status)
        db.session.add(school)
        db.session.commit()
        return redirect(url_for('list_schools'))
    return render_template('school_crud.html', form=form)

@login_required
@app.route('/schools/<int:id>', methods=['GET', 'POST'])
def update_school(id): 
    school = db.session.get(School, id)
    if school is None:
            return redirect(url_for('list_schools'))
    form = SchoolUpdateForm()

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
        db.session.commit()
        return redirect(url_for('list_schools'))
    # Fill in the form
    if request.method == 'GET':
        form.name.data = school.name
        form.address.data = school.address
        if school.type == 0:
            form.type.data = 'elementary'
        elif school.type == 1:
            form.type.data = 'middle'
        elif school.type == 2:
            form.type.data = 'high school'
        if school.status == 1:
            form.status.data = 'Open'
        elif school.status == 0:
            form.status.data = 'Closed'

    return render_template('school_crud.html', form=form)
    

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
    school = db.session.get(School, id)
    if school is None:
        return redirect(url_for('list_schools'))
    form = TransportationCostForm()
    
    form.from_school_id.data = id
    if form.validate_on_submit():
        transportation_cost = TransportationCost(
            from_school_id=id, 
            to_school_id=form.to_school_id.data,
            cost=form.cost.data
        )
        db.session.add(transportation_cost)
        db.session.commit()
        return redirect(url_for('list_schools'))
    # show the starting school ID
    form.from_school_id.data = id
    return render_template('transpo_cost_crud.html', form=form)

@login_required
@app.route('/schools/<int:id>/routes', methods=['GET', 'POST'])
def school_routes(id):
    schools = db.session.query(School).all()
    costs = db.session.query(TransportationCost).all()

    graph = {}

    # add all schools to the graph
    for school in schools:
        graph[school.id] = {}

    for cost in costs:
        s = cost.from_school_id
        d = cost.to_school_id
        w = cost.cost
        graph[s][d] = w

    #find the shortest paths starting from the given school
    dist, path = sp.dijkstra(graph, id)
    output = f'Shortest distances from school {id}:\n'
    output += f'{dist}<br>'

    for d in path:
        output += f'spf to {d}: {path[d]}<br>'

    return output
