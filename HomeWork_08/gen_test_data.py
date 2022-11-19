import sqlite3
from datetime import date, timedelta
from random import randint, choice

import faker

from connection import create_connection

NUM_DISC = 5
NUM_GRADES = 5
NUM_GROUP = 3
NUM_STD_IN_GROUP = 10


def gen_students():
    fake_data = faker.Faker('uk_UA')

    for grp_id in range(1, NUM_GROUP + 1):
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
        dsc_id = randint(1, NUM_DISC)
        grd_id = randint(1, NUM_GRADES)

        num_std = NUM_STD_IN_GROUP * NUM_GROUP
        for std_id in [randint(1, num_std) for _ in range(3)]:
            yield (grd_id, dsc_id,std_id, date_)


def generate_test_data():
    with create_connection() as conn:
        if conn is not None:
            try:
                cur = conn.cursor()
                sql_std_delete = "DELETE FROM students"
                sql_seq_update = "UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'students'"
                sql_std_insert = "INSERT INTO students (std_full_name, std_grp_id) VALUES(?, ?)"

                cur.execute(sql_std_delete)
                cur.execute(sql_seq_update)
                cur.executemany(sql_std_insert, gen_students())

                sql_grd_delete = "DELETE FROM grade_list"
                sql_seq_update = "UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'grade_list'"
                sql_grd_insert = """
                    INSERT INTO grade_list (
                        gls_grd_id, 
                        gls_dsc_id, 
                        gls_std_id, 
                        gls_date_of) 
                    VALUES(?, ?, ?, ?)"""

                cur.execute(sql_grd_delete)
                cur.execute(sql_seq_update)
                cur.executemany(sql_grd_insert, gen_grade_list())

                cur.close()
            except sqlite3.Error as err:
                if conn.in_transaction:
                    conn.rollback()
                print(err)
            finally:
                if conn.in_transaction:
                    conn.commit()



        #     SELECT
        #         CAST(grd_id as TEXT) 'Id',
        #         grd_name 'Оцінка',
        #         current_date 'Дата'
        #     FROM grades
        #     ORDER BY grd_id
        # """
        #
        # result = list(cur.execute(sql_get_groups_id).fetchall())
        # headers = tuple(item[0] for item in cur.description)
        # result.insert(0, headers)
        # cols_align = ("L", "R", "R")
        #
        # print(easy_table(result, cols_align))
        #
        # cur.close()
        #
        # if conn.in_transaction:
        #     conn.commit()


if __name__ == '__main__':
    generate_test_data()