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


def update(memberEmail, fn, ln, psw):
    query = """
    UPDATE team.member
    SET email = %(emailParam)s,
        first_name = %(fnParam)s,
        last_name = %(lnParam)s,
        password = %(pswParam)s
    WHERE email = %(emailParam)s
    """
    g.cursor.execute(query, {'emailParam': memberEmail, 'fnParam': fn, 'lnParam': ln, 'pswParam': psw})
    g.connection.commit()
    return g.cursor.rowcount

# Went to the following link for SQL update examples
# https://www.zentut.com/sql-tutorial/sql-update/#:~:text=%20To%20update%20data%20in%20a%20table%2C%20you,optional.%20If%20you%20omit%20the%20WHERE...%20More%20
#
# and more help from W3Schools below ...
#
# UPDATE table_name
# SET column1 = value1, column2 = value2, ...
# WHERE condition;

# https://www.w3schools.com/SQL/sql_update.asp
