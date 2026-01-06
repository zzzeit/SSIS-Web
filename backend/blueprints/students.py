from flask import Blueprint, jsonify, current_app, request, send_from_directory, url_for
from math import ceil
from extensions import get_db_connection
import psycopg2
from psycopg2.extras import RealDictCursor

students_bp = Blueprint('students', __name__)

@students_bp.route("/table/students", methods=["GET"])
def serve_student_page():
    return send_from_directory(current_app.static_folder, ".next/server/app/table/students.html")

# ---- LIST / SEARCH ----
# GET /students?attribute=id_num&page=1&ascending=1&value=...
@students_bp.route("/students", methods=["GET"])
def list_students():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        attribute = request.args.get("attribute", "id_num")
        page = int(request.args.get("page", 1))
        ascending = int(request.args.get("ascending", 1))

        sort_map = {
            'id_num': 'id_num',
            'fname': 'fname',
            'lname': 'lname',
            'program': 'program_code',
            'year': 'year',
            'sex': 'sex'
        }
        sort_col = sort_map.get(attribute.lower(), 'id_num')
        order = "ASC" if ascending == 1 else "DESC"
        per_page = 14
        offset = (page - 1) * per_page

        query = "SELECT id_num, fname, lname, program_code, year, sex FROM student"
        count_query = "SELECT COUNT(*) FROM student"
        where_clauses = []
        params = []

        # Main search value
        value = request.args.get("value")
        if value:
            if attribute.lower() == 'year':
                try:
                    year_val = int(value)
                    where_clauses.append("year = %s")
                    params.append(year_val)
                except ValueError:
                    return jsonify({"error": "Invalid year value"}), 400
            else:
                where_clauses.append(f"{sort_col} ILIKE %s")
                params.append(f"%{value}%")

        # Additional filters
        filter_map = {
            "Program": "program_code",
            "Year": "year",
            "Sex": "sex"
        }
        for filter_key, db_col in filter_map.items():
            filter_val = request.args.get(filter_key)
            if filter_val:
                if db_col == "year":
                    try:
                        filter_val = int(filter_val)
                        where_clauses.append(f"{db_col} = %s")
                        params.append(filter_val)
                    except ValueError:
                        return jsonify({"error": "Invalid year filter value"}), 400
                else:
                    where_clauses.append(f"{db_col} = %s")
                    params.append(filter_val)

        where_clause = ""
        if where_clauses:
            where_clause = " WHERE " + " AND ".join(where_clauses)

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
        current_app.logger.exception("list_students failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()


# ---- GET single ----
# GET /students/<id_num>
@students_bp.route("/students/<string:id_num>", methods=["GET"])
def get_student(id_num):
    id_num = id_num.replace("-", "")
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT * FROM student WHERE id_num = %s", (id_num,))
        student = cur.fetchone()
        if not student:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(student), 200
    except Exception:
        current_app.logger.exception("get_student failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()


# ---- CREATE ----
# POST /students  body: { "id_num": "...", "fname": "...", "lname": "...", "program_code": "...", "year": 1, "sex": "M" }
@students_bp.route("/students", methods=["POST"])
def create_student():
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

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Check if program exists
        cur.execute("SELECT 1 FROM program WHERE code = %s", (program_code,))
        if not cur.fetchone():
            return jsonify({"error": f"Program with code '{program_code}' does not exist."}), 400

        cur.execute("""
            INSERT INTO student (id_num, fname, lname, program_code, year, sex)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_num, fname, lname, program_code, year, sex
        """, (id_num, fname, lname, program_code, year, sex))
        
        new_student = cur.fetchone()
        conn.commit()
        
        location = url_for('.get_student', id_num=new_student['id_num'], _external=False)
        return jsonify(new_student), 201, {"Location": location}

    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"error": f"Student with ID '{id_num}' already exists."}), 409
    except Exception:
        conn.rollback()
        current_app.logger.exception("create_student failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()


# ---- UPDATE ----
# PUT /students/<old_id_num>  body: { "id_num": "...", "fname": "...", "lname": "...", "program_code": "...", "year": 1, "sex": "M" }
@students_bp.route("/students/edit/<string:old_id_num>", methods=["PUT"])
def update_student(old_id_num):
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
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Check if student exists
        cur.execute("SELECT 1 FROM student WHERE id_num = %s", (old_id_num,))
        if not cur.fetchone():
            return jsonify({"error": "Student not found"}), 404

        # Check if program exists
        cur.execute("SELECT 1 FROM program WHERE code = %s", (program_code,))
        if not cur.fetchone():
            return jsonify({"error": f"Program with code '{program_code}' does not exist."}), 400

        cur.execute("""
            UPDATE student
            SET id_num = %s, fname = %s, lname = %s, program_code = %s, year = %s, sex = %s
            WHERE id_num = %s
            RETURNING id_num, fname, lname, program_code, year, sex
        """, (new_id_num, fname, lname, program_code, year, sex, old_id_num))
        
        updated_student = cur.fetchone()
        conn.commit()
        return jsonify(updated_student), 200

    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"error": f"A student with ID '{new_id_num}' already exists."}), 409
    except Exception:
        conn.rollback()
        current_app.logger.exception("update_student failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()


# ---- DELETE ----
# DELETE /students/<id_num>
@students_bp.route("/students/delete/<string:id_num>", methods=["DELETE"])
def delete_student(id_num):
    id_num = id_num.replace("-", "")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM student WHERE id_num = %s RETURNING id_num", (id_num,))
        if not cur.fetchone():
            return jsonify({"error": "Student not found"}), 404
        conn.commit()
        return "", 204
    except Exception:
        conn.rollback()
        current_app.logger.exception("delete_student failed")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500
    finally:
        cur.close()
        conn.close()