from sqlite3 import Error
import sqlite3

def send_friend_request(conn, friendId, requesttoId):
    cur = conn.cursor()

    result = check_if_request_exists(conn, friendId, requesttoId)

    if result == None:
        sql = ''' INSERT INTO friend_request(friendId, requesttoId)
            VALUES(?,?)
            '''
        cur.execute(sql, (friendId, requesttoId))
        conn.commit()
    else:
        return result


def delete_friend_request(conn, friendId, requesttoId):

    cur = conn.cursor()

    sql = "DELETE FROM friend_request WHERE friendId = ? AND requesttoId = ?"

    cur.execute(sql, (friendId, requesttoId))
    conn.commit()
    cur.close()


def get_requests_for_friendId(conn, friendId):
    sql = "SELECT friendId FROM friend_request WHERE requesttoId = ?"

    cur = conn.cursor()

    try:
        cur.execute(sql, (friendId,))
        requests = []
        for row in cur:
            (friendId, ) = row
            requests.append(friendId)
        return requests
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return requests
    finally:
        cur.close()


def check_if_request_exists(conn, friendId, requesttoId):

    sql = "SELECT * FROM friend_request WHERE friendId = ? AND requesttoId = ?"
    cur = conn.cursor()
    cur.execute(sql, (friendId, requesttoId, ))

    result = cur.fetchone()

    if result == None:
        return None
    else:
        response_object_error = {
            "ok": "false",
            "message": "Friend request already made, still pending"
        }
        return response_object_error