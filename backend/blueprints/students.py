# backend/blueprints/students.py
from flask import Blueprint, jsonify, current_app
from math import ceil
from extensions import db
from models import Student, Program
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc

students_bp = Blueprint('students', __name__)

@students_bp.route("/get/students/<string:attribute>/<int:page>/<int:ascending>")
def getStudents(attribute, page, ascending):
    try:
        att_str = attribute.lower()
        sort_map = {
            'id_num': Student.id_num,
            'fname': Student.fname,
            'lname': Student.lname,
            'program': Student.program_code,
            'year': Student.year,
            'sex': Student.sex
        }
        att = sort_map.get(att_str, Student.id_num)

        order = desc(att) if ascending == 0 else asc(att)

        students = Student.query.order_by(order).offset((page - 1) * 14).limit(14).all()
        total_students = Student.query.count()
        total_pages = ceil(total_students / 14)

        result = [[s.id_num, s.fname, s.lname, s.program_code, s.year, s.sex] for s in students]
        return jsonify([result, total_pages]), 200

    except Exception:
        current_app.logger.exception("An error occurred in getStudents")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


@students_bp.route("/search/students/<string:attribute>/<string:value>/<int:page>/<int:ascending>")
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

    except Exception:
        current_app.logger.exception("An error occurred in searchStudents")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


@students_bp.route("/insert/student/<string:id_num>/<string:fname>/<string:lname>/<string:program_code>/<int:year>/<string:sex>")
def insertStudent(id_num, fname, lname, program_code, year, sex):
    try:
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
    except Exception:
        db.session.rollback()
        current_app.logger.exception("An error occurred in insertStudent")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


@students_bp.route("/delete/student/<string:id_num>")
def deleteStudent(id_num):
    try:
        student = Student.query.get(id_num)
        if student is None:
            return jsonify({"error": f"Student with ID '{id_num}' not found."}), 404

        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": f"Student with ID '{id_num}' deleted successfully."}), 200

    except Exception:
        db.session.rollback()
        current_app.logger.exception("An error occurred in deleteStudent")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


@students_bp.route("/edit/student/<string:old_id_num>/<string:new_id_num>/<string:fname>/<string:lname>/<string:program_code>/<int:year>/<string:sex>")
def editStudent(old_id_num, new_id_num, fname, lname, program_code, year, sex):
    try:
        student = Student.query.get(old_id_num)
        if student is None:
            return jsonify({"error": f"Student with ID '{old_id_num}' not found."}), 404

        if not Program.query.get(program_code):
            return jsonify({"error": f"Program with code '{program_code}' does not exist."}), 400

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
    except Exception:
        db.session.rollback()
        current_app.logger.exception("An error occurred in editStudent")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500