from flask import Blueprint, jsonify, current_app, request, send_from_directory, url_for
from math import ceil
from extensions import get_db_connection
import psycopg2
from psycopg2.extras import RealDictCursor

programs_bp = Blueprint('programs', __name__)

@programs_bp.route("/table/programs", methods=["GET"])
def serve_program_page():
    return send_from_directory(current_app.static_folder, ".next/server/app/table/programs.html")

# ---- LIST / SEARCH ----
# GET /programs?attribute=code&page=1&ascending=1&value=...
@programs_bp.route("/programs", methods=["GET"])
def list_programs():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        attribute = request.args.get("attribute", "code")
        page = int(request.args.get("page", 1))
        ascending = int(request.args.get("ascending", 1))

        sort_map = {
            'code': 'code',
            'name': 'name',
            'college': 'college'
        }
        sort_col = sort_map.get(attribute.lower(), 'code')
        order = "ASC" if ascending == 1 else "DESC"
        per_page = 14
        offset = (page - 1) * per_page

        query = "SELECT code, name, college FROM program"
        count_query = "SELECT COUNT(*) FROM program"
        where_clause = ""
        params = []

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
        current_app.logger.exception("list_programs failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()


# ---- GET single ----
# GET /programs/<code>
@programs_bp.route("/programs/<string:code>", methods=["GET"])
def get_program(code):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT code, name, college FROM program WHERE code = %s", (code,))
        program = cur.fetchone()
        if not program:
            return jsonify({"error": "Program not found"}), 404
        return jsonify(program), 200
    except Exception:
        current_app.logger.exception("get_program failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()


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

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Check if college exists
        cur.execute("SELECT 1 FROM college WHERE code = %s", (college,))
        if not cur.fetchone():
            return jsonify({"error": f"Cannot add program. College with code '{college}' does not exist."}), 400

        cur.execute("""
            INSERT INTO program (code, name, college)
            VALUES (%s, %s, %s)
            RETURNING code, name, college
        """, (code, name, college))
        
        new_program = cur.fetchone()
        conn.commit()
        
        location = url_for('.get_program', code=new_program['code'], _external=False)
        return jsonify(new_program), 201, {"Location": location}

    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"error": f"Program with code '{code}' already exists."}), 409
    except Exception:
        conn.rollback()
        current_app.logger.exception("create_program failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()


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

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Check if program exists
        cur.execute("SELECT 1 FROM program WHERE code = %s", (old_code,))
        if not cur.fetchone():
            return jsonify({"error": "Program not found"}), 404

        # Check if college exists
        cur.execute("SELECT 1 FROM college WHERE code = %s", (new_college,))
        if not cur.fetchone():
            return jsonify({"error": f"Cannot update program. College with code '{new_college}' does not exist."}), 400

        cur.execute("""
            UPDATE program
            SET code = %s, name = %s, college = %s
            WHERE code = %s
            RETURNING code, name, college
        """, (new_code, new_name, new_college, old_code))
        
        updated_program = cur.fetchone()
        conn.commit()
        return jsonify(updated_program), 200

    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"error": f"Program with code '{new_code}' already exists."}), 409
    except Exception:
        conn.rollback()
        current_app.logger.exception("update_program failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()


# ---- DELETE ----
# DELETE /programs/<code>
@programs_bp.route("/programs/delete/<string:code>", methods=["DELETE"])
def delete_program(code):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM program WHERE code = %s RETURNING code", (code,))
        if not cur.fetchone():
            return jsonify({"error": "Program not found"}), 404
        conn.commit()
        return "", 204
    except Exception:
        conn.rollback()
        current_app.logger.exception("delete_program failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()