# SonamRinzin_02240126_A3_test.py
import unittest
import os
from SonamRinzin_02240126_A3_PA import (
    Bank_Account,
    Personal_account,
    Business_account,
    Banking_system,
    InvalidAmountError,
    InsufficientFundsError,
    InvalidAccountError,
    BankError
)

class TestBankAccount(unittest.TestCase):
    """Test cases for Bank_Account class"""
    
    def setUp(self):
        self.account = Bank_Account("12345", "1234", "Personal", 1000)
    
    def test_deposit_positive_amount(self):
        """Test depositing a positive amount"""
        result = self.account.deposit(500)
        self.assertEqual(self.account.funds, 1500)
        self.assertIn("Deposited Nu: 500", result)
    
    def test_deposit_negative_amount(self):
        """Test depositing a negative amount"""
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(-100)
    
    def test_deposit_zero_amount(self):
        """Test depositing zero amount"""
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(0)
    
    def test_withdraw_valid_amount(self):
        """Test withdrawing a valid amount"""
        result = self.account.withdraw(500)
        self.assertEqual(self.account.funds, 500)
        self.assertIn("Withdrew Nu: 500", result)
    
    def test_withdraw_negative_amount(self):
        """Test withdrawing a negative amount"""
        with self.assertRaises(InvalidAmountError):
            self.account.withdraw(-100)
    
    def test_withdraw_zero_amount(self):
        """Test withdrawing zero amount"""
        with self.assertRaises(InvalidAmountError):
            self.account.withdraw(0)
    
    def test_withdraw_insufficient_funds(self):
        """Test withdrawing more than available balance"""
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(1500)
    
    def test_transfer_successful(self):
        """Test successful transfer between accounts"""
        recipient = Bank_Account("54321", "4321", "Personal", 500)
        result = self.account.transfer(300, recipient)
        self.assertEqual(self.account.funds, 700)
        self.assertEqual(recipient.funds, 800)
        self.assertIn("transferred Nu: 300", result)
    
    def test_transfer_insufficient_funds(self):
        """Test transfer with insufficient funds"""
        recipient = Bank_Account("54321", "4321", "Personal", 500)
        with self.assertRaises(BankError):
            self.account.transfer(1500, recipient)
    
    def test_transfer_invalid_recipient(self):
        """Test transfer to None recipient"""
        with self.assertRaises(BankError):
            self.account.transfer(100, None)

