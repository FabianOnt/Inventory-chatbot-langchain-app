from datetime import datetime
from functools import wraps
from typing import Callable, Any

from core.client import APIClient


BASE_URL = "http://localhost:8000"
USERNAME = "admin.app@example.com"
PASSWORD = "secretpassword"

CLIENT = APIClient(base_url=BASE_URL)
LAST_LOG_IN: datetime


def reset_connection() -> None:
    global CLIENT, LAST_LOG_IN, USERNAME, PASSWORD
    CLIENT.login(
        username=USERNAME,
        password=PASSWORD
    )
    LAST_LOG_IN = datetime.now()



def safe_api_call(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)

        except Exception as original_error:
            try:
                reset_connection()
                try:
                    return func(*args, **kwargs)
                
                except Exception as func_error:
                    raise RuntimeError(
                        f"API-function error: {func_error}"
                ) from func_error

            except Exception as login_error:
                raise RuntimeError(
                    f"Chatbot session error. Re-login failed: {login_error}"
                ) from login_error

    return wrapper