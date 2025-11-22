# backend/blueprints/programs.py
from flask import Blueprint, jsonify, current_app
from math import ceil
from extensions import db
from models import Program, College
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc

programs_bp = Blueprint('programs', __name__)

@programs_bp.route("/get/programs/<string:attribute>/<int:page>/<int:ascending>")
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

    except Exception:
        current_app.logger.exception("An error occurred in getPrograms")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


@programs_bp.route("/search/programs/<string:attribute>/<string:value>/<int:page>/<int:ascending>")
def searchProgram(attribute, value, page, ascending):
    try:
        search_pattern = f"%{value}%"
        att_str = attribute.lower()

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

        total_results = base_query.count()
        total_pages = ceil(total_results / 14)

        order = desc(sort_att) if ascending == 0 else asc(sort_att)
        paginated_results = base_query.order_by(order).offset((page - 1) * 14).limit(14).all()

        formatted_results = [[p.code, p.name, p.college] for p in paginated_results]

        return jsonify([formatted_results, total_pages]), 200

    except Exception:
        current_app.logger.exception("An error occurred in searchProgram")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


@programs_bp.route("/insert/program/<string:code>/<string:name>/<string:college>")
def insertProgram(code, name, college):
    try:
        college_exists = College.query.get(college)
        if not college_exists:
            return jsonify({"error": f"Cannot add program. College with code '{college}' does not exist."}), 400

        program = Program(code=code, name=name, college=college)
        db.session.add(program)
        db.session.commit()
        return jsonify([program.code, program.name]), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"Program with code '{code}' already exists."}), 409
    except Exception:
        db.session.rollback()
        current_app.logger.exception("An error occurred in insertProgram")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


@programs_bp.route("/delete/program/<string:code>")
def deleteProgram(code):
    try:
        program = Program.query.get(code)
        if program is None:
            return jsonify({"error": f"Program with code '{code}' not found."}), 404

        db.session.delete(program)
        db.session.commit()
        return jsonify({"message": f"Program with code '{code}' deleted successfully."}), 200

    except Exception:
        db.session.rollback()
        current_app.logger.exception("An error occurred in deleteProgram")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


@programs_bp.route("/edit/program/<string:oldCode>/<string:newCode>/<string:newName>/<string:newCollege>")
def editProgram(oldCode, newCode, newName, newCollege):
    try:
        program = Program.query.get(oldCode)
        if program is None:
            return jsonify({"error": f"Program with code '{oldCode}' not found."}), 404

        college_exists = College.query.get(newCollege)
        if not college_exists:
            return jsonify({"error": f"Cannot update program. College with code '{newCollege}' does not exist."}), 400

        program.code = newCode
        program.name = newName
        program.college = newCollege

        db.session.commit()
        return jsonify([program.code, program.name, program.college]), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"Program with code '{newCode}' already exists."}), 409
    except Exception:
        db.session.rollback()
        current_app.logger.exception("An error occurred in editProgram")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500