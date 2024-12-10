
# YASH Banking Management System

## Introduction

YASH Banking Management System is a Python-based core banking application that utilizes Object-Oriented Programming (OOP) principles 
and Python Database Connectivity (PDBC). 
This system allows users to manage their banking operations, including user authentication (login and signup) and 
basic CRUD operations for bank accounts.
The application uses decorators to control access to certain operations, ensuring that a user must be logged in before performing sensitive transactions.


## Features

- **User  Management:**
  - Signup for new users
  - Login for existing users
  

- **Banking Operations:**
  - Deposit money
  - Withdraw money
  - View bank balance
  - Transfer money to another account

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system
- A database management system (e.g.MySQL)

## Installation and Running

Clone the repository:

```
git clone https://github.com/SanketUpadhyay01/Bank_Management_System.git
cd bank_management_pdbc
```

Install the required dependencies:
```
pip install -r requirements.txt
```
Create the database schema using utils/bank.sql script.

Run main.py to launch the application
