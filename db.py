from flask import g
import psycopg2
import psycopg2.extras

data_source_name = "dbname=pika user=rwhite password=rwhite host=roller.cse.taylor.edu"


def open_db_connection():
    g.connection = psycopg2.connect(data_source_name)
    g.cursor = g.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def close_db_connection():
    g.cursor.close()
    g.connection.close()


def find_member(memberEmail):
    query = """
    SELECT m.email, m.first_name, m.last_name, p.file_path
    FROM member AS m
       LEFT OUTER JOIN photo AS p ON m.email = p.member_email 
    WHERE email = %(emailParam)s
    """
    g.cursor.execute(query, {'emailParam': memberEmail})
    return g.cursor.fetchone()


def create_member(email, first_name, last_name, password):
    query = '''
    INSERT INTO member (email, first_name, last_name, password)
    VALUES (%(email)s, %(first)s, %(last)s, %(pass)s)
    '''

    g.cursor.execute(query, {'email': email, 'first': first_name, 'last': last_name, 'pass': password})
    g.connection.commit()
    return g.cursor.rowcount
