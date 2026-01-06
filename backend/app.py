from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, JWTManager
from config import BaseConfig
import os
from extensions import get_db_connection
from routes.colleges import colleges_bp
from routes.programs import programs_bp
from routes.students import students_bp
from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env')

app = Flask(__name__, static_folder=os.path.join('static'), static_url_path='/static')
app.config.from_object(BaseConfig)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.register_blueprint(colleges_bp)
app.register_blueprint(programs_bp)
app.register_blueprint(students_bp)
@app.route("/register", methods=['POST'])
def register_user():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required."}), 400

        # Hash the password before storing
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        cur.execute('INSERT INTO "user" (username, password) VALUES (%s, %s)', (username, hashed_password))
        conn.commit()
        
        return jsonify({"message": f"User '{username}' created successfully."}), 201
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"error": f"User with username '{username}' already exists."}), 409
    except Exception as e:
        conn.rollback()
        print(f"An error occurred during registration: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500
    finally:
        cur.close()
        conn.close()


@app.route("/register", methods=["GET"])
def serve_register_page():
    return send_from_directory(app.static_folder, ".next/server/app/register.html")

@app.route("/login", methods=["GET"])
def serve_login_page():
    return send_from_directory(app.static_folder, ".next/server/app/login.html")

@app.route("/login", methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute('SELECT * FROM "user" WHERE username = %s', (username,))
        user = cur.fetchone()

        # Check if user exists and if the provided password hash matches the stored hash
        if user and bcrypt.check_password_hash(user['password'], password):
            # Create and return a new access token
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        
        return jsonify({"error": "Invalid username or password."}), 401
    finally:
        cur.close()
        conn.close()

@app.route("/")
def serve_index():
    return send_from_directory(os.path.join(app.static_folder, ".next", "server", "app"), "index.html")

@app.route("/about")
def serve_about():
    return send_from_directory(os.path.join(app.static_folder, ".next", "server", "app"), "about.html")

@app.route("/_next/static/<path:path>")
def serve_static_assets(path):
    return send_from_directory(os.path.join('static', '.next', 'static'), path)

@app.route("/media/<path:filename>", methods=["GET"])
def serve_static_files(filename):
    print(f"Serving static file: {filename}")
    return send_from_directory(app.static_folder, 'media/' + filename)

if __name__ == "__main__":
    app.run(host=BaseConfig.HOST, port=BaseConfig.PORT, debug=BaseConfig.DEBUG)