from log import logger
from colorama import Fore, Style
from models.bank_model import BankModel

class Login:
    """
    Handles user login process.
    """

    def __init__(self):
        self.bank_model = BankModel()

    def login_user(self):
        """
        Logs the user in by validating account number and password.
        """
        while True:
            try:
                account_number = int(input("Enter your account number: "))
                user = self.bank_model.get_user(account_number)

                if user is None:
                    raise ValueError("Invalid account number.")

                password = input("Enter your password: ")

                if user[6] == password: 
                    print(Fore.GREEN + "Login successful. Welcome!" + Style.RESET_ALL)
                    logger.info(f"User  {account_number} logged in successfully.")
                    return True, account_number  # Return login state and account number
                else:
                    print(Fore.RED + "Invalid password." + Style.RESET_ALL)
                    logger.warning("Failed login attempt due to invalid password.")
                    return False, None
            except ValueError as ve:
                print(Fore.RED + str(ve) + Style.RESET_ALL)
                logger.error("Invalid input during login.")
            except Exception as e:
                print(Fore.RED + "An error occurred: " + str(e) + Style.RESET_ALL)
                logger.error("An unexpected error occurred during login.")