CREATE DATABASE IF NOT EXISTS bank;

USE bank;

CREATE TABLE IF NOT EXISTS users (
    account_number INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    address VARCHAR(255),
    email VARCHAR(100),
    phone VARCHAR(10),
    password VARCHAR(255),
    balance DECIMAL(10, 2) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_number INT,
    transaction_type VARCHAR(50),
    amount DECIMAL(10, 2),
    date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_number) REFERENCES users(account_number)
);
