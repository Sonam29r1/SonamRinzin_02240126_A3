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

class TestPersonalAccount(unittest.TestCase):
    """Test cases for Personal_account subclass"""
    
    def test_personal_account_creation(self):
        """Test personal account creation with default values"""
        account = Personal_account("12345", "1234")
        self.assertEqual(account.account_category, "Personal")
        self.assertEqual(account.funds, 0)
    
    def test_personal_account_with_funds(self):
        """Test personal account creation with initial funds"""
        account = Personal_account("12345", "1234", "Personal", 1000)
        self.assertEqual(account.funds, 1000)

class TestBusinessAccount(unittest.TestCase):
    """Test cases for Business_account subclass"""
    
    def test_business_account_creation(self):
        """Test business account creation with default values"""
        account = Business_account("12345", "1234")
        self.assertEqual(account.account_category, "Business")
        self.assertEqual(account.funds, 0)
    
    def test_business_account_with_funds(self):
        """Test business account creation with initial funds"""
        account = Business_account("12345", "1234", "Business", 5000)
        self.assertEqual(account.funds, 5000)

class TestBankingSystem(unittest.TestCase):
    """Test cases for Banking_system class"""
    
    def setUp(self):
        self.test_filename = "test_accounts.txt"
        with open(self.test_filename, "w") as f:
            f.write("10001,1111,Personal,1000\n")
            f.write("20002,2222,Business,5000\n")
        self.bank = Banking_system(self.test_filename)
    
    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
    
    def test_load_accounts(self):
        """Test loading accounts from file"""
        self.assertEqual(len(self.bank.accounts), 2)
        self.assertIn("10001", self.bank.accounts)
        self.assertIn("20002", self.bank.accounts)
    
    def test_create_personal_account(self):
        """Test creating a new personal account"""
        account = self.bank.create_account("Personal")
        self.assertEqual(account.account_category, "Personal")
        self.assertEqual(account.funds, 0)
        self.assertIn(account.id, self.bank.accounts)
    
    def test_create_business_account(self):
        """Test creating a new business account"""
        account = self.bank.create_account("Business")
        self.assertEqual(account.account_category, "Business")
        self.assertEqual(account.funds, 0)
        self.assertIn(account.id, self.bank.accounts)
    
    def test_create_invalid_account_type(self):
        """Test creating account with invalid type"""
        with self.assertRaises(ValueError):
            self.bank.create_account("InvalidType")
    
    def test_login_success(self):
        """Test successful login"""
        account = self.bank.login("10001", "1111")
        self.assertEqual(account.id, "10001")
        self.assertEqual(account.passcode, "1111")
    
    def test_login_invalid_id(self):
        """Test login with invalid account ID"""
        with self.assertRaises(InvalidAccountError):
            self.bank.login("99999", "1111")
    
    def test_login_invalid_passcode(self):
        """Test login with invalid passcode"""
        with self.assertRaises(InvalidAccountError):
            self.bank.login("10001", "wrong")
    
    def test_delete_account(self):
        """Test deleting an existing account"""
        self.bank.delete_account("10001")
        self.assertNotIn("10001", self.bank.accounts)
    
    def test_delete_nonexistent_account(self):
        """Test deleting a non-existent account"""
        with self.assertRaises(InvalidAccountError):
            self.bank.delete_account("99999")
    
    def test_top_up_mobile_success(self):
        """Test successful mobile top-up"""
        account = self.bank.accounts["10001"]
        result = self.bank.top_up_mobile(account, "17123456", 200)
        self.assertEqual(account.funds, 800)
        self.assertIn("topped up Nu: 200", result)
    
    def test_top_up_mobile_insufficient_funds(self):
        """Test mobile top-up with insufficient funds"""
        account = self.bank.accounts["10001"]
        with self.assertRaises(BankError):
            self.bank.top_up_mobile(account, "17123456", 2000)

class TestEdgeCases(unittest.TestCase):
    """Test edge cases and unusual inputs"""
    
    def setUp(self):
        self.bank = Banking_system("edge_case_accounts.txt")
        self.account = self.bank.create_account("Personal")
    
    def test_deposit_very_large_amount(self):
        """Test depositing an extremely large amount"""
        try:
            result = self.account.deposit(1e20)
            self.assertEqual(self.account.funds, 1e20)
        except Exception as e:
            self.fail(f"Depositing large amount raised unexpected exception: {e}")
    
    def test_withdraw_all_funds(self):
        """Test withdrawing all available funds"""
        self.account.funds = 500
        result = self.account.withdraw(500)
        self.assertEqual(self.account.funds, 0)
        self.assertIn("Withdrew Nu: 500", result)
    
    def test_transfer_all_funds(self):
        """Test transferring all available funds"""
        self.account.funds = 500
        recipient = self.bank.create_account("Business")
        result = self.account.transfer(500, recipient)
        self.assertEqual(self.account.funds, 0)
        self.assertEqual(recipient.funds, 500)
    
    def test_account_id_collision(self):
        """Test handling of potential account ID collisions"""
        # Create 100 accounts to check for ID collisions
        accounts = set()
        for _ in range(100):
            account = self.bank.create_account("Personal")
            self.assertNotIn(account.id, accounts)
            accounts.add(account.id)

if __name__ == "__main__":
    unittest.main()