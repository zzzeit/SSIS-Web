# backend/blueprints/programs.py
from flask import Blueprint, jsonify, current_app, request, send_from_directory, url_for
from math import ceil
from extensions import db
from models import Program, College
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc

programs_bp = Blueprint('programs', __name__)

@programs_bp.route("/table/programs", methods=["GET"])
def serve_program_page():
    return send_from_directory(current_app.static_folder, ".next/server/app/table/programs.html")

# ---- LIST / SEARCH ----
# GET /programs?attribute=code&page=1&ascending=1&value=...
@programs_bp.route("/programs", methods=["GET"])
def list_programs():
    try:
        attribute = request.args.get("attribute", "code")
        page = int(request.args.get("page", 1))
        ascending = int(request.args.get("ascending", 1))

        if attribute.lower() == 'name':
            att = Program.name
        elif attribute.lower() == 'college':
            att = Program.college
        else:
            att = Program.code

        order = desc(att) if ascending == 0 else asc(att)
        per_page = 14

        value = request.args.get("value")
        if value:
            search_pattern = f"%{value}%"
            if attribute.lower() == 'name':
                base_query = Program.query.filter(Program.name.ilike(search_pattern))
            elif attribute.lower() == 'college':
                base_query = Program.query.filter(Program.college.ilike(search_pattern))
            else:
                base_query = Program.query.filter(Program.code.ilike(search_pattern))

            total = base_query.count()
            items = base_query.order_by(order).offset((page - 1) * per_page).limit(per_page).all()
        else:
            total = Program.query.count()
            items = Program.query.order_by(order).offset((page - 1) * per_page).limit(per_page).all()

        total_pages = ceil(total / per_page) if total > 0 else 0
        result = [[p.code, p.name, p.college] for p in items]
        return jsonify([result, total_pages]), 200

    except Exception:
        current_app.logger.exception("list_programs failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


# ---- GET single ----
# GET /programs/<code>
@programs_bp.route("/programs/<string:code>", methods=["GET"])
def get_program(code):
    program = Program.query.get(code)
    if not program:
        return jsonify({"error": "Program not found"}), 404
    return jsonify({"code": program.code, "name": program.name, "college": program.college}), 200


# ---- CREATE ----
# POST /programs  body: { "code": "...", "name": "...", "college": "..." }
@programs_bp.route("/programs", methods=["POST"])
def create_program():
    data = request.get_json(silent=True) or {}
    code = data.get("code")
    name = data.get("name")
    college = data.get("college")
    if not code or not name or not college:
        return jsonify({"error": "'code', 'name', and 'college' are required"}), 400

    try:
        college_exists = College.query.get(college)
        if not college_exists:
            return jsonify({"error": f"Cannot add program. College with code '{college}' does not exist."}), 400

        program = Program(code=code, name=name, college=college)
        db.session.add(program)
        db.session.commit()
        location = url_for('.get_program', code=program.code, _external=False)
        return jsonify({"code": program.code, "name": program.name, "college": program.college}), 201, {"Location": location}

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"Program with code '{code}' already exists."}), 409
    except Exception:
        db.session.rollback()
        current_app.logger.exception("create_program failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


# ---- UPDATE ----
# PUT /programs/<old_code>  body: { "code": "...", "name": "...", "college": "..." }
@programs_bp.route("/programs/edit/<string:old_code>", methods=["PUT"])
def update_program(old_code):
    data = request.get_json(silent=True) or {}
    new_code = data.get("code")
    new_name = data.get("name")
    new_college = data.get("college")
    if not new_code or not new_name or not new_college:
        return jsonify({"error": "'code', 'name', and 'college' are required"}), 400

    try:
        program = Program.query.get(old_code)
        if not program:
            return jsonify({"error": "Program not found"}), 404

        college_exists = College.query.get(new_college)
        if not college_exists:
            return jsonify({"error": f"Cannot update program. College with code '{new_college}' does not exist."}), 400

        program.code = new_code
        program.name = new_name
        program.college = new_college
        db.session.commit()
        return jsonify({"code": program.code, "name": program.name, "college": program.college}), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"Program with code '{new_code}' already exists."}), 409
    except Exception:
        db.session.rollback()
        current_app.logger.exception("update_program failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


# ---- DELETE ----
# DELETE /programs/<code>
@programs_bp.route("/programs/delete/<string:code>", methods=["DELETE"])
def delete_program(code):
    try:
        program = Program.query.get(code)
        if not program:
            return jsonify({"error": "Program not found"}), 404
        db.session.delete(program)
        db.session.commit()
        return "", 204
    except Exception:
        db.session.rollback()
        current_app.logger.exception("delete_program failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500