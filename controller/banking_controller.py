from log import logger
from view.login import Login
from view.signup import Signup
from colorama import Fore, Style
from models.bank_model import BankModel
from view.bank_operations import BankOperation
from user_decorator.authentication import login_required  # Import the login_required decorator

class BankController:
    """
    Controls the flow of the banking system.
    Manages user sessions and provides options for banking operations.
    """
    def __init__(self):
        """
        Initializes BankController with default login status and user session.
        """
        self.bank_operation = BankOperation()
        self.bank_model = None  # Initialize without connection
        self.is_logged_in = False
        self.logged_in_user = None

    def main_menu(self):
        """
        Displays the main menu with signup, login, and exit options.
        """
        while True:
            print(Fore.LIGHTBLUE_EX + "\n===== Welcome to Banking System =====")
            print(Fore.YELLOW + "1. Signup")
            print(Fore.YELLOW + "2. Login")
            print(Fore.YELLOW + "3. Exit")
            choice = input(Fore.LIGHTWHITE_EX + "Enter your choice: ")

            if choice == "1":
                Signup().signup_user()
            elif choice == "2":
                self.is_logged_in, self.logged_in_user = Login().login_user()
                if self.is_logged_in:
                    self.bank_model = BankModel()  # Open the database connection after login
                    self.bank_operations_menu()  # Access banking operations menu
            elif choice == "3":
                self.close_connection()  # Close the database connection before exiting
                print(Fore.GREEN + "Thank you for using the banking system.")
                break
            else:
                print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

    @login_required
    def bank_operations_menu(self):
        """
        Displays the bank operations menu after the user logs in.
        """
        while True:
            print("\n===== Bank Operations =====")
            print(Fore.YELLOW + "1. Deposit")
            print(Fore.YELLOW + "2. Withdraw")
            print(Fore.YELLOW + "3. Check Balance")
            print(Fore.YELLOW + "4. Transfer Money")
            print(Fore.YELLOW + "5. Show Account Statement")
            print(Fore.YELLOW + "6. Logout")
            choice = input(Fore.LIGHTWHITE_EX + "Enter your choice: ")

            if choice == "1":
                self.bank_operation.deposit(self.logged_in_user)
            elif choice == "2":
                self.bank_operation.withdraw(self.logged_in_user)
            elif choice == "3":
                self.bank_operation.check_balance(self.logged_in_user)
            elif choice == "4":
                self.bank_operation.transfer_money(self.logged_in_user)
            elif choice == "5":
                self.bank_operation.show_transaction_history(self.logged_in_user)
            elif choice == "6":
                self.logout()
                break
            else:
                print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

    def logout(self):
        """
        Logs the user out by clearing session data.
        """
        self.is_logged_in = False
        self.logged_in_user = None
        print(Fore.GREEN + "Logged out successfully." + Style.RESET_ALL)
        self.close_connection()  # Close the database connection on logout
        logger.info("User  logged out.")

    def close_connection(self):
        """
        Closes the database connection if open.
        """
        if self.bank_model and self.bank_model.connection.open:
            self.bank_model.close_connection()
            logger.info("Database connection closed.")
