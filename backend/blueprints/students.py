# backend/blueprints/students.py
from flask import Blueprint, jsonify, current_app, request, url_for
from math import ceil
from extensions import db
from models import Student, Program
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc

students_bp = Blueprint('students', __name__)


# ---- LIST / SEARCH ----
# GET /students?attribute=id_num&page=1&ascending=1&value=...
@students_bp.route("/students", methods=["GET"])
def list_students():
    try:
        attribute = request.args.get("attribute", "id_num")
        page = int(request.args.get("page", 1))
        ascending = int(request.args.get("ascending", 1))

        sort_map = {
            'id_num': Student.id_num,
            'fname': Student.fname,
            'lname': Student.lname,
            'program': Student.program_code,
            'year': Student.year,
            'sex': Student.sex
        }
        att = sort_map.get(attribute.lower(), Student.id_num)

        order = desc(att) if ascending == 0 else asc(att)
        per_page = 14

        value = request.args.get("value")
        if value:
            search_pattern = f"%{value}%"
            if attribute.lower() == 'year':
                # year search expects exact integer
                try:
                    year_val = int(value)
                except ValueError:
                    return jsonify({"error": "Invalid year value"}), 400
                base_query = Student.query.filter(Student.year == year_val)
            else:
                col = sort_map.get(attribute.lower(), Student.id_num)
                base_query = Student.query.filter(col.ilike(search_pattern))

            total = base_query.count()
            items = base_query.order_by(order).offset((page - 1) * per_page).limit(per_page).all()
        else:
            total = Student.query.count()
            items = Student.query.order_by(order).offset((page - 1) * per_page).limit(per_page).all()

        total_pages = ceil(total / per_page) if total > 0 else 0
        result = [[s.id_num, s.fname, s.lname, s.program_code, s.year, s.sex] for s in items]
        return jsonify([result, total_pages]), 200

    except Exception:
        current_app.logger.exception("list_students failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


# ---- GET single ----
# GET /students/<id_num>
@students_bp.route("/students/<string:id_num>", methods=["GET"])
def get_student(id_num):
    id_num = id_num.replace("-", "")
    student = Student.query.get(id_num)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({
        "id_num": student.id_num,
        "fname": student.fname,
        "lname": student.lname,
        "program_code": student.program_code,
        "year": student.year,
        "sex": student.sex
    }), 200


# ---- CREATE ----
# POST /students  body: { "id_num": "...", "fname": "...", "lname": "...", "program_code": "...", "year": 1, "sex": "M" }
@students_bp.route("/students", methods=["POST"])
def create_student():
    data = request.get_json(silent=True) or {}
    id_num = data.get("id_num").replace("-", "")
    fname = data.get("fname")
    lname = data.get("lname")
    program_code = data.get("program_code")
    year = data.get("year")
    sex = data.get("sex")

    if not all([id_num, fname, lname, program_code, year, sex]):
        return jsonify({"error": "'id_num', 'fname', 'lname', 'program_code', 'year', and 'sex' are required"}), 400

    try:
        if not Program.query.get(program_code):
            return jsonify({"error": f"Program with code '{program_code}' does not exist."}), 400

        new_student = Student(
            id_num=id_num,
            fname=fname,
            lname=lname,
            program_code=program_code,
            year=int(year),
            sex=sex
        )
        db.session.add(new_student)
        db.session.commit()
        location = url_for('.get_student', id_num=new_student.id_num, _external=False)
        return jsonify({
            "id_num": new_student.id_num,
            "fname": new_student.fname,
            "lname": new_student.lname,
            "program_code": new_student.program_code,
            "year": new_student.year,
            "sex": new_student.sex
        }), 201, {"Location": location}

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"Student with ID '{id_num}' already exists."}), 409
    except Exception:
        db.session.rollback()
        current_app.logger.exception("create_student failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


# ---- UPDATE ----
# PUT /students/<old_id_num>  body: { "id_num": "...", "fname": "...", "lname": "...", "program_code": "...", "year": 1, "sex": "M" }
@students_bp.route("/students/edit/<string:old_id_num>", methods=["PUT"])
def update_student(old_id_num):
    old_id_num = old_id_num.replace("-", "")
    data = request.get_json(silent=True) or {}
    new_id_num = data.get("id_num").replace("-", "")
    fname = data.get("fname")
    lname = data.get("lname")
    program_code = data.get("program_code")
    year = data.get("year")
    sex = data.get("sex")

    if not all([new_id_num, fname, lname, program_code, year, sex]):
        return jsonify({"error": "'id_num', 'fname', 'lname', 'program_code', 'year', and 'sex' are required"}), 400

    try:
        student = Student.query.get(old_id_num)
        if not student:
            return jsonify({"error": "Student not found"}), 404

        if not Program.query.get(program_code):
            return jsonify({"error": f"Program with code '{program_code}' does not exist."}), 400

        student.id_num = new_id_num
        student.fname = fname
        student.lname = lname
        student.program_code = program_code
        student.year = int(year)
        student.sex = sex

        db.session.commit()
        return jsonify({
            "id_num": student.id_num,
            "fname": student.fname,
            "lname": student.lname,
            "program_code": student.program_code,
            "year": student.year,
            "sex": student.sex
        }), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"A student with ID '{new_id_num}' already exists."}), 409
    except Exception:
        db.session.rollback()
        current_app.logger.exception("update_student failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


# ---- DELETE ----
# DELETE /students/<id_num>
@students_bp.route("/students/delete/<string:id_num>", methods=["DELETE"])
def delete_student(id_num):
    id_num = id_num.replace("-", "")
    try:
        student = Student.query.get(id_num)
        if not student:
            return jsonify({"error": "Student not found"}), 404
        db.session.delete(student)
        db.session.commit()
        return "", 204
    except Exception:
        db.session.rollback()
        current_app.logger.exception("delete_student failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500