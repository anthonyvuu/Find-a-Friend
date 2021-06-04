import sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash,  check_password_hash
import random
import base64


database = r"./database.db"

default_image = "data:image/jpeg;base64,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"


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                id INTEGER,
                                email TEXT NOT NULL,
                                passwordhash TEXT NOT NULL,
                                PRIMARY KEY (id),
                                UNIQUE(email)
                            );"""


sql_create_friends_table = """CREATE TABLE IF NOT EXISTS friends (
                                friendId TEXT PRIMARY KEY,
                                firstName TEXT UNIQUE,
                                lastName TEXT,
                                description TEXT,
                                image LARGEBINARY
                            );"""

sql_create_friend_request_table = """CREATE TABLE IF NOT EXISTS friend_request (
                                friendId TEXT,
                                requesttoId TEXT
                            );"""

sql_create_hobbies_table = """CREATE TABLE IF NOT EXISTS hobbies (
                                id INTEGER PRIMARY KEY,
                                hobby TEXT UNIQUE
                            );"""

sql_create_friend_hobbies_table = """CREATE TABLE IF NOT EXISTS friend_hobby (
                                friendId TEXT,
                                hobby TEXT,
                                backgroundColor TEXT
                            );"""

sql_create_isFriend_table = """CREATE TABLE IF NOT EXISTS isFriend (
                                friendId TEXT,
                                friendWith TEXT
                            );"""

sql_create_gallery_images_table = """CREATE TABLE IF NOT EXISTS gallery_images (
                                id INTEGER PRIMARY KEY,
                                friendId INTEGER,
                                data LARGEBINARY
                            );"""

sql_create_chatchannel_table = """CREATE TABLE IF NOT EXISTS chatchannel (
                                id INTEGER PRIMARY KEY,
                                channel INTEGER,
                                isImage STRING,
                                isFile STRING,
                                firstName STRING,
                                message STRING,
                                fileName TEXT,
                                date TEXT                    
                            );"""


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def setup():
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_friends_table)
        create_table(conn, sql_create_users_table)
        
        create_table(conn, sql_create_friend_hobbies_table)
        create_table(conn, sql_create_hobbies_table)
        create_table(conn, sql_create_friend_request_table)
        create_table(conn, sql_create_isFriend_table)
        create_table(conn, sql_create_gallery_images_table)
        create_table(conn, sql_create_chatchannel_table)

        add_user(conn, "test@live.no", "test123")
        add_user(conn, "tony@live.no", "tony123")
        # add_friend(conn, "1", "test1", "Vu", "Test1", None)
        # add_friend(conn, "2", "test2", "Vu", "Test2", None)

        # add_friend_hobby(conn, "1", "football")
        # add_friend_hobby(conn, "1", "gaming")
        # add_friend_hobby(conn, "1", "golf")
        # add_friend_hobby(conn, "2", "golf")
        # add_friend_hobby(conn, "2", "surf")
        # add_friend_hobby(conn, "2", "handball")

        add_hobby(conn, "football")
        add_hobby(conn, "gaming")
        add_hobby(conn, "programming")
        add_hobby(conn, "golf")
        add_hobby(conn, "handball")
        add_hobby(conn, "tennis")
        add_hobby(conn, "hiking")
        add_hobby(conn, "shopping")
        add_hobby(conn, "coffee")
        add_hobby(conn, "surf")

    conn.close()


# if __name__ == '__main__':
#     setup()