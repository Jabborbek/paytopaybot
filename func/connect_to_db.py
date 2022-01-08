import sqlite3
from func.create_db import SQLither


async def connect_to_db_func(path_url,file_name):

    conn = sqlite3.connect(f'{path_url}/{file_name}',check_same_thread=False)
    cur = conn.cursor()
    cur.execute(f"SELECT count(filename) FROM kaltlar")
    result = cur.fetchone()
    conn.close()
    return result[0]
