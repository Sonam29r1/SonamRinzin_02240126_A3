
'''
Beginning part A implementation
'''

import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog

class BankError(Exception):
    pass

class InvalidAmountError(BankError):
    pass

class InsufficientFundsError(BankError):
    pass

class InvalidAccountError(BankError):
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
        

#Separate userinput processer
class BankingController:
    """Handles all user input processing"""
    def __init__(self, banking_system):
        self.bank = banking_system
        self.current_account = None

    def processUserInput(self, choice, is_main_menu=True):
        """
        Processes all user input from both menus
        Arguments:
            choice: The user's menu or function choice
            is_main_menu: processing of main menu input
        Returns:
            str: Result message for successful operations
        """
        if is_main_menu:
            return self._process_main_menu(choice)
        else:
            return self._process_account_menu(choice)

    def _process_main_menu(self, choice):
        """Process main menu choices"""
        if choice == "1":
            return self._create_account()
        elif choice == "2":
            return self._login()
        elif choice == "3":
            return "exit"
        raise ValueError("Invalid main menu choice")

    def _process_account_menu(self, choice):
        """Process account menu choices"""
        if not self.current_account:
            raise BankError("No account logged in")

        if choice == "1":  # Balance check function
            return f"Current balance: Nu: {self.current_account.funds}"
        
        elif choice == "2":  # Deposit function
            amount = float(simpledialog.askstring("Deposit", "Enter amount:"))
            return self.current_account.deposit(amount)
        
        elif choice == "3":  # Withdraw function
            amount = float(simpledialog.askstring("Withdraw", "Enter amount:"))
            return self.current_account.withdraw(amount)
        
        elif choice == "4":  # Transfer function
            recipient_id = simpledialog.askstring("Transfer", "Recipient account ID:")
            amount = float(simpledialog.askstring("Transfer", "Enter amount:"))
            recipient = self.bank.accounts.get(recipient_id)
            if not recipient:
                raise BankError("Recipient account not found")
            return self.current_account.transfer(amount, recipient)
        
        elif choice == "5":  # Mobile top-up function
            phone = simpledialog.askstring("Mobile Top-up", "Phone number:")
            amount = float(simpledialog.askstring("Mobile Top-up", "Amount:"))
            return self.bank.top_up_mobile(self.current_account, phone, amount)
        
        elif choice == "6":  # Delete account function
            confirm = messagebox.askyesno("Confirm", "Permanently delete this account?")
            if confirm:
                self.bank.delete_account(self.current_account.id)
                self.current_account = None
                return "Account deleted successfully"
            return "Account deletion cancelled"
        
        elif choice == "7":  # Logout function
            self.current_account = None
            return "logout"
        raise ValueError("Invalid account menu choice")

    def _create_account(self):
        """Handle account creation"""
        acc_type = simpledialog.askstring("Account Type", "1 for Personal, 2 for Business:")
        if acc_type not in ("1", "2"):
            raise ValueError("Invalid account type")
        
        account = self.bank.create_account("Personal" if acc_type == "1" else "Business")
        return (f"Account created successfully!\n"
                f"Account ID: {account.id}\n"
                f"Passcode: {account.passcode}")

    def _login(self):
        """Handle user login"""
        account_id = simpledialog.askstring("Login", "Enter account ID:")
        passcode = simpledialog.askstring("Login", "Enter passcode:", show="*")
        self.current_account = self.bank.login(account_id, passcode)
        return f"Welcome, {account_id}"

# GUI Interface

class BankingGUI:
    """GUI"""
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Bhutanese Banking System")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f8ff")  # Light blue background
        
        #Font configurations
        self.header_font = ("Helvetica", 18, "bold")
        self.button_font = ("Helvetica", 11)
        self.label_font = ("Helvetica", 12)
        
        #Coloring of background, button, text
        self.bg_color = "#f0f8ff"
        self.button_bg = "#cce0ff"
        self.button_active_bg = "#2e5cb8"
        self.text_color = "black"
        self.header_color = "#2e5cb8"
        
        self.setup_main_menu()

    def setup_main_menu(self):
        """Main menu"""
        self.clear_window()
        
        # Header 
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(pady=20)
        
        tk.Label(header_frame, 
                text="Druk Banking",
                font=self.header_font,
                fg=self.header_color,
                bg=self.bg_color).pack()
        
        tk.Label(header_frame,
                text="Your Trusted Financial Partner",
                font=self.label_font,
                bg=self.bg_color).pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(expand=True, fill=tk.BOTH, padx=30)
        
        # Menu buttons
        buttons = [
            ("📝 1. Create Account", self.handle_create_account),
            ("🔑 2. Login", self.handle_login),
            ("🚪 3. Exit", self.root.quit)
        ]
        
        for text, command in buttons:
            btn = tk.Button(button_frame,
                          text=text,
                          font=self.button_font,
                          bg=self.button_bg,
                          fg=self.text_color,
                          activebackground=self.button_active_bg,
                          activeforeground="white",
                          relief=tk.RAISED,
                          borderwidth=2,
                          command=command)
            btn.pack(fill=tk.X, pady=5, ipady=8)
        
        # Footer
        tk.Label(self.root,
                text="© 2023 Bhutanese Bank",
                font=("Helvetica", 9),
                bg=self.bg_color).pack(side=tk.BOTTOM, pady=20)

    def setup_account_menu(self):
        """Account menu with standard tkinter styling"""
        self.clear_window()
        
        # Header frame
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(pady=20)
        
        tk.Label(header_frame,
                text=f"Account: {self.controller.current_account.id}",
                font=self.header_font,
                fg=self.header_color,
                bg=self.bg_color).pack()
        
        tk.Label(header_frame,
                text=f"Balance: Nu: {self.controller.current_account.funds:.2f}",
                font=("Helvetica", 14, "bold"),
                bg=self.bg_color).pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(expand=True, fill=tk.BOTH, padx=30)
        
        # Operation buttons
        operations = [
            ("💵 1. Check Balance", self.handle_check_balance),
            ("💰 2. Deposit", self.handle_deposit),
            ("💸 3. Withdraw", self.handle_withdraw),
            ("🔄 4. Transfer", self.handle_transfer),
            ("📱 5. Mobile Top-up", self.handle_topup),
            ("❌ 6. Delete Account", self.handle_delete_account),
            ("👋 7. Logout", self.handle_logout)
        ]
        
        for text, command in operations:
            btn = tk.Button(button_frame,
                          text=text,
                          font=self.button_font,
                          bg=self.button_bg,
                          fg=self.text_color,
                          activebackground=self.button_active_bg,
                          activeforeground="white",
                          relief=tk.RAISED,
                          borderwidth=2,
                          command=command)
            btn.pack(fill=tk.X, pady=5, ipady=6)

    def create_dialog(self, title, prompt):
        return simpledialog.askstring(title, prompt, parent=self.root)

    def clear_window(self):
        """Clear all widgets"""
        for widget in self.root.winfo_children():
            widget.destroy()

    # basic process handler

    def handle_create_account(self):
        self._handle_main_choice("1")

    def handle_login(self):
        self._handle_main_choice("2")

    def handle_check_balance(self):
        self._handle_account_choice("1")

    def handle_deposit(self):
        self._handle_account_choice("2")

    def handle_withdraw(self):
        self._handle_account_choice("3")

    def handle_transfer(self):
        self._handle_account_choice("4")

    def handle_topup(self):
        self._handle_account_choice("5")

    def handle_delete_account(self):
        self._handle_account_choice("6")

    def handle_logout(self):
        self._handle_account_choice("7")
        
    def _handle_main_choice(self, choice):
        """Process main menu selections"""
        try:
            result = self.controller.processUserInput(choice, is_main_menu=True)
            if result == "exit":
                self.root.quit()
            else:
                messagebox.showinfo("Success", result)
                if choice == "2":  # After successful login
                    self.setup_account_menu()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _handle_account_choice(self, choice):
        """Process account menu selections"""
        try:
            result = self.controller.processUserInput(choice, is_main_menu=False)
            if result == "logout":
                self.setup_main_menu()
            else:
                messagebox.showinfo("Success", result)
                self.controller.bank.save_accounts()
                if choice == "6":  # After account deletion
                    self.setup_main_menu()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _clear_window(self):
        """Remove all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        """Center and run the application"""
        self.root.eval('tk::PlaceWindow . center')
        self.root.mainloop()

if __name__ == "__main__":
    bank_system = Banking_system()
    controller = BankingController(bank_system)
    app = BankingGUI(controller)
    app.run()