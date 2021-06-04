from sqlite3 import Error
import sqlite3

def get_image_for_friendId(conn, friendId):

    cur = conn.cursor()

    sql = "SELECT id, data FROM gallery_images WHERE friendId = ?"

    try:
        cur.execute(sql, (friendId,))
        images = []
        for row in cur:
            (id, data) = row
            images.append({
                "id": id,
                "data": data
            })
        return images
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    finally:
        cur.close()


def add_image(conn, friendId, filedata):
    cur = conn.cursor()

    sql = ''' INSERT INTO gallery_images(friendId, data)
            VALUES(?,?)
            '''

    cur.execute(sql, (friendId, filedata))
    conn.commit()
    cur.close()

def delete_image(conn, imageId):
    cur = conn.cursor()

    sql = ''' DELETE FROM gallery_images WHERE id = ? '''
    cur.execute(sql, (imageId))
    conn.commit()
    cur.close()