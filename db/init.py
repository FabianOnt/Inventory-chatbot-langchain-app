from mysql.connector import MySQLConnection, connect
from mysql.connector.cursor import MySQLCursor
from typing import Any
import json


try:
    with open("db/config.json", "r") as file:
        DB_CONFIG: dict[str, Any] = json.load(file)
except Exception as e:
    raise RuntimeError(f"Failed to load DB config: {e}")


def run_sql_script(
    cursor: MySQLCursor, 
    filename: str, 
    delimiter: str = ";"
):
    """Execute a SQL script file."""
    sentence: str = ""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            script = file.read()

        statements = script.split(delimiter)

        for stmt in statements:
            sentence = stmt.strip()
            if sentence:  # skip empty statements
                cursor.execute(sentence)

    except Exception as e:
        raise RuntimeError(
            f"An error occurred when executing SQL statement:\n{sentence}\nError: {e}"
        )


def initialize_database():
    """(Delete and) create the DB, load schema and procedures."""
    global DB_CONFIG

    try:
        conn = connect(
            user=DB_CONFIG["admin_user"],
            password=DB_CONFIG["admin_password"],
            host=DB_CONFIG["host"],
            autocommit=True,
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to connect to the MySQL database: {e}"
        )
    
    cursor = conn.cursor()
    database = DB_CONFIG['database']

    cursor.execute(
        operation=f"DROP DATABASE IF EXISTS {database}"
    )

    cursor.execute(
        operation=f"CREATE DATABASE {database}"
    )

    cursor.execute(
        operation=f"USE {database}"
    )

    files = [
        ("db/schema.sql", ";"),
        ("db/procedures.sql", "//")
    ]

    for filename, delimiter in files:
        run_sql_script(
            cursor=cursor, 
            filename=filename,
            delimiter=delimiter
        )

    # Create the Admin user at the API level (password-hashed)
    admin_name = DB_CONFIG['app_admin_name']
    admin_user = DB_CONFIG['app_admin_user']

    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    admin_password = pwd_context.hash(DB_CONFIG['app_admin_password'])

    cursor.execute(
        operation=f"""
            INSERT INTO users (name, email, password, permission_level)
            VALUES ('{admin_name}','{admin_user}','{admin_password}','admin')
        """
    )

    api_user = DB_CONFIG['api_user']
    api_password = DB_CONFIG['api_password']

    cursor.execute(
        operation=f"""
            DROP USER IF EXISTS '{api_user}'@'localhost'
        """
    )

    cursor.execute(
        operation=f"""
            CREATE USER '{api_user}'@'localhost' IDENTIFIED BY '{api_password}'
        """
    )

    cursor.execute(
        operation=F"""
            GRANT EXECUTE ON {database}.* TO '{api_user}'@'localhost'
        """
    )

    conn.close()