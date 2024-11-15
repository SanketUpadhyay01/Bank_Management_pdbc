import os
import sys
import pytest
from decimal import Decimal

# Added the parent directory of 'models' to the system path to import model file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.bank_model import BankModel
from validation.bank_validation import BankValidation

@pytest.fixture
def bank_model():
    """
    Sets up the BankModel instance for testing.
    Ensures the database connection is closed after testing.
    """
    model = BankModel()
    yield model
    model.close_connection()

@pytest.fixture
def bank_validation():
    """
    Sets up the BankValidation instance for testing.
    """
    return BankValidation()

def test_create_account(bank_model: BankModel):
    """
    Tests account creation functionality in BankModel.
    Ensures a new account is created and a valid account number is returned.
    """
    account_number = bank_model.create_account(
        name="John Doe",
        age=30,
        address="123 Main St",
        email="john@example.com",
        phone="1234567890",
        password="StrongPassword@123"
    )
    assert account_number is not None
    assert bank_model.check_account_exists(account_number) == True

def test_get_balance(bank_model: BankModel):
    """
    Tests balance retrieval for an existing account.
    Ensures the returned balance is of Decimal type.
    """
    account_number = bank_model.create_account(
        name="Jane Doe",
        age=28,
        address="456 Elm St",
        email="jane@example.com",
        phone="0987654321",
        password="AnotherPassword@123"
    )
    balance = bank_model.get_balance(account_number)
    assert isinstance(balance, Decimal)

def test_deposit(bank_model: BankModel):
    """
    Tests deposit functionality by adding funds to an account.
    Verifies that the balance is updated correctly.
    """
    account_number = bank_model.create_account(
        name="Alice Smith",
        age=40,
        address="789 Oak St",
        email="alice@example.com",
        phone="5555555555",
        password="SecurePassword@123"
    )
    initial_balance = bank_model.get_balance(account_number)
    deposit_amount = Decimal('500.00')
    bank_model.update_balance(account_number, initial_balance + deposit_amount)
    new_balance = bank_model.get_balance(account_number)
    assert new_balance == initial_balance + deposit_amount

def test_withdraw(bank_model: BankModel, bank_validation: BankValidation):
    """
    Tests withdrawal functionality by deducting funds from an account.
    """
    account_number = bank_model.create_account(
        name="Bob Brown",
        age=35,
        address="321 Maple St",
        email="bob@example.com",
        phone="6666666666",
        password="WithdrawalTest@123"
    )
    initial_balance = bank_model.get_balance(account_number)
    withdrawal_amount = Decimal('200.00')

    if bank_validation.validate_sufficient_balance(account_number, withdrawal_amount):
        bank_model.update_balance(account_number, initial_balance - withdrawal_amount)
        new_balance = bank_model.get_balance(account_number)
        assert new_balance == initial_balance - withdrawal_amount
    else:
        pytest.skip("Insufficient funds for withdrawal test.")

def test_transfer_funds(bank_model: BankModel):
    """
    Tests fund transfer functionality between two accounts.
    Ensures that the sender's balance decreases and the receiver's balance increases.
    """
    sender_account = bank_model.create_account(
        name="Charlie Green",
        age=32,
        address="654 Pine St",
        email="charlie@example.com",
        phone="7777777777",
        password="SenderPassword@123"
    )
    receiver_account = bank_model.create_account(
        name="Dana Blue",
        age=29,
        address="987 Cedar St",
        email="dana@example.com",
        phone="8888888888",
        password="ReceiverPassword@123"
    )

    transfer_amount = Decimal('150.00')
    sender_initial_balance = bank_model.get_balance(sender_account)
    receiver_initial_balance = bank_model.get_balance(receiver_account)

    if sender_initial_balance >= transfer_amount:
        transfer_success = bank_model.transfer_funds(sender_account, receiver_account, transfer_amount)
        assert transfer_success

        sender_new_balance = bank_model.get_balance(sender_account)
        receiver_new_balance = bank_model.get_balance(receiver_account)

        assert sender_new_balance == sender_initial_balance - transfer_amount
        assert receiver_new_balance == receiver_initial_balance + transfer_amount
    else:
        pytest.skip("Insufficient funds for transfer test.")
