import os 
import pymysql
from log import logger
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

class BankModel:
    """
    Interacts with the database to perform operations on user accounts and transactions.
    """

    def __init__(self):
        """
        Initializes the database connection.
        """
        self.connection = pymysql.connect(
            host= os.getenv("DB_HOST") ,
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.connection.cursor()

    def create_account(self, name: str, age: int, address: str, email: str, phone: str, password: str) -> int:
        """
        Creates a new account and stores user details in the database.
        Returns the account number.
        """
        self.cursor.execute("SELECT MAX(account_number) FROM users")
        result = self.cursor.fetchone()
        last_account_number = result[0] if result[0] is not None else 540000
        new_account_number = last_account_number + 1

        query = """
        INSERT INTO users (account_number, name, age, address, email, phone, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (new_account_number, name, age, address, email, phone, password))
        self.connection.commit()

        return new_account_number

    def check_account_exists(self, account_number: int) -> bool:
        """
        Checks if an account exists in the database based on account number.
        """
        query = "SELECT account_number FROM users WHERE account_number = %s"
        self.cursor.execute(query, (account_number,))
        result = self.cursor.fetchone()
        return result is not None

    def get_user(self, account_number: int):
        """
        Retrieves user information from the database.
        """
        query = "SELECT * FROM users WHERE account_number = %s"
        self.cursor.execute(query, (account_number,))
        return self.cursor.fetchone()

    def update_balance(self, account_number: int, new_balance: Decimal) -> None:
        """
        Updates the balance for the given account number.
        """
        query = "UPDATE users SET balance = %s WHERE account_number = %s"
        self.cursor.execute(query, (new_balance, account_number))
        self.connection.commit()

    def get_balance(self, account_number: int) -> Decimal:
        """
        Retrieves the current balance for the given account number.
        """
        query = "SELECT balance FROM users WHERE account_number = %s"
        self.cursor.execute(query, (account_number,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def add_transaction(self, account_number: int, transaction_type: str, amount: Decimal) -> None:
        """
        Adds a transaction record to the database.
        """
        query = """
        INSERT INTO transactions (account_number, transaction_type, amount)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (account_number, transaction_type, amount))
        self.connection.commit()

    def transfer_funds(self, sender_account: int, receiver_account: int, amount: Decimal) -> bool:
        """
        Transfers funds between two accounts.
        Returns True if successful, otherwise False.
        """
        sender_balance = self.get_balance(sender_account)
        receiver_balance = self.get_balance(receiver_account)

        if sender_balance is None or receiver_balance is None:
            return False  # One of the accounts does not exist

        if sender_balance < amount:
            return False  # Not enough funds

        self.update_balance(sender_account, sender_balance - amount)
        self.update_balance(receiver_account, receiver_balance + amount)
        self.add_transaction(sender_account, "Transfer Out", amount)
        self.add_transaction(receiver_account, "Transfer In", amount)

        return True

    def get_transaction_history(self, account_number: int):
        """
        Retrieves the transaction history for a specific account.
        """
        try:
            query = """
            SELECT transaction_type, amount, date_time
            FROM transactions
            WHERE account_number = %s
            ORDER BY date_time DESC
            """
            self.cursor.execute(query, (account_number,))
            transactions = self.cursor.fetchall()
            return transactions
        except Exception as e:
            logger.error(f"Error fetching transaction history for account {account_number}: {e}")
            return None

    def close_connection(self):
        """
        Close the database connection.
        """
        if self.connection.open:
            self.connection.close()
            print("Database connection closed.")
