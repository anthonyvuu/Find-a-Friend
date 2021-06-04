import random
from sqlite3 import Error
import sqlite3

def delete_hobbies_friendId(conn, friendId):

    cur = conn.cursor()

    sql = ''' DELETE FROM friend_hobby WHERE friendId = ?
            '''

    cur.execute(sql, (friendId))
    conn.commit()
    cur.close()

def add_hobby(conn, hobby):

    cur = conn.cursor()

    try:
        sql = ''' INSERT INTO hobbies(hobby)
               VALUES(?) '''
        cur.execute(sql, (hobby.lower(), ))
        conn.commit()
        return "ok"
    except Error as e:
        errorMsg = {
            "ok": "false",
            'message': 'Hobby ' + hobby + ' eksisterer allerede'
        }
        return errorMsg

def get_hobbies_for_friendId(conn, friendId):
    cur = conn.cursor()

    try:
        sql = ("SELECT hobby, backgroundColor FROM friend_hobby WHERE friendId = ?")
        cur.execute(sql, (friendId,))
        hobbies = []
        for row in cur:
            (hobby, backgroundColor) = row
            hobbies.append({
                "hobby": hobby,
                "backgroundColor": backgroundColor
            })
        return hobbies
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

def get_hobbies(conn):

    cur = conn.cursor()

    sql = "SELECT hobby FROM hobbies"
    cur.execute(sql, )

    hobbies = []

    for row in cur:
        (hobby,) = row
        hobbies.append(hobby)
    return hobbies


# når en hobby første gang blir brukt så får den en tilfedig hex fargekode. 
def add_friend_hobby(conn, friendId, hobby):
    cur = conn.cursor()
    sql = ''' INSERT INTO friend_hobby(friendId, hobby, backgroundColor)
              VALUES(?,?,?) '''

    randomcolor = f'{"#%06x" % random.randint(0, 0xFFFFFF)}'

    exists = check_if_hobby_have_color(conn, hobby)

    if exists == None:
        cur.execute(sql, (friendId, hobby, randomcolor))
        conn.commit()
    else:
        cur.execute(sql, (friendId, hobby, exists))
        conn.commit()

# funksjon for å sørge for at venner som har samme hobby ender opp med samme farge på frontenden.  
def check_if_hobby_have_color(conn, hobby):

    sql = ("SELECT backgroundColor FROM friend_hobby WHERE hobby = ?")

    cur = conn.cursor()
    cur.execute(sql, (hobby,))

    result = cur.fetchone()

    if result == None:
        return None
    else:
        return result[0]