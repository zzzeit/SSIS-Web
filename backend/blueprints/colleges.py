from flask import Blueprint, request, jsonify, current_app, url_for, send_from_directory
from math import ceil
from extensions import db
from models import College
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc

colleges_bp = Blueprint('colleges', __name__)

@colleges_bp.route("/table/colleges", methods=["GET"])
def serve_college_page():
    return send_from_directory(current_app.static_folder, ".next/server/app/table/colleges.html")


# ---- LIST / SEARCH ----
# GET /colleges?attribute=code&page=1&ascending=1
@colleges_bp.route("/colleges", methods=["GET"])
def list_colleges():
    try:
        attribute = request.args.get("attribute", "code")
        page = int(request.args.get("page", 1))
        ascending = int(request.args.get("ascending", 1))

        if attribute.lower() == 'name':
            att = College.name
        else:
            att = College.code

        order = desc(att) if ascending == 0 else asc(att)
        per_page = 14

        # optional search value
        value = request.args.get("value")
        if value:
            search_pattern = f"%{value}%"
            if attribute.lower() == 'name':
                base_query = College.query.filter(College.name.ilike(search_pattern))
            else:
                base_query = College.query.filter(College.code.ilike(search_pattern))
            total = base_query.count()
            items = base_query.order_by(order).offset((page - 1) * per_page).limit(per_page).all()
        else:
            total = College.query.count()
            items = College.query.order_by(order).offset((page - 1) * per_page).limit(per_page).all()

        total_pages = ceil(total / per_page) if total > 0 else 0
        result = [[c.code, c.name] for c in items]
        return jsonify([result, total_pages]), 200

    except Exception:
        current_app.logger.exception("list_colleges failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

# ---- GET single ----
# GET /colleges/<code>
@colleges_bp.route("/colleges/<string:code>", methods=["GET"])
def get_college(code):
    college = College.query.get(code)
    if not college:
        return jsonify({"error": "College not found"}), 404
    return jsonify({"code": college.code, "name": college.name}), 200

# ---- CREATE ----
# POST /colleges  body: { "code": "...", "name": "..." }
@colleges_bp.route("/colleges", methods=["POST"])
def create_college():
    data = request.get_json(silent=True) or {}
    code = data.get("code")
    name = data.get("name")
    if not code or not name:
        return jsonify({"error": "Both 'code' and 'name' are required"}), 400

    try:
        college = College(code=code, name=name)
        db.session.add(college)
        db.session.commit()
        # Return 201 with Location header for the new resource
        location = url_for(".get_college", code=college.code, _external=False)
        return jsonify({"code": college.code, "name": college.name}), 201, {"Location": location}
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"College with code '{code}' already exists."}), 409
    except Exception:
        db.session.rollback()
        current_app.logger.exception("create_college failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

# ---- UPDATE ----
# PUT /colleges/<old_code>  body: { "code": "...", "name": "..." }
@colleges_bp.route("/colleges/edit/<string:old_code>", methods=["PUT"])
def update_college(old_code):
    data = request.get_json(silent=True) or {}
    new_code = data.get("code")
    new_name = data.get("name")
    if not new_code or not new_name:
        return jsonify({"error": "Both 'code' and 'name' are required"}), 400

    try:
        college = College.query.get(old_code)
        if not college:
            return jsonify({"error": "College not found"}), 404

        college.code = new_code
        college.name = new_name
        db.session.commit()
        return jsonify({"code": college.code, "name": college.name}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"College with code '{new_code}' already exists."}), 409
    except Exception:
        db.session.rollback()
        current_app.logger.exception("update_college failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

# ---- DELETE ----
# DELETE /colleges/<code>
@colleges_bp.route("/colleges/delete/<string:code>", methods=["DELETE"])
def delete_college(code):
    try:
        college = College.query.get(code)
        if not college:
            return jsonify({"error": "College not found"}), 404
        db.session.delete(college)
        db.session.commit()
        return "", 204
    except Exception:
        db.session.rollback()
        current_app.logger.exception("delete_college failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500