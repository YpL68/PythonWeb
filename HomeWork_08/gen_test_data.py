import sqlite3
from datetime import date, timedelta
from random import randint

import faker

from connection import create_connection

NUM_DISC = 5
NUM_GRADES = 5
NUM_GROUP = 3
NUM_STD_IN_GROUP = 10

STD_GROUPS = [("1 група",), ("2 група",), ("3 група",)]
GRADES = [("кол", 1), ("незадовільно", 2), ("задовільно", 3), ("добре", 4), ("відмінно", 5)]
TEACHERS = [("Прокопенко Іван Васильович",), ("Зеленський Олег Володимирович",),
            ("Ющенко Дмитро Олегович",), ("Тимошенко Юлія Володимирівна",), ("Литвин Микола Сергійович",)]
DISCIPLINES = [("Математичний аналіз", 1), ("Радіоелектронна боротьба", 2),
               ("Теорія електричних ланцюгів та сигналів", 3), ("Лінійна алгебра", 4), ("Мова программування PL/I", 5)]


def delete_from_table(conn: sqlite3.Connection, table_name: str):
    conn.execute(f"DELETE FROM {table_name}")
    conn.execute(f"UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = '{table_name}'")


def gen_students():
    fake_data = faker.Faker('uk_UA')

    for grp_id in range(1, len(STD_GROUPS) + 1):
        for _ in range(NUM_STD_IN_GROUP):
            yield (fake_data.name(), grp_id)


def gen_grade_list():
    date_start = date(2022, 5, 1)
    date_end = date(2022, 8, 31)
    def gen_dates(start_date: date, end_date: date):
        current_date = start_date
        while current_date <= end_date:
            if current_date.isoweekday() < 6:
                yield current_date
            current_date += timedelta(1)

    for date_ in gen_dates(date_start, date_end):
        dsc_id = randint(1, len(DISCIPLINES))
        grd_id = randint(1, len(GRADES))

        num_std = NUM_STD_IN_GROUP * len(STD_GROUPS)
        for std_id in [randint(1, num_std) for _ in range(3)]:
            yield (grd_id, dsc_id, std_id, date_)


def generate_test_data():
    with create_connection() as conn:
        if conn is not None:
            try:
                cur = conn.cursor()

                delete_from_table(conn, "std_groups")
                cur.executemany("INSERT INTO std_groups (grp_name) VALUES(?)", STD_GROUPS)

                delete_from_table(conn, "grades")
                cur.executemany("INSERT INTO grades (grd_name, grd_value) VALUES(?, ?)", GRADES)

                delete_from_table(conn, "teachers")
                cur.executemany("INSERT INTO teachers (tch_name) VALUES(?)", TEACHERS)

                delete_from_table(conn, "disciplines")
                cur.executemany("INSERT INTO disciplines (dsc_name, dsc_tch_id) VALUES(?, ?)", DISCIPLINES)

                delete_from_table(conn, "students")
                cur.executemany("INSERT INTO students (std_full_name, std_grp_id) VALUES(?, ?)", gen_students())

                delete_from_table(conn, "grade_list")
                sql_insert = """
                    INSERT INTO grade_list (
                        gls_grd_id, 
                        gls_dsc_id, 
                        gls_std_id, 
                        gls_date_of) 
                    VALUES(?, ?, ?, ?)"""
                cur.executemany(sql_insert, gen_grade_list())

                cur.close()
            except sqlite3.Error as err:
                if conn.in_transaction:
                    conn.rollback()
                print(err)
            finally:
                if conn.in_transaction:
                    conn.commit()


if __name__ == '__main__':
    generate_test_data()