from flask import Blueprint, request, jsonify, current_app, url_for, send_from_directory
import psycopg2
from models.colleges import list_colleges, get_college, create_college, update_college, delete_college

colleges_bp = Blueprint('colleges', __name__)

@colleges_bp.route("/table/colleges", methods=["GET"])
def serve_college_page():
    return send_from_directory(current_app.static_folder, ".next/server/app/table/colleges.html")

@colleges_bp.route("/colleges", methods=["GET"])
def colleges_list_route():
    try:
        attribute = request.args.get("attribute", "code")
        page = int(request.args.get("page", 1))
        ascending = int(request.args.get("ascending", 1))
        value = request.args.get("value")
        result, total_pages = list_colleges(attribute, page, ascending, value)
        return jsonify([result, total_pages]), 200
    except Exception:
        current_app.logger.exception("list_colleges failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@colleges_bp.route("/colleges/<string:code>", methods=["GET"])
def colleges_get_route(code):
    try:
        college = get_college(code)
        if not college:
            return jsonify({"error": "College not found"}), 404
        return jsonify(college), 200
    except Exception:
        current_app.logger.exception("get_college failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@colleges_bp.route("/colleges", methods=["POST"])
def colleges_create_route():
    data = request.get_json(silent=True) or {}
    code = data.get("code")
    name = data.get("name")
    if not code or not name:
        return jsonify({"error": "Both 'code' and 'name' are required"}), 400
    try:
        new_college = create_college(code, name)
        location = url_for(".colleges_get_route", code=new_college['code'], _external=False)
        return jsonify(new_college), 201, {"Location": location}
    except psycopg2.IntegrityError:
        return jsonify({"error": f"College with code '{code}' already exists."}), 409
    except Exception:
        current_app.logger.exception("create_college failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@colleges_bp.route("/colleges/edit/<string:old_code>", methods=["PUT"])
def colleges_update_route(old_code):
    data = request.get_json(silent=True) or {}
    new_code = data.get("code")
    new_name = data.get("name")
    if not new_code or not new_name:
        return jsonify({"error": "Both 'code' and 'name' are required"}), 400
    try:
        updated_college = update_college(old_code, new_code, new_name)
        if not updated_college:
            return jsonify({"error": "College not found"}), 404
        return jsonify(updated_college), 200
    except psycopg2.IntegrityError:
        return jsonify({"error": f"College with code '{new_code}' already exists."}), 409
    except Exception:
        current_app.logger.exception("update_college failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

@colleges_bp.route("/colleges/delete/<string:code>", methods=["DELETE"])
def colleges_delete_route(code):
    try:
        deleted = delete_college(code)
        if not deleted:
            return jsonify({"error": "College not found"}), 404
        return "", 204
    except Exception:
        current_app.logger.exception("delete_college failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500