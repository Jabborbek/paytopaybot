import sqlite3
import hashlib
from func.create_db import SQLither
from loader import db



async def get_hash_code(path_url,file_name,user_id):
    conn = sqlite3.connect(f'{path_url}/{file_name}',check_same_thread=False)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM kaltlar")
    result = cur.fetchall()
    conn.close()
    new_db_file = path_url + '/' + str(user_id) + '_' + file_name
    try:
        SQLither(f"{new_db_file}")
        await db.update_path_url_send_file(path_url_send_file=new_db_file,telegram_id=user_id)
        conn1 = sqlite3.connect(f"{new_db_file}")
        cursor = conn1.cursor()
        table = """CREATE TABLE kaltlar(filename VARCHAR(255), hashqiymat VARCHAR(255),kaltqiymat VARCHAR(255))"""
        cursor.execute(table)

        for i in range(len(result)):
            string = result[i][1] + result[i][2] + str(991430269)
            encoded = string.encode()
            key = hashlib.sha256(encoded)
            kalit = key.hexdigest()
            cursor.execute("""INSERT INTO kaltlar(filename, hashqiymat, kaltqiymat) VALUES(?,?,?)""",
                           (result[i][1], result[i][2], kalit))
            conn1.commit()
        conn1.close()


    except Exception :
        print("Already table exits")


