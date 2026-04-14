from mysql.connector import MySQLConnection, connect, Error
from mysql.connector.cursor import MySQLCursor
from typing import Any
import json


try:
    with open("api/db/config.json", "r") as file:
        DB_CONFIG: dict[str, Any] = json.load(file)
except Exception as e:
    raise RuntimeError(f"Failed to load DB config: {e}")


def get_connection() -> MySQLConnection:
    try:
        conn = connect(
            database=DB_CONFIG["database"],
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            autocommit=True,
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
    except Exception as e:
        raise RuntimeError(f"Failed to connect to MySQL database")
    return conn



def run_proc(
    conn: MySQLConnection,
    proc: str,
    args: tuple = ()
) -> list[list[Any]]:
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc(proc, args)

        results = []
        for result_cursor in cursor.stored_results():
            results.append(result_cursor.fetchall())

        conn.commit()
        return results

    except Error as e:
        conn.rollback()
        raise RuntimeError(
            f"MySQL procedure error ({e.sqlstate}): {e.msg}"
        ) from e

    finally:
        cursor.close()