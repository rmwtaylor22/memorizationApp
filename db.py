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
    SELECT email, first_name, last_name, password, member_id
    FROM public.member
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


def matchPassword(em, pw):
    query = """
        SELECT email, password
        FROM member
        WHERE email = %(emParam)s and password = %(pwParam)s
    """
    g.cursor.execute(query, {'emParam': em, 'pwParam': pw})
    return g.cursor.fetchone()


def getVerses(member_id):
    query = """
    SELECT *
    FROM pika.public.member
    INNER JOIN pika.public.member_verse as mv on member.member_id = mv.member_id
    INNER JOIN bible b on b.id = mv.bible_id
    WHERE member.member_id = %(mid)s
    ORDER BY book
    """
    g.cursor.execute(query, {'mid': member_id})
    return g.cursor.fetchall()


def add_verse(member_id, bible_id):
    query = '''
    INSERT INTO member_verse (member_id, bible_id, amount)
    VALUES (%(mid)s, %(bid)s, %(amount)s)
    '''

    g.cursor.execute(query, {'mid': member_id, 'bid': bible_id, 'amount': 1})
    g.connection.commit()
    return g.cursor.rowcount


def find_verse_id(bk, ch, vs):
    query = """
        SELECT id
        FROM bible
        WHERE book = %(bkParam)s and chapter = %(chParam)s and verse = %(vsParam)s
        """
    g.cursor.execute(query, {'bkParam': bk, 'chParam': ch, 'vsParam': vs})
    return g.cursor.fetchone()


def find_verse(bk, chtr, vs):
    query = """
        SELECT text
        FROM bible
        WHERE book = %(bkParam)s and chapter = %(chParam)s and verse = %(vsParam)s
        """
    g.cursor.execute(query, {'bkParam': bk, 'chParam': chtr, 'vsParam': vs})
    return g.cursor.fetchone()


def find_member_verse(member_id, bible_id):
    query = """
    SELECT member_id, bible_id
    FROM member_verse
    WHERE member_id = %(mid)s and bible_id = %(bid)s 
    """
    g.cursor.execute(query, {'mid': member_id, 'bid': bible_id})
    return g.cursor.fetchone()