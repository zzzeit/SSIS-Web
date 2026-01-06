from extensions import get_db_connection
import psycopg2
from psycopg2.extras import RealDictCursor
from math import ceil

def list_students(attribute, page, ascending, value, filters):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
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
        if value:
            if attribute.lower() == 'year':
                try:
                    year_val = int(value)
                    where_clauses.append("year = %s")
                    params.append(year_val)
                except ValueError:
                    return None, "invalid_year"
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
            filter_val = filters.get(filter_key)
            if filter_val:
                if db_col == "year":
                    try:
                        filter_val = int(filter_val)
                        where_clauses.append(f"{db_col} = %s")
                        params.append(filter_val)
                    except ValueError:
                        return None, "invalid_year_filter"
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
        return (result, total_pages), None
    finally:
        cur.close()
        conn.close()

def get_student(id_num):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT * FROM student WHERE id_num = %s", (id_num,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

def create_student(id_num, fname, lname, program_code, year, sex):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Check if program exists
        cur.execute("SELECT 1 FROM program WHERE code = %s", (program_code,))
        if not cur.fetchone():
            return None, "program_not_found"
        cur.execute("""
            INSERT INTO student (id_num, fname, lname, program_code, year, sex)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_num, fname, lname, program_code, year, sex
        """, (id_num, fname, lname, program_code, year, sex))
        new_student = cur.fetchone()
        conn.commit()
        return new_student, None
    except psycopg2.IntegrityError:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def update_student(old_id_num, new_id_num, fname, lname, program_code, year, sex):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Check if student exists
        cur.execute("SELECT 1 FROM student WHERE id_num = %s", (old_id_num,))
        if not cur.fetchone():
            return None, "student_not_found"
        # Check if program exists
        cur.execute("SELECT 1 FROM program WHERE code = %s", (program_code,))
        if not cur.fetchone():
            return None, "program_not_found"
        cur.execute("""
            UPDATE student
            SET id_num = %s, fname = %s, lname = %s, program_code = %s, year = %s, sex = %s
            WHERE id_num = %s
            RETURNING id_num, fname, lname, program_code, year, sex
        """, (new_id_num, fname, lname, program_code, year, sex, old_id_num))
        updated_student = cur.fetchone()
        conn.commit()
        return updated_student, None
    except psycopg2.IntegrityError:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def delete_student(id_num):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM student WHERE id_num = %s RETURNING id_num", (id_num,))
        deleted = cur.fetchone()
        conn.commit()
        return deleted
    finally:
        cur.close()
        conn.close()