from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc, ForeignKey
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, JWTManager
from math import ceil
from config import BaseConfig

from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env')

app = Flask(__name__)
app.config.from_object(BaseConfig)
CORS(app)

bcrypt = Bcrypt(app)
app.config["JWT_SECRET_KEY"] = "absolute-nihility" # Change this!
jwt = JWTManager(app)

# Configure the PostgreSQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:na1227@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
def hello_world():
    return "Hello, World!"


# COLLEGE
class College(db.Model):
    code = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Program(db.Model):
    code = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    college = db.Column(db.String(30), db.ForeignKey('college.code', ondelete='SET NULL', onupdate='CASCADE'), nullable=False)

class Student(db.Model):
    id_num = db.Column(db.String(8), primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    program_code = db.Column(db.String(30), db.ForeignKey('program.code', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)
    year = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)

class User(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()

from blueprints import colleges, programs, students
app.register_blueprint(colleges.colleges_bp)
app.register_blueprint(programs.programs_bp)
app.register_blueprint(students.students_bp)

if __name__ == "__main__":
    app.run(host=BaseConfig.HOST, port=BaseConfig.PORT, debug=BaseConfig.DEBUG)