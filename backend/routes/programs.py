from flask import Blueprint, jsonify, current_app, request, send_from_directory, url_for
import psycopg2
from models.programs import list_programs, get_program, create_program, update_program, delete_program

programs_bp = Blueprint('programs', __name__)

@programs_bp.route("/table/programs", methods=["GET"])
def serve_program_page():
    return send_from_directory(current_app.static_folder, ".next/server/app/table/programs.html")

@programs_bp.route("/programs", methods=["GET"])
def programs_list_route():
    try:
        attribute = request.args.get("attribute", "code")
        page = int(request.args.get("page", 1))
        ascending = int(request.args.get("ascending", 1))
        value = request.args.get("value")
        result, total_pages = list_programs(attribute, page, ascending, value)
        return jsonify([result, total_pages]), 200
    except Exception:
        current_app.logger.exception("list_programs failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@programs_bp.route("/programs/<string:code>", methods=["GET"])
def programs_get_route(code):
    try:
        program = get_program(code)
        if not program:
            return jsonify({"error": "Program not found"}), 404
        return jsonify(program), 200
    except Exception:
        current_app.logger.exception("get_program failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@programs_bp.route("/programs", methods=["POST"])
def programs_create_route():
    data = request.get_json(silent=True) or {}
    code = data.get("code")
    name = data.get("name")
    college = data.get("college")
    if not code or not name or not college:
        return jsonify({"error": "'code', 'name', and 'college' are required"}), 400
    try:
        new_program, err = create_program(code, name, college)
        if err == "college_not_found":
            return jsonify({"error": f"Cannot add program. College with code '{college}' does not exist."}), 400
        location = url_for('.programs_get_route', code=new_program['code'], _external=False)
        return jsonify(new_program), 201, {"Location": location}
    except psycopg2.IntegrityError:
        return jsonify({"error": f"Program with code '{code}' already exists."}), 409
    except Exception:
        current_app.logger.exception("create_program failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@programs_bp.route("/programs/edit/<string:old_code>", methods=["PUT"])
def programs_update_route(old_code):
    data = request.get_json(silent=True) or {}
    new_code = data.get("code")
    new_name = data.get("name")
    new_college = data.get("college")
    if not new_code or not new_name or not new_college:
        return jsonify({"error": "'code', 'name', and 'college' are required"}), 400
    try:
        updated_program, err = update_program(old_code, new_code, new_name, new_college)
        if err == "program_not_found":
            return jsonify({"error": "Program not found"}), 404
        if err == "college_not_found":
            return jsonify({"error": f"Cannot update program. College with code '{new_college}' does not exist."}), 400
        return jsonify(updated_program), 200
    except psycopg2.IntegrityError:
        return jsonify({"error": f"Program with code '{new_code}' already exists."}), 409
    except Exception:
        current_app.logger.exception("update_program failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@programs_bp.route("/programs/delete/<string:code>", methods=["DELETE"])
def programs_delete_route(code):
    try:
        deleted = delete_program(code)
        if not deleted:
            return jsonify({"error": "Program not found"}), 404
        return "", 204
    except Exception:
        current_app.logger.exception("delete_program failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500