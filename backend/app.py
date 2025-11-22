from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc, ForeignKey
from math import ceil
from config import BaseConfig

from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env')

app = Flask(__name__)
app.config.from_object(BaseConfig)
CORS(app)

from extensions import db
db.init_app(app)

from models import College, Program, Student
with app.app_context():
    db.create_all()

from blueprints import colleges, programs, students
app.register_blueprint(colleges.colleges_bp)
app.register_blueprint(programs.programs_bp)
app.register_blueprint(students.students_bp)

if __name__ == "__main__":
    app.run(host=BaseConfig.HOST, port=BaseConfig.PORT, debug=BaseConfig.DEBUG)