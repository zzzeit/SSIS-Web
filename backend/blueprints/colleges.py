from flask import Blueprint, request, jsonify, current_app, url_for, send_from_directory
from math import ceil
from extensions import get_db_connection
import psycopg2
from psycopg2.extras import RealDictCursor

colleges_bp = Blueprint('colleges', __name__)

@colleges_bp.route("/table/colleges", methods=["GET"])
def serve_college_page():
    return send_from_directory(current_app.static_folder, ".next/server/app/table/colleges.html")


# ---- LIST / SEARCH ----
# GET /colleges?attribute=code&page=1&ascending=1
@colleges_bp.route("/colleges", methods=["GET"])
def list_colleges():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        attribute = request.args.get("attribute", "code")
        page = int(request.args.get("page", 1))
        ascending = int(request.args.get("ascending", 1))

        sort_map = {
            'code': 'code',
            'name': 'name'
        }
        sort_col = sort_map.get(attribute.lower(), 'code')
        order = "ASC" if ascending == 1 else "DESC"
        per_page = 14
        offset = (page - 1) * per_page

        query = "SELECT code, name FROM college"
        count_query = "SELECT COUNT(*) FROM college"
        where_clause = ""
        params = []

        # optional search value
        value = request.args.get("value")
        if value:
            where_clause = f" WHERE {sort_col} ILIKE %s"
            params.append(f"%{value}%")

        # Get total count
        cur.execute(count_query + where_clause, tuple(params))
        total = cur.fetchone()[0]

        # Get items
        full_query = f"{query}{where_clause} ORDER BY {sort_col} {order} LIMIT %s OFFSET %s"
        params.extend([per_page, offset])
        
        cur.execute(full_query, tuple(params))
        items = cur.fetchall()

        total_pages = ceil(total / per_page) if total > 0 else 0
        result = [list(item) for item in items]
        return jsonify([result, total_pages]), 200

    except Exception:
        current_app.logger.exception("list_colleges failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()

# ---- GET single ----
# GET /colleges/<code>
@colleges_bp.route("/colleges/<string:code>", methods=["GET"])
def get_college(code):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT code, name FROM college WHERE code = %s", (code,))
        college = cur.fetchone()
        if not college:
            return jsonify({"error": "College not found"}), 404
        return jsonify(college), 200
    except Exception:
        current_app.logger.exception("get_college failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()

# ---- CREATE ----
# POST /colleges  body: { "code": "...", "name": "..." }
@colleges_bp.route("/colleges", methods=["POST"])
def create_college():
    data = request.get_json(silent=True) or {}
    code = data.get("code")
    name = data.get("name")
    if not code or not name:
        return jsonify({"error": "Both 'code' and 'name' are required"}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
            INSERT INTO college (code, name)
            VALUES (%s, %s)
            RETURNING code, name
        """, (code, name))
        
        new_college = cur.fetchone()
        conn.commit()
        
        # Return 201 with Location header for the new resource
        location = url_for(".get_college", code=new_college['code'], _external=False)
        return jsonify(new_college), 201, {"Location": location}
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"error": f"College with code '{code}' already exists."}), 409
    except Exception:
        conn.rollback()
        current_app.logger.exception("create_college failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()

# ---- UPDATE ----
# PUT /colleges/<old_code>  body: { "code": "...", "name": "..." }
@colleges_bp.route("/colleges/edit/<string:old_code>", methods=["PUT"])
def update_college(old_code):
    data = request.get_json(silent=True) or {}
    new_code = data.get("code")
    new_name = data.get("name")
    if not new_code or not new_name:
        return jsonify({"error": "Both 'code' and 'name' are required"}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Check if college exists
        cur.execute("SELECT 1 FROM college WHERE code = %s", (old_code,))
        if not cur.fetchone():
            return jsonify({"error": "College not found"}), 404

        cur.execute("""
            UPDATE college
            SET code = %s, name = %s
            WHERE code = %s
            RETURNING code, name
        """, (new_code, new_name, old_code))
        
        updated_college = cur.fetchone()
        conn.commit()
        return jsonify(updated_college), 200
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"error": f"College with code '{new_code}' already exists."}), 409
    except Exception:
        conn.rollback()
        current_app.logger.exception("update_college failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()

# ---- DELETE ----
# DELETE /colleges/<code>
@colleges_bp.route("/colleges/delete/<string:code>", methods=["DELETE"])
def delete_college(code):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM college WHERE code = %s RETURNING code", (code,))
        if not cur.fetchone():
            return jsonify({"error": "College not found"}), 404
        conn.commit()
        return "", 204
    except Exception:
        conn.rollback()
        current_app.logger.exception("delete_college failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()