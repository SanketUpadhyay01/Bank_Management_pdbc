from log import logger
from decimal import Decimal
from colorama import Fore, Style
from models.bank_model import BankModel

class BankOperation:
    """
    Handles bank operations such as deposit, withdrawal, balance check, money transfer, and transaction history.
    """

    def __init__(self):
        self.bank_model = BankModel()

    def deposit(self, account_number):
        """
        Deposits a specified amount to the user's account.
        """
        try:
            amount = Decimal(input("Enter amount to deposit: "))

            # Check if the deposit amount is within the allowed range
            if amount < 1 or amount > 100000:
                print(Fore.RED + "Deposit amount must be between 1 and 100,000." + Style.RESET_ALL)
                return

            balance = self.bank_model.get_balance(account_number)
            new_balance = balance + amount
            self.bank_model.update_balance(account_number, new_balance)
            self.bank_model.add_transaction(account_number, "Deposit", amount)
            print(Fore.GREEN + f"Deposit successful. New balance: {new_balance}" + Style.RESET_ALL)
            logger.info(f"Deposit of {amount} made to account {account_number}. New balance: {new_balance}")
        except ValueError:
            print(Fore.RED + "Invalid amount. Please enter a numeric value." + Style.RESET_ALL)
            logger.error("Invalid amount entered for deposit.")
        finally:
            logger.info("Deposit operation completed.")

    def withdraw(self, account_number):
        """
        Withdraws a specified amount from the user's account.
        """
        try:
            amount = Decimal(input("Enter amount to withdraw: "))

            # Check if the withdrawal amount is within the allowed range
            if amount < 1 or amount > 100000:
                print(Fore.RED + "Withdrawal amount must be between 1 and 100,000." + Style.RESET_ALL)
                return

            balance = self.bank_model.get_balance(account_number)
            if balance < amount:
                print(Fore.RED + "Insufficient funds." + Style.RESET_ALL)
                logger.warning(f"Withdrawal of {amount} failed due to insufficient funds in account {account_number}.")
                return
            new_balance = balance - amount
            self.bank_model.update_balance(account_number, new_balance)
            self.bank_model.add_transaction(account_number, "Withdrawal", amount)
            print(Fore.GREEN + f"Withdrawal successful. New balance: {new_balance}" + Style.RESET_ALL)
            logger.info(f"Withdrawal of {amount} made from account {account_number}. New balance: {new_balance}")
        except ValueError:
            print(Fore.RED + "Invalid amount. Please enter a numeric value." + Style.RESET_ALL)
            logger.error("Invalid amount entered for withdrawal.")
        finally:
            logger.info("Withdrawal operation completed.")

    def check_balance(self, account_number):
        """
        Displays the current balance of the user's account.
        """
        try:
            balance = self.bank_model.get_balance(account_number)
            print(Fore.CYAN + f"Your current balance is: {balance}" + Style.RESET_ALL)
            logger.info(f"Balance check for account {account_number}. Balance: {balance}")
        except Exception as e:
            logger.error(f"Error during balance check: {e}")
        finally:
            logger.info("Balance check operation completed.")

    def transfer_money(self, account_number):
        """
        Transfers a specified amount to another user's account.
        """
        while True:
            try:
                receiver_account = int(input("Enter receiver's account number: "))

                # Check if receiver account exists
                if not self.bank_model.check_account_exists(receiver_account):
                    raise ValueError("Invalid account number.")

                amount = Decimal(input("Enter amount to transfer: "))

                # Check if the transfer amount is within the allowed range
                if amount < 1 or amount > 100000:
                    print(Fore.RED + "Transfer amount must be between 1 and 100,000." + Style.RESET_ALL)
                    continue

                sender_balance = self.bank_model.get_balance(account_number)
                if sender_balance < amount:
                    print(Fore.RED + "Insufficient funds for the transfer." + Style.RESET_ALL)
                    return

                # Perform the transfer
                transfer_success = self.bank_model.transfer_funds(account_number, receiver_account, amount)
                if transfer_success:
                    print(Fore.GREEN + f"Successfully transferred {amount} to account {receiver_account}." + Style.RESET_ALL)
                    logger.info(f"Transfer of {amount} from account {account_number} to account {receiver_account} successful.")
                else:
                    print(Fore.RED + "Transfer failed due to an issue with account numbers or balance." + Style.RESET_ALL)
                    logger.warning(f"Transfer of {amount} from account {account_number} to account {receiver_account} failed.")
                break
            except ValueError as e:
                print(Fore.RED + f"{e}. Please enter a valid account number." + Style.RESET_ALL)
                logger.error(f"Invalid receiver account number entered: {receiver_account}")
            except Exception as e:
                print(Fore.RED + "An error occurred during the transfer." + Style.RESET_ALL)
                logger.error(f"Error during transfer: {e}")

    def show_transaction_history(self, account_number):
        """
        Displays the transaction history for a specific account.
        """
        transactions = self.bank_model.get_transaction_history(account_number)
        if transactions:
            print(Fore.CYAN + f"{'Type':<15}{'Amount':<10}{'Date'}" + Style.RESET_ALL)
            for transaction in transactions:
                print(f"{transaction[0]:<15}{transaction[1]:<10}{transaction[2].strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"Displayed transaction history for account {account_number}")
        else:
            print(Fore.RED + "No transactions found." + Style.RESET_ALL)
            logger.info(f"No transactions found for account {account_number}")
