import sqlite3
from connection import create_connection

from queries import QUERY_LIST
from easy_table import easy_table


def execute_query(conn: sqlite3.Connection, num_query: int) -> list:
    cur = conn.cursor()
    result = []

    try:
        result = list(cur.execute(QUERY_LIST[num_query-1]).fetchall())
        headers = tuple(item[0] for item in cur.description)
        result.insert(0, headers)
    except sqlite3.Error as err:
        cur.close()
        if conn.in_transaction:
            conn.rollback()
        print(err)
    finally:
        cur.close()
        if conn.in_transaction:
            conn.commit()

    return result


def main():
    with create_connection() as conn:
        if conn is not None:
            while True:
                inp_str = input("Enter the query number or 'exit' to quit: ")
                try:
                    if inp_str.lower() == "exit":
                        break
                    num_query = int(inp_str)
                    if not (1 <= num_query <= 12):
                        raise ValueError
                except ValueError:
                    print("Please enter a valid query number (1 - 12).")
                else:
                    print(easy_table(execute_query(conn, num_query)))


if __name__ == '__main__':
    main()
