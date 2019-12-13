import sqlite3
import random
from pathlib import Path
from string import digits, ascii_uppercase


def create_database(database_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(database_path)
    conn.execute("CREATE TABLE MEMBERS ("
                 "MEMBER_ID TEXT PRIMARY KEY, "
                 "EMAIL TEXT, "
                 "PHONE TEXT )"
                 )

    for _ in range(3):
        add_random_member(conn)

    conn.commit()
    return conn


def get_connection(database_path: str) -> sqlite3.Connection:
    """
    Returns connection to the database.
    If database file is not found then it creates database.
    """
    if Path(database_path).is_file():
        conn = sqlite3.connect(database_path)
        return conn
    else:
        print("Database not found! Creating fresh ...")
        return create_database(database_path)


def add_random_member(conn: sqlite3.Connection):
    """
    Adds random member with random int values to table MEMBERS
    """
    query = "INSERT INTO MEMBERS VALUES(?,?,?)"
    random_id = "".join(random.choices(digits, k=4))
    random_email = "".join(random.choices(ascii_uppercase, k=5))
    random_phone = "".join(random.choices(digits, k=8))
    conn.execute(query, (random_id, random_email, random_phone))
    conn.commit()


def get_member_data(member_id: str, conn: sqlite3.Connection) -> dict:
    """
    Gets email and phone data from database based on passed member.
    This function uses placeholders in query so it is injection safe.
    Look up get_member_data_injection for example where it's NOT injection safe.
    """
    query = "SELECT EMAIL,PHONE FROM MEMBERS WHERE MEMBER_ID=?"
    cursor = conn.cursor()
    cursor.execute(query, (member_id,))
    rows = cursor.fetchall()
    return dict(rows)


def get_member_data_injection(member_id: str, conn: sqlite3.Connection) -> dict:
    """
    Gets email and phone data from database based on passed member.
    This function uses direct string formatting for query so it is NOT injection safe.
    Look up get_member_data for example where it's injection safe.
    """
    query = "SELECT EMAIL,PHONE FROM MEMBERS WHERE MEMBER_ID={}".format(member_id)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return dict(rows)


def print_db(conn):
    query = "SELECT * FROM MEMBERS"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    print("Printing database table MEMBERS:")
    for row in rows:
        print("\t", dict(row))
    # newline for pretty print
    print()


if __name__ == "__main__":
    connection = get_connection("db.sqlite3")
    connection.row_factory = sqlite3.Row  # this  is for getting the column names when we fetch, for nice printing
    print("Connected to database..\n")

    print_db(connection)

    while True:
        message = ("Enter 1 for querying with injection SAFE query. "
                   "Enter 2 for querying with injection UNSAFE query. "
                   "Exit to stop.\n"
                   "Your input:")

        user_input = input(message).lower()
        if user_input == "1":
            query_method = get_member_data
        elif user_input == "2":
            query_method = get_member_data_injection
        elif user_input == "exit":
            break
        else:
            print("Unknown input..")
            continue

        member_id_input = input("Enter member ID that you want to fetch data from. "
                                "(to test vulnerability you can input '123 OR 1=1' without quotes)\n"
                                "Your input:")
        print("Results:", query_method(member_id_input, connection), "\n")
