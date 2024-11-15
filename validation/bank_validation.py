from log import logger
from models.bank_model import BankModel

class BankValidation:

    """
    Validates bank-specific operations, such as checking account existence and sufficient funds.
    """

    def __init__(self):
        self.bank_model = BankModel()

    def validate_account_exists(self, account_number: int) -> bool:
        """
        Checks if an account exists in the bank database based on the account number.
        Returns True if the account exists, otherwise False.
        """
        exists = self.bank_model.check_account_exists(account_number)
        if exists:
            logger.info(f"Account {account_number} exists.")
        else:
            logger.warning(f"Account {account_number} does not exist.")
        return exists

    def validate_sufficient_balance(self, account_number: int, amount: float) -> bool:
        """
        Checks if an account has sufficient balance for a withdrawal or transfer.
        Returns True if there are sufficient funds, otherwise False.
        """
        balance = self.bank_model.get_balance(account_number)
        if balance is None:
            logger.warning(f"Balance check failed: Account {account_number} does not exist.")
            return False
        elif balance >= amount:
            logger.info(f"Account {account_number} has sufficient balance for transaction.")
            return True
        else:
            logger.warning(f"Account {account_number} has insufficient balance for transaction.")
            return False
