from extensions import db

class College(db.Model):
    code = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Program(db.Model):
    code = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    college = db.Column(db.String(30), db.ForeignKey('college.code', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

class Student(db.Model):
    id_num = db.Column(db.String(8), primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    program_code = db.Column(db.String(30), db.ForeignKey('program.code', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)
    year = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)