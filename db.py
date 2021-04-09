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

def friends():
    query = """
    SELECT * FROM friends_list
        """
    g.cursor.execute(query)
    return g.cursor.fetchall()

def find_member(memberEmail):
    query = """
    SELECT email, first_name, last_name, password
    FROM team.member
    WHERE email = %(emailParam)s
    """
    g.cursor.execute(query, {'emailParam': memberEmail})
    return g.cursor.fetchone()


def create_member(email, first_name, last_name, password):
    query = '''
    INSERT INTO team.member (email, first_name, last_name, password)
    VALUES (%(email)s, %(first)s, %(last)s, %(pass)s)
    '''

    g.cursor.execute(query, {'email': email, 'first': first_name, 'last': last_name, 'pass': password})
    g.connection.commit()
    return g.cursor.rowcount


def passw_check(memberEmail):
    query = """
    SELECT password
    FROM team.member
    WHERE email = %(emailParam)s
    """
    g.cursor.execute(query, {'emailParam': memberEmail})
    return g.cursor.fetchone()

def update(memberEmail):
    query = """
    SELECT password
    FROM team.member
    WHERE email = %(emailParam)s
    """
    g.cursor.execute(query, {'emailParam': memberEmail})
    return g.cursor.fetchone()