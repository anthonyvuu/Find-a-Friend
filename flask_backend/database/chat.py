from sqlite3 import Error
import sqlite3

def add_chatmessage(conn, channel, isImage, isFile, firstName, message, fileName, date):

    cur = conn.cursor()

    sql = ''' INSERT INTO chatchannel(channel, isImage, isFile, firstName, message, fileName, date)
            VALUES(?,?,?,?,?,?,?)
            '''
    cur.execute(sql, (channel, isImage, isFile, firstName, message, fileName, date))
    conn.commit()

def get_chatmessage_for_channel(conn, channel):

    cur = conn.cursor()

    sql = "SELECT message, fileName, isImage, isFile, firstName, date FROM chatchannel WHERE channel = ?"

    try:
        cur.execute(sql, (channel,))
        messages = []
        for row in cur:
            (message, fileName, isImage, isFile, firstName, date) = row
            messages.append({
                "message": message,
                "fileName": fileName,
                "isImage": isImage,
                "isFile": isFile,
                "firstName": firstName,
                "date": date
            })
        return messages
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    finally:
        cur.close()