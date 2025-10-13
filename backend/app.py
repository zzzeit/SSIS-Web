from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc
from math import ceil

# 2. Create an instance of the Flask class
app = Flask(__name__)
CORS(app)
# Configure the PostgreSQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:na1227@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
def hello_world():
    return "Hello, World!"


# COLLEGE
class College(db.Model):
    code = db.Column(db.String(16), primary_key=True)
    name = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/get/colleges/<int:page>/<int:ascending>")
def getColleges(page, ascending):
    order = desc(College.code)
    if ascending == 1:
        order = asc(College.code)
    colleges = College.query.order_by(order).offset((page - 1) * 14).limit(14).all()
    total_colleges = College.query.count()
    total_pages = ceil(total_colleges / 14)
    result = [[c.code, c.name] for c in colleges]
    return jsonify([result, total_pages])

@app.route("/insert/college/<string:code>/<string:name>")
def insertCollege(code, name):
    try:
        college = College(code=code, name=name)
        db.session.add(college)
        db.session.commit()
        # Return the newly created object with a 201 Created status
        return jsonify([college.code, college.name]), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"College with code '{code}' already exists."}), 409
    except Exception as e:
        db.session.rollback()
        # It's a good idea to log the error here
        print(f"An error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    
@app.route("/delete/college/<string:code>")
def deleteCollege(code):
    try:
        # Find the college by its primary key
        college = College.query.get(code)

        # If the college doesn't exist, return a 404 error
        if college is None:
            return jsonify({"error": f"College with code '{code}' not found."}), 404

        # Delete the college object and commit the session
        db.session.delete(college)
        db.session.commit()

        # Return a success message
        return jsonify({"message": f"College with code '{code}' deleted successfully."}), 200

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@app.route("/edit/college/<string:oldCode>/<string:newCode>/<string:newName>")
def editCollege(oldCode, newCode, newName):
    try:
        college = College.query.get(oldCode)
        if college is None:
            return jsonify({"error": f"College with code '{oldCode}' not found."}), 404

        college.code = newCode
        college.name = newName
        db.session.commit()
        return jsonify([college.code, college.name]), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"College with code '{newCode}' already exists."}), 409
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

# In backend/app.py

@app.route("/search/colleges/<string:attribute>/<string:value>/<int:page>/<int:ascending>")
def searchCollege(value, attribute, page, ascending):
    search_pattern = f"%{value}%"

    # 1. Build the base query with the filter
    if attribute == 'name':
        base_query = College.query.filter(College.name.ilike(search_pattern))
    elif attribute == 'code':
        base_query = College.query.filter(College.code.ilike(search_pattern))
    else:
        return jsonify({"error": f"Searching by attribute '{attribute}' is not supported."}), 400

    # 2. Get the total count from the base query
    total_results = base_query.count()
    total_pages = ceil(total_results / 14) # Assuming 14 items per page

    # 3. Apply sorting and pagination to the base query
    order = desc(College.code) if ascending == 0 else asc(College.code)
    
    paginated_results = base_query.order_by(order).offset((page - 1) * 14).limit(14).all()

    # 4. Format the results for the current page
    formatted_results = [[c.code, c.name] for c in paginated_results]

    # 5. Return both the paginated data and the total page count
    return jsonify([formatted_results, total_pages])

# This part is optional but good practice to run the app
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)