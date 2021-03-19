from flask import g
import psycopg2
import psycopg2.extras


data_source_name = "dbname=rwhite user=rwhite password=rwhite host=roller.cse.taylor.edu"


def open_db_connection():
    g.connection = psycopg2.connect(data_source_name)
    g.cursor = g.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def close_db_connection():
    g.cursor.close()
    g.connection.close()


def trip_report():
    query = """
        SELECT s.first_name, s.last_name,  s.class, t.destination, t.year, t.semester
        FROM student AS s
           INNER JOIN student_trip AS st ON s.id = st.student_id 
           INNER JOIN trip AS t ON st.trip_id = t.id
        """
    g.cursor.execute(query)
    return g.cursor.fetchall()