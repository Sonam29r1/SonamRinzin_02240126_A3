import random

class Bank_Account():
    def __init__(self,id,passcode,account_category,funds=0):
        self.id = id
        self.passcode = passcode
        self.account_category = account_category
        self.funds = funds
    def deposit(self,amount):
        if amount > 0:
            self.funds += amount
            return f"Deposited Nu: {amount}"
        return "Invalid Amount"
    def withdraw(self,amount):
        if 0 < amount <= self.funds:
            self.funds -= amount
        return "Insufficient Amount"
    def transfer(self, amount, receipient_account):
        withdrawal_message = self.withdraw(amount)
        if withdrawal_message == "Withdrawal Completed ":
            receipient_account.deposit(amount)
            return "Succesfully Transferred"
        return withdrawal_message

class Personal_account(Bank_Account):
    def __init__(self, id, passcode, account_category, funds=0):
        super().__init__(id, passcode, account_category, funds)

class Business_account(Bank_Account):
    def __init__(self, id, passcode, account_category, funds=0):
        super().__init__(id, passcode, account_category, funds)

class Banking_system:
    def __init__(self,filename="accounts.txt"):
        self.filename = filename
        self.accoints = self.load_accounts()

    def load_accounts(self):
        accounts = {}
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    id, passcode, account_category, funds = line.strip().split(",")
                    funds = float(funds)
                    if account_category == "Personal":
                        account = Personal_account(id, passcode, funds)
                    else:
                        account = Business_account(id, passcode, funds)
                    accounts[id] = account
        except FileNotFoundError:
            pass
        return accounts
    
    def save_accounts(self):
        with open(self.filename, "w") as file:
            for account in self.accounts.values():
                file.write("account.account_id), (account.passcode), (account.account_category), (account.funds)\n")

    def create_account(self, account_type):
        id = str(random.randint(10000, 99999))
        passcode = str(random.randint(1000, 9999))
        if account_type == "Personal": 
            account = Personal_account(id, passcode) 
        else: 
            account = Business_account(id, passcode) 
        self.accounts[id] = account 
        self.save_accounts()
        return account
    def login(self, id, passcode):
        account = self.accounts.get(id) 
        if account and account.passcode == passcode: 
            return account
        raise ValueError("Account number or password is not recognized")
        
    def delete_account(self,id):
        if id in self.accounts:
            del self.accounts[id]
            self.save_accounts()
        else:
            raise ValueError("Account does not exist")
        
def main():
    bank = Banking_system()
    while True:
        print("\nHello, How can i assist you?\n1. Open Account\n2. Login to your Account\n3. Exit") 
        choice = input("Enter your choice:")
        if choice == "1":
            account_type = input("Select account type (1 for Personal, 2 for Business): ")
            if account_type == "1":
                account = bank.create_account("Personal")
            elif account_type == "2":
                account = bank.create_account("Business")
            else:
                print("Unsupported account type")
                continue
            print("Account created. Account id: (account.account id), Passcode: (account.passcode)")
        elif choice == "2":
            account_id = input("Enter your account id: ") 
            passcode = input("Enter your passcode: ")
            try:
                account = bank.login(account_id, passcode)
                while True:
                    print("\n1. Check funds\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Delete Account\n6. Logout")
                    action = input("Enter your choice: ")
                    if action == "1":
                        print(f"Your funds is {account.funds}")

                    elif action == "2":
                        amount = float(input("Please input the deposit amount: "))
                        print(account.deposit(amount))
                        bank.save_accounts()
                    elif action == "3":
                        amount = float(input("Please input the withdrawal amount: "))
                        print(account.withdraw(amount))
                        bank.save_accounts()
                    elif action == "4":
                        recipient_id = input("Enter recipient account id: ")
                        amount = float(input("Enter amount to transfer: "))
                        try:
                            recipient_account = bank.accounts[recipient_id]
                            print(account.transfer (amount, recipient_account))
                            bank.save_accounts()
                        except KeyError:
                            print("Recipient account does not exist.")
                    elif action == "5":
                        bank.delete_account(account_id)
                        print("Account deletion successful")
                        break
                    elif action == "6":
                        break
                    else:
                        print("Please select a valid option.")
            except ValueError as e:
                print(e)
        elif choice == "3":
            break
        else:
            print("Please select a valid option..")

if __name__ == "__main__":
    main()


        