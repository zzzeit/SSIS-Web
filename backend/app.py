from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc, ForeignKey
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

with app.app_context():
    db.create_all()

@app.route("/get/colleges/<string:attribute>/<int:page>/<int:ascending>")
def getColleges(page, attribute, ascending):
    try:
        if attribute.lower() == 'name':
            att = College.name
        else:
            att = College.code
        
        order = desc(att)
        if ascending == 1:
            order = asc(att)
            
        colleges = College.query.order_by(order).offset((page - 1) * 14).limit(14).all()
        total_colleges = College.query.count()
        total_pages = ceil(total_colleges / 14)
        
        result = [[c.code, c.name] for c in colleges]
        return jsonify([result, total_pages]), 200
        
    except Exception as e:
        # Log the error for debugging on the server
        print(f"An error occurred in getColleges: {e}")
        # Return a generic 500 error to the client
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

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

@app.route("/search/colleges/<string:attribute>/<string:value>/<int:page>/<int:ascending>")
def searchCollege(value, attribute, page, ascending):
    search_pattern = f"%{value}%"

    # 1. Build the base query with the filter
    if attribute.lower() == 'name':
        base_query = College.query.filter(College.name.ilike(search_pattern))
        att = College.name
    elif attribute.lower() == 'code':
        base_query = College.query.filter(College.code.ilike(search_pattern))
        att = College.code
    else:
        return jsonify({"error": f"Searching by attribute '{attribute}' is not supported."}), 400

    # 2. Get the total count from the base query
    total_results = base_query.count()
    total_pages = ceil(total_results / 14) # Assuming 14 items per page

    # 3. Apply sorting and pagination to the base query
    order = desc(att) if ascending == 0 else asc(att)
    
    paginated_results = base_query.order_by(order).offset((page - 1) * 14).limit(14).all()

    # 4. Format the results for the current page
    formatted_results = [[c.code, c.name] for c in paginated_results]

    # 5. Return both the paginated data and the total page count
    return jsonify([formatted_results, total_pages])

# PROGRAMS
@app.route("/get/programs/<string:attribute>/<int:page>/<int:ascending>")
def getPrograms(attribute, page, ascending):
    try:
        if attribute.lower() == 'code':
            att = Program.code
        elif attribute.lower() == 'name':
            att = Program.name
        else:
            att = Program.college
        
        order = desc(att)
        if ascending == 1:
            order = asc(att)
            
        programs = Program.query.order_by(order).offset((page - 1) * 14).limit(14).all()
        total_programs = Program.query.count()
        total_pages = ceil(total_programs / 14)
        
        result = [[p.code, p.name, p.college] for p in programs]
        return jsonify([result, total_pages]), 200
        
    except Exception as e:
        print(f"An error occurred in getPrograms: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@app.route("/search/programs/<string:attribute>/<string:value>/<int:page>/<int:ascending>")
def searchProgram(attribute, value, page, ascending):
    try:
        search_pattern = f"%{value}%"
        att_str = attribute.lower()

        # 1. Build the base query with the filter
        if att_str == 'name':
            base_query = Program.query.filter(Program.name.ilike(search_pattern))
            sort_att = Program.name
        elif att_str == 'code':
            base_query = Program.query.filter(Program.code.ilike(search_pattern))
            sort_att = Program.code
        elif att_str == 'college':
            base_query = Program.query.filter(Program.college.ilike(search_pattern))
            sort_att = Program.college
        else:
            return jsonify({"error": f"Searching by attribute '{attribute}' is not supported."}), 400

        # 2. Get the total count from the filtered query
        total_results = base_query.count()
        total_pages = ceil(total_results / 14)

        # 3. Apply sorting and pagination
        order = desc(sort_att) if ascending == 0 else asc(sort_att)
        paginated_results = base_query.order_by(order).offset((page - 1) * 14).limit(14).all()

        # 4. Format results, including the college code
        formatted_results = [[p.code, p.name, p.college] for p in paginated_results]

        # 5. Return paginated data and total page count
        return jsonify([formatted_results, total_pages]), 200
        
    except Exception as e:
        print(f"An error occurred in searchProgram: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@app.route("/insert/program/<string:code>/<string:name>/<string:college>")
def insertProgram(code, name, college):
    try:
        # 1. Check if the referenced college exists first
        college_exists = College.query.get(college)
        if not college_exists:
            # 2. If not, return a specific error (400 Bad Request is appropriate)
            return jsonify({"error": f"Cannot add program. College with code '{college}' does not exist."}), 400

        program = Program(code=code, name=name, college=college)
        db.session.add(program)
        db.session.commit()
        return jsonify([program.code, program.name]), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"Program with code '{code}' already exists."}), 409
        
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@app.route("/delete/program/<string:code>")
def deleteProgram(code):
    try:
        # Find the program by its primary key
        program = Program.query.get(code)

        # If the program doesn't exist, return a 404 error
        if program is None:
            return jsonify({"error": f"Program with code '{code}' not found."}), 404

        # Delete the program object and commit the session
        db.session.delete(program)
        db.session.commit()

        # Return a success message with a 200 OK status
        return jsonify({"message": f"Program with code '{code}' deleted successfully."}), 200

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while deleting program: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@app.route("/edit/program/<string:oldCode>/<string:newCode>/<string:newName>/<string:newCollege>")
def editProgram(oldCode, newCode, newName, newCollege):
    try:
        # Find the program to be edited
        program = Program.query.get(oldCode)
        if program is None:
            return jsonify({"error": f"Program with code '{oldCode}' not found."}), 404

        # Proactively check if the new college exists before trying to update
        college_exists = College.query.get(newCollege)
        if not college_exists:
            return jsonify({"error": f"Cannot update program. College with code '{newCollege}' does not exist."}), 400

        # Update the program's attributes
        program.code = newCode
        program.name = newName
        program.college = newCollege
        
        # Commit the changes to the database
        db.session.commit()
        
        # Return the updated data with a 200 OK status
        return jsonify([program.code, program.name, program.college]), 200

    except IntegrityError:
        # This error will be caught if the newCode already exists in the program table
        db.session.rollback()
        return jsonify({"error": f"Program with code '{newCode}' already exists."}), 409
        
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while editing program: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


# STUDENTS
@app.route("/get/students/<string:attribute>/<int:page>/<int:ascending>")
def getStudents(attribute, page, ascending):
    try:
        att_str = attribute.lower()
        # Map the attribute string to the actual model column
        sort_map = {
            'id_num': Student.id_num,
            'fname': Student.fname,
            'lname': Student.lname,
            'program': Student.program_code,
            'year': Student.year,
            'sex': Student.sex
        }
        # Default to sorting by id_num if attribute is invalid
        att = sort_map.get(att_str, Student.id_num)
        
        order = desc(att) if ascending == 0 else asc(att)
            
        students = Student.query.order_by(order).offset((page - 1) * 14).limit(14).all()
        total_students = Student.query.count()
        total_pages = ceil(total_students / 14)
        
        result = [[s.id_num, s.fname, s.lname, s.program_code, s.year, s.sex] for s in students]
        return jsonify([result, total_pages]), 200
        
    except Exception as e:
        print(f"An error occurred in getStudents: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@app.route("/search/students/<string:attribute>/<string:value>/<int:page>/<int:ascending>")
def searchStudents(attribute, value, page, ascending):
    try:
        search_pattern = f"%{value}%"
        att_str = attribute.lower()

        sort_map = {
            'id_num': Student.id_num,
            'fname': Student.fname,
            'lname': Student.lname,
            'program': Student.program_code,
            'year': Student.year,
            'sex': Student.sex
        }

        if att_str not in sort_map:
            return jsonify({"error": f"Searching by attribute '{attribute}' is not supported."}), 400

        search_column = sort_map[att_str]
        
        # Handle integer column search separately
        if att_str == 'year':
             base_query = Student.query.filter(Student.year == int(value))
        else:
             base_query = Student.query.filter(search_column.ilike(search_pattern))
        
        total_results = base_query.count()
        total_pages = ceil(total_results / 14)

        order = desc(search_column) if ascending == 0 else asc(search_column)
        paginated_results = base_query.order_by(order).offset((page - 1) * 14).limit(14).all()

        formatted_results = [[s.id_num, s.fname, s.lname, s.program_code, s.year, s.sex] for s in paginated_results]
        return jsonify([formatted_results, total_pages]), 200
        
    except Exception as e:
        print(f"An error occurred in searchStudents: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@app.route("/insert/student/<string:id_num>/<string:fname>/<string:lname>/<string:program_code>/<int:year>/<string:sex>")
def insertStudent(id_num, fname, lname, program_code, year, sex):
    try:
        # Check if the referenced program exists
        program_exists = Program.query.get(program_code)
        if not program_exists:
            return jsonify({"error": f"Program with code '{program_code}' does not exist."}), 400

        new_student = Student(
            id_num=id_num,
            fname=fname,
            lname=lname,
            program_code=program_code,
            year=year,
            sex=sex
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({"message": "Student created successfully."}), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"Student with ID '{id_num}' already exists."}), 409
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred in insertStudent: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@app.route("/delete/student/<string:id_num>")
def deleteStudent(id_num):
    try:
        student = Student.query.get(id_num)
        if student is None:
            return jsonify({"error": f"Student with ID '{id_num}' not found."}), 404

        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": f"Student with ID '{id_num}' deleted successfully."}), 200

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while deleting student: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@app.route("/edit/student/<string:old_id_num>/<string:new_id_num>/<string:fname>/<string:lname>/<string:program_code>/<int:year>/<string:sex>")
def editStudent(old_id_num, new_id_num, fname, lname, program_code, year, sex):
    try:
        student = Student.query.get(old_id_num)
        if student is None:
            return jsonify({"error": f"Student with ID '{old_id_num}' not found."}), 404

        # Check if the new program exists, if it's being changed
        if not Program.query.get(program_code):
            return jsonify({"error": f"Program with code '{program_code}' does not exist."}), 400

        # Update fields from URL parameters
        student.id_num = new_id_num
        student.fname = fname
        student.lname = lname
        student.program_code = program_code
        student.year = year
        student.sex = sex
        
        db.session.commit()
        return jsonify({"message": "Student updated successfully."}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"A student with ID '{new_id_num}' already exists."}), 409
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while editing student: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)