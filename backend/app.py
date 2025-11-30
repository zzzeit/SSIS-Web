from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc, ForeignKey
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, JWTManager
from math import ceil
from config import BaseConfig
import os

from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env')

app = Flask(__name__)
app.config.from_object(BaseConfig)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

from extensions import db
db.init_app(app)

class User(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(120), nullable=False)
from models import College, Program, Student
with app.app_context():
    db.create_all()

from blueprints import colleges, programs, students
app.register_blueprint(colleges.colleges_bp)
app.register_blueprint(programs.programs_bp)
app.register_blueprint(students.students_bp)

@app.route("/register", methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required."}), 400

        # Hash the password before storing
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"message": f"User '{username}' created successfully."}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"User with username '{username}' already exists."}), 409
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred during registration: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route("/login", methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    user = User.query.get(username)

    # Check if user exists and if the provided password hash matches the stored hash
    if user and bcrypt.check_password_hash(user.password, password):
        # Create and return a new access token
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    
    return jsonify({"error": "Invalid username or password."}), 401

if __name__ == "__main__":
    app.run(host=BaseConfig.HOST, port=BaseConfig.PORT, debug=BaseConfig.DEBUG)