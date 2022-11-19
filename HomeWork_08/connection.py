from contextlib import contextmanager
from sqlite3 import Error, connect


@contextmanager
def create_connection():
    conn = None
    try:
        conn = connect("hw_08.db")
        yield conn
    except Error as err:
        print(err)
    finally:
        conn.close()
