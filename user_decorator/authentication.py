from log import logger
from functools import wraps
from colorama import Fore, Style

def login_required(func):
    @wraps(func)
    def wrapper(controller, *args, **kwargs):
        if not controller.is_logged_in:
            print(Fore.RED + "Please log in first." + Style.RESET_ALL)
            logger.warning("Attempted operation without login.")
            controller.main_menu()  # Redirect to main menu for login if not logged in
        else:
            return func(controller, *args, **kwargs)
    return wrapper
