from extensions import get_db_connection
import psycopg2
from psycopg2.extras import RealDictCursor
from math import ceil

def list_colleges(attribute, page, ascending, value):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        sort_map = {'code': 'code', 'name': 'name'}
        sort_col = sort_map.get(attribute.lower(), 'code')
        order = "ASC" if ascending == 1 else "DESC"
        per_page = 14
        offset = (page - 1) * per_page

        query = "SELECT code, name FROM college"
        count_query = "SELECT COUNT(*) FROM college"
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

def get_college(code):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT code, name FROM college WHERE code = %s", (code,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

def create_college(code, name):
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
        return new_college
    except psycopg2.IntegrityError:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def update_college(old_code, new_code, new_name):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT 1 FROM college WHERE code = %s", (old_code,))
        if not cur.fetchone():
            return None
        cur.execute("""
            UPDATE college
            SET code = %s, name = %s
            WHERE code = %s
            RETURNING code, name
        """, (new_code, new_name, old_code))
        updated_college = cur.fetchone()
        conn.commit()
        return updated_college
    except psycopg2.IntegrityError:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def delete_college(code):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM college WHERE code = %s RETURNING code", (code,))
        deleted = cur.fetchone()
        conn.commit()
        return deleted
    finally:
        cur.close()
        conn.close()