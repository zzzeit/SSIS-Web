from extensions import get_db_connection
import psycopg2
from psycopg2.extras import RealDictCursor
from math import ceil

def list_programs(attribute, page, ascending, value):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        sort_map = {'code': 'code', 'name': 'name', 'college': 'college'}
        sort_col = sort_map.get(attribute.lower(), 'code')
        order = "ASC" if ascending == 1 else "DESC"
        per_page = 14
        offset = (page - 1) * per_page

        query = "SELECT code, name, college FROM program"
        count_query = "SELECT COUNT(*) FROM program"
        where_clause = ""
        params = []

        if value:
            where_clause = f" WHERE {sort_col} ILIKE %s"
            params.append(f"%{value}%")

        cur.execute(count_query + where_clause, tuple(params))
        total = cur.fetchone()[0]

        full_query = f"{query}{where_clause} ORDER BY {sort_col} {order} LIMIT %s OFFSET %s"
        params.extend([per_page, offset])
        cur.execute(full_query, tuple(params))
        items = cur.fetchall()

        total_pages = ceil(total / per_page) if total > 0 else 0
        result = [list(item) for item in items]
        return result, total_pages
    finally:
        cur.close()
        conn.close()

def get_program(code):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT code, name, college FROM program WHERE code = %s", (code,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

def create_program(code, name, college):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Check if college exists
        cur.execute("SELECT 1 FROM college WHERE code = %s", (college,))
        if not cur.fetchone():
            return None, "college_not_found"
        cur.execute("""
            INSERT INTO program (code, name, college)
            VALUES (%s, %s, %s)
            RETURNING code, name, college
        """, (code, name, college))
        new_program = cur.fetchone()
        conn.commit()
        return new_program, None
    except psycopg2.IntegrityError:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def update_program(old_code, new_code, new_name, new_college):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT 1 FROM program WHERE code = %s", (old_code,))
        if not cur.fetchone():
            return None, "program_not_found"
        cur.execute("SELECT 1 FROM college WHERE code = %s", (new_college,))
        if not cur.fetchone():
            return None, "college_not_found"
        cur.execute("""
            UPDATE program
            SET code = %s, name = %s, college = %s
            WHERE code = %s
            RETURNING code, name, college
        """, (new_code, new_name, new_college, old_code))
        updated_program = cur.fetchone()
        conn.commit()
        return updated_program, None
    except psycopg2.IntegrityError:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def delete_program(code):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM program WHERE code = %s RETURNING code", (code,))
        deleted = cur.fetchone()
        conn.commit()
        return deleted
    finally:
        cur.close()
        conn.close()