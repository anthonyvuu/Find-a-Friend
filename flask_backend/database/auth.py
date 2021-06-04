from werkzeug.security import generate_password_hash,  check_password_hash
import sqlite3
from sqlite3 import Error


def get_id_by_email(conn, email):
    cur = conn.cursor()
    try:
        sql = ("SELECT id FROM users WHERE email = ?")
        cur.execute(sql, (email.lower(),))
        for row in cur:
            (id, ) = row
            return {
                "id": id
            }
        else:
            
            return {
                "ok": "false",
                "message": "Bruker for den emailen finnes ikke"
            }
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

def add_user(conn, email, password):

    cur = conn.cursor()

    hash = generate_password_hash(password)

    try:
        sql = ("INSERT INTO users (email, passwordhash) VALUES (?,?)")
        cur.execute(sql, (email.lower(), hash))
        conn.commit()
    except sqlite3.Error as err:
        response_object_error = {
            'ok': 'false',
            'message': 'Registrering feilet, email allerede i bruk'
        }
        return response_object_error
    else:
        return {
            "id": cur.lastrowid
        }
    finally:
        cur.close()

def get_hash_for_login(conn, email):
    """Get user details from id."""
    cur = conn.cursor()
    try:
        sql = ("SELECT passwordhash FROM users WHERE email=?")
        cur.execute(sql, (email.lower(),))
        for row in cur:
            (passhash,) = row
            return passhash
        else:
            return None
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()