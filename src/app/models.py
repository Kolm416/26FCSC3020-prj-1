'''
CSC3020 - Software Engineering Fundamentals
Instructor: Thyago Mota
Student(s):
Description: Project 1 - Schools
'''

from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    about = db.Column(db.String)
    passwd = db.Column(db.LargeBinary)

class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    _type = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f'<School(id={self.id}, name={self.name})>'

class TransportationCost(db.Model):
    __tablename__ = 'transportation_costs'
    from_school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False, primary_key=True)
    to_school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False, primary_key=True)
    cost = db.Column(db.Integer, nullable=False)
    from_school = db.relationship("School", foreign_keys=[from_school_id])
    to_school = db.relationship("School", foreign_keys=[to_school_id])

    def __str__(self):
        return f'<Cost(from_school={self.from_school}, to_school={self.to_school}, cost={self.cost})>'
