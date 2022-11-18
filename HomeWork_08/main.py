import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect("hw_08.db") as con:
        if not con.isolation_level:
            print("NONE")

        cur = con.cursor()
        cur.execute(sql)
        if con.in_transaction:
            print("in transaction")
            con.commit()
        return cur.fetchall()


sql1 = """
    SELECT *
    FROM grades AS g
"""

print(execute_query(sql1))
