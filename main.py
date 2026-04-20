import sys
import subprocess

def configure() -> None:
    """
    Create config.json files among all the project independent sections 
    with only the necessary data on them. Open config/config.py to modify
    such values.
    """
    
    import json

    from config.config import (
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

    print("Configuring project ... ", end="", flush=True)

    try:
        with open("db/config.json", "w", encoding="utf-8") as file:
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

        with open("api/db/config.json", "w", encoding="utf-8") as file:
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
    except Exception as e:
        print("failed.")
        raise RuntimeError(f"Project configuration failed: {e}")
    else:
        print("done.")

def initialize() -> None:
    """
    Initialize the MySQL database and the Python REST API from scratch.
    MySQL users are created and the API is turned on.
    """

    from db.init import initialize_database
    
    print("Initializing DB ... ", end="", flush=True)
    try:
        initialize_database()
    except Exception as e:
        print("failed.")
        raise RuntimeError(f"Database initialization failed: {e}")
    else:
        print("done.")


def run_api(
    host: str = "localhost",
    port: int = 8000,
    timeout: int = 30
) -> subprocess.Popen:
    """
    Start the API server and wait until it is ready.
    """
    import time
    import requests

    print("Starting API ... ", end="", flush=True)
    try:
        process = subprocess.Popen(
            ["cmd.exe", "/k", "fastapi run app.py"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        url = f"http://{host}:{port}"
        start_time = time.time()

        while time.time() - start_time < timeout:
            if process.poll() is not None:
                raise RuntimeError("API process terminated before startup completed.")

            try:
                response = requests.get(url, timeout=1)

                if response.status_code == 200:
                    print("done.")
                    return process

            except requests.RequestException:
                pass
            time.sleep(0.5)
    except Exception as e:
        print("failed.")
        process.terminate()
        raise TimeoutError(f"API did not start within {timeout} seconds.")


def populate() -> None:
    """
    Populate the MySQL database by API-calls with the API-Client interface.
    """
    from generation.generator import populate_database
    
    print("Populating DB ... ", end="", flush=True)
    try:
        populate_database()
    except Exception as e:
        print("failed.")
        raise RuntimeError(f"Database population process failed: {e}")
    else:
        print("done.")


def chat() -> None:
    """
    Start the chatbot model
    """
    print("Starting chatbot ... ", end="", flush=True)
    try:
        process = subprocess.Popen(
            ["cmd.exe", "/k", "python3 run chat.py"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        if process.poll() is not None:
            raise RuntimeError("Chatbot service terminated before startup completed.")
    except Exception as e:
        raise RuntimeError(f"Error running chatbot service: {e}")
    else:
        print("done.")

def main() -> None:
    """
    Main controller of the program.
    """
    configure()
    initialize()
    run_api()
    populate()
    chat()


if __name__ == "__main__":

    cmd = sys.argv[1] if len(sys.argv) > 1 else "main"

    if cmd == "config":
        configure()
    elif cmd == "init":
        initialize()
    elif cmd == "api":
        run_api()
    elif cmd == "populate":
        populate()
    elif cmd == "main":
        main()
    elif cmd == "chat":
        chat()

    else:
        print("Unknown command")