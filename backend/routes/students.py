from flask import Blueprint, jsonify, current_app, request, send_from_directory, url_for
import psycopg2
from models.students import list_students, get_student, create_student, update_student, delete_student

students_bp = Blueprint('students', __name__)

@students_bp.route("/table/students", methods=["GET"])
def serve_student_page():
    return send_from_directory(current_app.static_folder, ".next/server/app/table/students.html")

@students_bp.route("/students", methods=["GET"])
def students_list_route():
    try:
        attribute = request.args.get("attribute", "id_num")
        page = int(request.args.get("page", 1))
        ascending = int(request.args.get("ascending", 1))
        value = request.args.get("value")
        filters = {
            "Program": request.args.get("Program"),
            "Year": request.args.get("Year"),
            "Sex": request.args.get("Sex")
        }
        (result, total_pages), err = list_students(attribute, page, ascending, value, filters)
        if err == "invalid_year":
            return jsonify({"error": "Invalid year value"}), 400
        if err == "invalid_year_filter":
            return jsonify({"error": "Invalid year filter value"}), 400
        return jsonify([result, total_pages]), 200
    except Exception:
        current_app.logger.exception("list_students failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@students_bp.route("/students/<string:id_num>", methods=["GET"])
def students_get_route(id_num):
    id_num = id_num.replace("-", "")
    try:
        student = get_student(id_num)
        if not student:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(student), 200
    except Exception:
        current_app.logger.exception("get_student failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@students_bp.route("/students", methods=["POST"])
def students_create_route():
    data = request.get_json(silent=True) or {}
    id_num = data.get("id_num", "").replace("-", "")
    fname = data.get("fname")
    lname = data.get("lname")
    program_code = data.get("program_code")
    year = data.get("year")
    sex = data.get("sex")

    if not all([id_num, fname, lname, program_code, year, sex]):
        return jsonify({"error": "'id_num', 'fname', 'lname', 'program_code', 'year', and 'sex' are required"}), 400

    if not id_num.isdigit():
        return jsonify({"error": "ID number must be numeric"}), 400
    try:
        year = int(year)
    except ValueError:
        return jsonify({"error": "Year must be an integer"}), 400

    try:
        new_student, err = create_student(id_num, fname, lname, program_code, year, sex)
        if err == "program_not_found":
            return jsonify({"error": f"Program with code '{program_code}' does not exist."}), 400
        location = url_for('.students_get_route', id_num=new_student['id_num'], _external=False)
        return jsonify(new_student), 201, {"Location": location}
    except psycopg2.IntegrityError:
        return jsonify({"error": f"Student with ID '{id_num}' already exists."}), 409
    except Exception:
        current_app.logger.exception("create_student failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@students_bp.route("/students/edit/<string:old_id_num>", methods=["PUT"])
def students_update_route(old_id_num):
    old_id_num = old_id_num.replace("-", "")
    data = request.get_json(silent=True) or {}
    new_id_num = data.get("id_num", "").replace("-", "")
    fname = data.get("fname")
    lname = data.get("lname")
    program_code = data.get("program_code")
    year = data.get("year")
    sex = data.get("sex")

    if not all([new_id_num, fname, lname, program_code, year, sex]):
        return jsonify({"error": "'id_num', 'fname', 'lname', 'program_code', 'year', and 'sex' are required"}), 400

    if not new_id_num.isdigit():
        return jsonify({"error": "ID number must be numeric"}), 400
    try:
        year = int(year)
    except ValueError:
        return jsonify({"error": "Year must be an integer"}), 400

    try:
        updated_student, err = update_student(old_id_num, new_id_num, fname, lname, program_code, year, sex)
        if err == "student_not_found":
            return jsonify({"error": "Student not found"}), 404
        if err == "program_not_found":
            return jsonify({"error": f"Program with code '{program_code}' does not exist."}), 400
        return jsonify(updated_student), 200
    except psycopg2.IntegrityError:
        return jsonify({"error": f"A student with ID '{new_id_num}' already exists."}), 409
    except Exception:
        current_app.logger.exception("update_student failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@students_bp.route("/students/delete/<string:id_num>", methods=["DELETE"])
def students_delete_route(id_num):
    id_num = id_num.replace("-", "")
    try:
        deleted = delete_student(id_num)
        if not deleted:
            return jsonify({"error": "Student not found"}), 404
        return "", 204
    except Exception:
        current_app.logger.exception("delete_student failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500