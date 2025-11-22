# backend/blueprints/colleges.py
from flask import Blueprint, jsonify, current_app
from math import ceil
from extensions import db
from models import College
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc, desc

colleges_bp = Blueprint('colleges', __name__)

@colleges_bp.route("/get/colleges/<string:attribute>/<int:page>/<int:ascending>")
def getColleges(attribute, page, ascending):
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
        current_app.logger.exception("An error occurred in getColleges")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


@colleges_bp.route("/insert/college/<string:code>/<string:name>")
def insertCollege(code, name):
    try:
        college = College(code=code, name=name)
        db.session.add(college)
        db.session.commit()
        return jsonify([college.code, college.name]), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": f"College with code '{code}' already exists."}), 409
    except Exception:
        db.session.rollback()
        current_app.logger.exception("An error occurred in insertCollege")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


@colleges_bp.route("/delete/college/<string:code>")
def deleteCollege(code):
    try:
        college = College.query.get(code)
        if college is None:
            return jsonify({"error": f"College with code '{code}' not found."}), 404

        db.session.delete(college)
        db.session.commit()
        return jsonify({"message": f"College with code '{code}' deleted successfully."}), 200

    except Exception:
        db.session.rollback()
        current_app.logger.exception("An error occurred in deleteCollege")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


@colleges_bp.route("/edit/college/<string:oldCode>/<string:newCode>/<string:newName>")
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
    except Exception:
        db.session.rollback()
        current_app.logger.exception("An error occurred in editCollege")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500


@colleges_bp.route("/search/colleges/<string:attribute>/<string:value>/<int:page>/<int:ascending>")
def searchCollege(attribute, value, page, ascending):
    try:
        search_pattern = f"%{value}%"

        if attribute.lower() == 'name':
            base_query = College.query.filter(College.name.ilike(search_pattern))
            att = College.name
        elif attribute.lower() == 'code':
            base_query = College.query.filter(College.code.ilike(search_pattern))
            att = College.code
        else:
            return jsonify({"error": f"Searching by attribute '{attribute}' is not supported."}), 400

        total_results = base_query.count()
        total_pages = ceil(total_results / 14)

        order = desc(att) if ascending == 0 else asc(att)
        paginated_results = base_query.order_by(order).offset((page - 1) * 14).limit(14).all()
        formatted_results = [[c.code, c.name] for c in paginated_results]
        return jsonify([formatted_results, total_pages]), 200

    except Exception:
        current_app.logger.exception("An error occurred in searchCollege")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500