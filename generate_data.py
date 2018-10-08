import mysql.connector
import random
import string
import functools
import time
import argparse
import sys
from tqdm import tqdm


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_timestamp = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_timestamp
        duration = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print('data insert completed in {}'.format(duration))
        return result

    return wrapper


def rand_string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@timeit
def insert_rows(rows=100000):
    i = 0
    print("preparing sql statements..")
    for i in tqdm(range(1, int(rows) + 1)):
        name = rand_string_generator(size=3) + str(i)
        address = rand_string_generator(size=6) + str(i) + name
        insert_query = "INSERT INTO random_table (rand_column_1, rand_column_2) VALUES ('{}', '{}')".format(name, address)
        db_cursor.execute(insert_query)
    db.commit()
    print("{}  - rows inserted to database".format(i))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser("Script to insert random data to Mysql database.")
    arg_parser.add_argument("host", help="database hostname/ip")
    arg_parser.add_argument("username", help="database username")
    arg_parser.add_argument("password", help="database password")
    arg_parser.add_argument("database", help="database name to generate random data")
    arg_parser.add_argument("--rows", help="count of rows to be inserted to database.")
    if len(sys.argv) < 4:
        arg_parser.print_help()
        sys.exit(1)

    arguments = arg_parser.parse_args()
    db_host = arguments.host
    db_username = arguments.username
    db_password = arguments.password
    db_name = arguments.database
    db_rows = arguments.rows
    try:
        db = mysql.connector.connect(
            host=db_host,
            user=db_username,
            passwd=db_password,
            database=db_name
        )
        db_cursor = db.cursor()
        print("connected to MySQL server..")
        db_cursor.execute(
            "CREATE TABLE IF NOT EXISTS random_table "
            "(id BIGINT AUTO_INCREMENT PRIMARY KEY, rand_column_1 VARCHAR(255), rand_column_2 VARCHAR(255))")
        db.commit()
        print("created database..")
        insert_rows(rows=db_rows)
    except mysql.connector.errors.ProgrammingError as pro_e:
        if 'Unknown database' in pro_e.msg:
            print("Error:  {}".format(pro_e))
        elif 'Access denied' in  pro_e.msg:
            print("Error:  {}".format(pro_e))
        else:
            print("unknown error occurred: ".format(pro_e.msg))
    except mysql.connector.errors.DatabaseError as conn_e:
        if 'Unknown MySQL server host' in conn_e.msg:
            print("Error:  {}".format(conn_e))
        else:
            print("unknown error occurred: check the database server".format(conn_e.msg))
