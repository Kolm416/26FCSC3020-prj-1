'''
CSC3020 - Software Engineering Fundamentals
Instructor: Thyago Mota
Student(s): Leigha Lennon
Description: Project 1 - Schools
'''

from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, InputRequired

class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    about = TextAreaField('About')
    passwd = PasswordField('Password', validators=[DataRequired()])
    passwd_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class LoginForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class SchoolCreateForm(FlaskForm):
    # id = IntegerField('Id', validators=[InputRequired()])
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address')
    type = SelectField('Type', choices=['elementary', 'middle', 'high school'], validators=[DataRequired()])
    status = SelectField('Status', choices=['Open', 'Closed'])
    submit = SubmitField('Confirm')

class SchoolUpdateForm(FlaskForm):
    # id = IntegerField('Id', render_kw = {'disabled': 'disabled'})
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address')
    type = SelectField('Type', choices=['elementary', 'middle', 'high school'], validators=[DataRequired()])
    status = SelectField('Status', choices=['Open', 'Closed'])
    submit = SubmitField('Confirm')

class SchoolDeleteForm(FlaskForm):
    # id = IntegerField('Id', render_kw = {'disabled': 'disabled'})
    name = StringField('Name', render_kw = {'disabled': 'disabled'})
    address = StringField('Address', render_kw = {'disabled': 'disabled'})
    type = SelectField('Type', choices=['elementary', 'middle', 'high school'], render_kw = {'disabled': 'disabled'})
    status = SelectField('Status', choices=['Open', 'Closed'], render_kw = {'disabled': 'disabled'})
    submit = SubmitField('Confirm')

class TransportationCostForm(FlaskForm):
    from_school_id = IntegerField('From', render_kw = {'disabled': 'disabled'})
    to_school_id = IntegerField('To', validators=[InputRequired()])
    cost = IntegerField('Cost', validators=[DataRequired()])
    submit = SubmitField('Confirm')