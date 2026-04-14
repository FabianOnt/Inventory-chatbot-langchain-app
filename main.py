import sys


def configure() -> None:
    """
    Create config.json files among all the project independent sections 
    with only the necessary data on them. Open config/config.py to modify
    such values.
    """
    
    import json

    from backend.config.config import (
        DATABASE,
        HOST,
        PORT,
        ADMIN_USER,
        ADMIN_PASSWORD,
        API_USER,
        API_PASSWORD,
        APP_ADMIN_NAME,
        APP_ADMIN_USER,
        APP_ADMIN_PASSWORD
    )

    with open("backend/db/config.json", "w", encoding="utf-8") as file:
        json.dump(
            {
                "database": DATABASE,
                "host": HOST,
                "port": PORT,
                "admin_user": ADMIN_USER,
                "admin_password": ADMIN_PASSWORD,
                "api_user": API_USER,
                "api_password": API_PASSWORD,
                "app_admin_name": APP_ADMIN_NAME,
                "app_admin_user": APP_ADMIN_USER,
                "app_admin_password": APP_ADMIN_PASSWORD
            },
            file,
            indent=4
        )

    with open("backend/api/db/config.json", "w", encoding="utf-8") as file:
        json.dump(
            {
                "database": DATABASE,
                "host": HOST,
                "port": PORT,
                "user": API_USER,
                "password": API_PASSWORD
            },
            file,
            indent=4
        )


def initialize() -> None:
    """
    Initialize the MySQL database and the Python REST API from scratch.
    MySQL users are created and the API is turned on.
    """

    from backend.db.init import initialize_database
    
    print("Initializing DB ... ", end="", flush=True)
    try:
        initialize_database()
    except Exception as e:
        print("failed.")
        raise RuntimeError(f"Database initialization failed: {e}")
    else:
        print("done.")



def main() -> None:
    """
    Main controller of the program.
    """
    configure()
    initialize()


if __name__ == "__main__":

    cmd = sys.argv[1] if len(sys.argv) > 1 else "main"

    if cmd == "config":
        configure()
    elif cmd == "init":
        initialize()

    elif cmd == "main":
        main()
    else:
        print("Unknown command")