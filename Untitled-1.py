# import random
# class Bank_Account():
#     def __init__(self,id,passcode,account_category,funds=0):
#         self.id = id
#         self.passcode = passcode
#         self.account_category = account_category
#         self.funds = funds
#     def deposit(self,amount):
#         if amount > 0:
#             self.funds += amount
#             return f"Deposited Nu: {amount}"
#         return "Invalid Amount"
#     def withdraw(self,amount):
#         if 0 < amount <= self.funds:
#             self.funds -= amount
#         return "Insufficient Amount"
#     def transfer(self, amount, receipient_account):
#         withdrawal_message = self.withdraw(amount)
#         if withdrawal_message == "Withdrawal Completed ":
#             receipient_account.deposit(amount)
#             return "Succesfully Transferred"
#         return withdrawal_message

# class Personal_account(Bank_Account):
#     def __init__(self, id, passcode, account_category, funds=0):
#         super().__init__(id, passcode, account_category, funds)

# class Business_account(Bank_Account):
#     def __init__(self, id, passcode, account_category, funds=0):
#         super().__init__(id, passcode, account_category, funds)

# class Banking_system:
#     def __init__(self,filename="accounts.txt"):
#         self.filename = filename
#         self.accoints = self.load_accounts()

#     def load_accounts(self):
#         accounts = {}
#         try:
#             with open(self.filename, "r") as file:
#                 for line in file:
#                     id, passcode, account_category, funds = line.strip().split(",")
#                     funds = float(funds)
#                     if account_category == "Personal":
#                         account = Personal_account(id, passcode, funds)
#                     else:
#                         account = Business_account(id, passcode, funds)
#                     accounts[id] = account
#         except FileNotFoundError:
#             pass
#         return accounts
    
#     def save_accounts(self):
#         with open(self.filename, "w") as file:
#             for account in self.accounts.values():
#                 file.write("account.account_id), (account.passcode), (account.account_category), (account.funds)\n")

#     def create_account(self, account_type):
#         id = str(random.randint(10000, 99999))
#         passcode = str(random.randint(1000, 9999))
#         if account_type == "Personal": 
#             account = Personal_account(id, passcode) 
#         else: 
#             account = Business_account(id, passcode) 
#         self.accounts[id] = account 
#         self.save_accounts()
#         return account
#     def login(self, id, passcode):
#         account = self.accounts.get(id) 
#         if account and account.passcode == passcode: 
#             return account
#         raise ValueError("Account number or password is not recognized")
        
#     def delete_account(self,id):
#         if id in self.accounts:
#             del self.accounts[id]
#             self.save_accounts()
#         else:
#             raise ValueError("Account does not exist")
        
# def main():
#     bank = Banking_system()
#     while True:
#         print("\nHello, How can i assist you?\n1. Open Account\n2. Login to your Account\n3. Exit") 
#         choice = input("Enter your choice:")
#         if choice == "1":
#             account_type = input("Select account type (1 for Personal, 2 for Business): ")
#             if account_type == "1":
#                 account = bank.create_account("Personal")
#             elif account_type == "2":
#                 account = bank.create_account("Business")
#             else:
#                 print("Unsupported account type")
#                 continue
#             print(f"Account created. Account id: {account.account_id}, Passcode: {account.passcode}")
#         elif choice == "2":
#             account_id = input("Enter your account id: ") 
#             passcode = input("Enter your passcode: ")
#             try:
#                 account = bank.login(account_id, passcode)
#                 while True:
#                     print("\n1. Check funds\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Delete Account\n6. Logout")
#                     action = input("Enter your choice: ")
#                     if action == "1":
#                         print(f"Your funds is {account.funds}")

#                     elif action == "2":
#                         amount = float(input("Please input the deposit amount: "))
#                         print(account.deposit(amount))
#                         bank.save_accounts()
#                     elif action == "3":
#                         amount = float(input("Please input the withdrawal amount: "))
#                         print(account.withdraw(amount))
#                         bank.save_accounts()
#                     elif action == "4":
#                         recipient_id = input("Enter recipient account id: ")
#                         amount = float(input("Enter amount to transfer: "))
#                         try:
#                             recipient_account = bank.accounts[recipient_id]
#                             print(account.transfer (amount, recipient_account))
#                             bank.save_accounts()
#                         except KeyError:
#                             print("Recipient account does not exist.")
#                     elif action == "5":
#                         bank.delete_account(account_id)
#                         print("Account deletion successful")
#                         break
#                     elif action == "6":
#                         break
#                     else:
#                         print("Please select a valid option.")
#             except ValueError as e:
#                 print(e)
#         elif choice == "3":
#             break
#         else:
#             print("Please select a valid option..")

# if __name__ == "__main__":
#     main()

'''
Beginning part A implementation
'''

import random
import tkinter as tk
from tkinter import messagebox, simpledialog

class BankError(Exception):
    """exception class for banking errors"""
    pass

class InvalidAmountError(BankError):
    """Raised when an invalid amount is entered"""
    pass

class InsufficientFundsError(BankError):
    """Raised when there are insufficient funds for a transaction"""
    pass

class InvalidAccountError(BankError):
    """Raised when an invalid account is referenced"""
    pass

class Bank_Account():
    """class representing a bank account which performs few basic operations"""
    def __init__(self, id, passcode, account_category, funds=0):
        """
        Initialize a bank account with following parameter:
        """
        self.id = id
        self.passcode = passcode
        self.account_category = account_category
        self.funds = funds
    
    def deposit(self, amount):
        """
        Deposit money into the account
        Aeguments:
            amount: amount to be deposited
        returns:
            str: showing amount of deposition and new balance
        Raises error:
            InvalidAmountError: If amount is not positive
        """
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")
        self.funds += amount
        return f"Deposited Nu: {amount}. New balance: Nu: {self.funds}"
    
    def withdraw(self, amount):

        """
        Withdraw money from the account    
        arguments:
            amount: amount to be withdrawn
        return:
            str: showing amount withdrawn and new balance
        Raises:
            InvalidAmountError: If amount is not positive
            InsufficientFundsError: If account has insufficient funds
        """

        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        if amount > self.funds:
            raise InsufficientFundsError("Insufficient funds for withdrawal")
        self.funds -= amount
        return f"Withdrew Nu: {amount}. New balance: Nu: {self.funds}"
    
    def transfer(self, amount, recipient_account):
        """
        Transfer money to another account
        argument:
            amount: amount to be transfereed
            recipient_account: amount recipient
        return:
            str: shows amount trasferred and the recipient acc's id
        Raises:
            BankError: For any transfer related errors
        """
        try:
            withdrawal_msg = self.withdraw(amount)
            recipient_account.deposit(amount)
            return f"Successfully transferred Nu: {amount} to account {recipient_account.id}"
        except BankError as e:
            raise BankError(f"Transfer failed: {str(e)}")

class Personal_account(Bank_Account):
    """Class representing a personal bank account"""
    def __init__(self, id, passcode, account_category="Personal", funds=0):
        super().__init__(id, passcode, account_category, funds) #Using super() beacuase it is safer if the parent class name changes later.

class Business_account(Bank_Account):
    """Class representing a business bank account"""
    def __init__(self, id, passcode, account_category="Business", funds=0):
        super().__init__(id, passcode, account_category, funds) #Using super() beacuase it is safer if the parent class name changes later.
        
class Banking_system:
    """Class representing the banking system with account management"""
    def __init__(self, filename="accounts.txt"):
        """
        Initialize the banking system
        Args:
            filename (str, optional): File to store accounts. Defaults to "accounts.txt".
        """
        self.filename = filename
        self.accounts = self.load_accounts()
    
    def load_accounts(self):
        """
        Load accounts from file
        
        Returns:
            dict: Dictionary of loaded accounts
            used dictionary because it has time complexity average O(1) for lookups
        """
        accounts = {}
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    try:
                        id, passcode, account_category, funds = line.strip().split(",")
                        funds = float(funds)
                        if account_category == "Personal":
                            account = Personal_account(id, passcode, account_category, funds)
                        else:
                            account = Business_account(id, passcode, account_category, funds)
                        accounts[id] = account
                    except ValueError:
                        continue 
        except FileNotFoundError:
            pass
        return accounts
    
    def save_accounts(self):
        """Save all accounts to file"""
        with open(self.filename, "w") as file:
            for account in self.accounts.values():
                file.write(f"{account.id},{account.passcode},{account.account_category},{account.funds}\n")
    
    def create_account(self, account_type):
        """
        Create a new account
        Returns:
            Bank_Account: The created account object
        Raises:
            ValueError: If account type is invalid
        """
        id = str(random.randint(10000, 99999))
        passcode = str(random.randint(1000, 9999))
        if account_type == "Personal":
            account = Personal_account(id, passcode)
        elif account_type == "Business":
            account = Business_account(id, passcode)
        else:
            raise ValueError("Invalid account type")
        self.accounts[id] = account
        self.save_accounts()
        return account
    
    def login(self, id, passcode):
        """
        Login to an account
        
        Arguments to be passed:
            id: Account ID
            passcode: Account passcode
            
        Returns:
            Bank_Account: The logged in account object
            
        Raises:
            InvalidAccountError: If credentials are invalid
        """
        account = self.accounts.get(id)
        if not account or account.passcode != passcode:
            raise InvalidAccountError("Invalid account ID or passcode")
        return account
    
    def delete_account(self, id):
        """
        Delete an account
        
        Args:
            id (str): Account ID to delete
            
        Raises:
            InvalidAccountError: If account doesn't exist
        """
        if id not in self.accounts:
            raise InvalidAccountError("Account does not exist")
        del self.accounts[id]
        self.save_accounts()
    
    def top_up_mobile(self, account, phone_number, amount):
        """
        Top up a mobile phone balance from bank account
        We can use withdraw function instead of creating new one

        Arguments:
            account (Bank_Account): Account to deduct from
            phone_number (str): Phone number to top up
            amount (float): Amount to top up
            
        Returns:
            str: Confirmation message
            
        Raises:
            BankError: For any transaction errors
        """
        try:
            account.withdraw(amount)
            return f"Successfully topped up Nu: {amount} to phone {phone_number}"
        except BankError as e:
            raise BankError(f"Mobile top-up failed: {str(e)}")
        

#Gui implementation
class BankingGUI:
    """Class providing a graphical user interface for the banking system"""
    def __init__(self, banking_system):
        """
        Initialize the banking GUI
        
        Args:
            banking_system (Banking_system): The banking system instance
        """
        self.bank = banking_system
        self.current_account = None
        
        self.root = tk.Tk()
        self.root.title("Banking System")
        self.root.geometry("400x300")
        
        self.create_main_menu()
    
    def create_main_menu(self):
        """Create the main menu interface"""
        self.clear_window()
        
        tk.Label(self.root, text="Banking System", font=("Arial", 16)).pack(pady=10)
        
        tk.Button(self.root, text="1. Open Account", command=self.open_account).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self.root, text="2. Login", command=self.login).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self.root, text="3. Exit", command=self.root.quit).pack(fill=tk.X, padx=50, pady=5)
    
    def create_account_menu(self):
        """Create the account operations menu"""
        self.clear_window()
        
        tk.Label(self.root, text=f"Account {self.current_account.id}", font=("Arial", 14)).pack(pady=10)
        
        tk.Button(self.root, text="1. Check Balance", command=self.check_balance).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self.root, text="2. Deposit", command=self.deposit).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self.root, text="3. Withdraw", command=self.withdraw).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self.root, text="4. Transfer", command=self.transfer).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self.root, text="5. Mobile Top-up", command=self.mobile_topup).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self.root, text="6. Delete Account", command=self.delete_account).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self.root, text="7. Logout", command=self.logout).pack(fill=tk.X, padx=50, pady=5)
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def open_account(self):
        """Handle account opening"""
        account_type = simpledialog.askstring("Account Type", "Enter account type (1 for Personal, 2 for Business):")
        try:
            if account_type == "1":
                account = self.bank.create_account("Personal")
            elif account_type == "2":
                account = self.bank.create_account("Business")
            else:
                messagebox.showerror("Error", "Invalid account type")
                return
            
            messagebox.showinfo("Account Created", 
                              f"Account created successfully!\nAccount ID: {account.id}\nPasscode: {account.passcode}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def login(self):
        """Handle user login"""
        account_id = simpledialog.askstring("Login", "Enter your account ID:")
        passcode = simpledialog.askstring("Login", "Enter your passcode:", show="*")
        
        try:
            self.current_account = self.bank.login(account_id, passcode)
            self.create_account_menu()
        except BankError as e:
            messagebox.showerror("Login Failed", str(e))
    
    def check_balance(self):
        """Display account balance"""
        messagebox.showinfo("Account Balance", f"Your current balance is Nu: {self.current_account.funds}")
    
    def deposit(self):
        """Handle deposit operation"""
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        try:
            if amount is not None:
                result = self.current_account.deposit(amount)
                self.bank.save_accounts()
                messagebox.showinfo("Deposit", result)
        except BankError as e:
            messagebox.showerror("Deposit Error", str(e))
    
    def withdraw(self):
        """Handle withdrawal operation"""
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        try:
            if amount is not None:
                result = self.current_account.withdraw(amount)
                self.bank.save_accounts()
                messagebox.showinfo("Withdrawal", result)
        except BankError as e:
            messagebox.showerror("Withdrawal Error", str(e))
    
    def transfer(self):
        """Handle transfer operation"""
        recipient_id = simpledialog.askstring("Transfer", "Enter recipient account ID:")
        amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:")
        
        try:
            if recipient_id and amount is not None:
                recipient = self.bank.accounts.get(recipient_id)
                if not recipient:
                    raise InvalidAccountError("Recipient account not found")
                result = self.current_account.transfer(amount, recipient)
                self.bank.save_accounts()
                messagebox.showinfo("Transfer", result)
        except BankError as e:
            messagebox.showerror("Transfer Error", str(e))
    
    def mobile_topup(self):
        """Handle mobile top-up operation"""
        phone_number = simpledialog.askstring("Mobile Top-up", "Enter phone number:")
        amount = simpledialog.askfloat("Mobile Top-up", "Enter amount to top up:")
        
        try:
            if phone_number and amount is not None:
                result = self.bank.top_up_mobile(self.current_account, phone_number, amount)
                self.bank.save_accounts()
                messagebox.showinfo("Mobile Top-up", result)
        except BankError as e:
            messagebox.showerror("Top-up Error", str(e))
    
    def delete_account(self):
        """Handle account deletion"""
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this account?")
        if confirm:
            try:
                self.bank.delete_account(self.current_account.id)
                messagebox.showinfo("Account Deleted", "Your account has been deleted successfully")
                self.current_account = None
                self.create_main_menu()
            except BankError as e:
                messagebox.showerror("Deletion Error", str(e))
    
    def logout(self):
        """Handle user logout"""
        self.current_account = None
        self.create_main_menu()
    
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()

def main():
    """Main function to run the banking system"""
    bank = Banking_system()
    
    gui = BankingGUI(bank)
    gui.run()
