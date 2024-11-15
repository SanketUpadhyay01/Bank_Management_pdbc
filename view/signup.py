from log import logger
from colorama import Fore, Style
from models.bank_model import BankModel
from validation.user_validation import UserValidation

class Signup:
    """
    Handles user signup and account creation.
    """

    def __init__(self):
        self.bank_model = BankModel()
        self.user_validation = UserValidation()

    def signup_user(self):
        """
        Takes user input for signup and creates an account after validation.
        """
        while True:
            try:
                name = input("Enter your name: ")
                if not self.user_validation.validate_name(name):
                    raise ValueError("Name must contain only alphabetic characters and spaces.")
                break
            except ValueError as e:
                print(Fore.RED + str(e) + Style.RESET_ALL)
                logger.error(f"Invalid name entered: {name}")

        while True:
            try:
                age = input("Enter your age: ")
                if not age.isdigit() or not self.user_validation.validate_age(int(age)):
                    raise ValueError("Age must be a positive integer.")
                age = int(age)
                break
            except ValueError as e:
                print(Fore.RED + str(e) + Style.RESET_ALL)
                logger.error(f"Invalid age entered: {age}")

        while True:
            try:
                address = input("Enter your address: ")
                if not address:
                    raise ValueError("Address cannot be empty.")
                break
            except ValueError as e:
                print(Fore.RED + str(e) + Style.RESET_ALL)
                logger.error("Address field cannot be empty.")

        while True:
            try:
                email = input("Enter your email: ")
                if not self.user_validation.validate_email(email):
                    raise ValueError("Invalid email format. Must contain '@' and end with a domain like '.com'.")
                break
            except ValueError as e:
                print(Fore.RED + str(e) + Style.RESET_ALL)
                logger.error(f"Invalid email entered: {email}")

        while True:
            try:
                phone = input("Enter your phone number: ")
                if not self.user_validation.validate_phone(phone):
                    raise ValueError("Phone number must be 10 digits and contain only numbers.")
                break
            except ValueError as e:
                print(Fore.RED + str(e) + Style.RESET_ALL)
                logger.error(f"Invalid phone number entered: {phone}")

        while True:
            try:
                password = input("Enter your password (min 12 characters, uppercase, lowercase, number, special character): ")
                if not self.user_validation.validate_password(password):
                    raise ValueError(
                        "Password must be at least 12 characters long and include uppercase, lowercase, number, and special character."
                    )
                break
            except ValueError as e:
                print(Fore.RED + str(e) + Style.RESET_ALL)
                logger.error("Invalid password format.")

        account_number = self.bank_model.create_account(name, age, address, email, phone, password)
        print(Fore.GREEN + f"Account created successfully. Your account number is: {account_number}" + Style.RESET_ALL)
        logger.info(f"Account {account_number} created successfully for user {name}.")
