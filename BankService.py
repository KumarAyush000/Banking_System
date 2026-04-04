from SavingsAccount import SavingsAccount
from CurrentAccount import CurrentAccount


class BankService:
    def __init__(self):
        self.accounts = {}

    def create_account(self, owner_name: str, balance: float, city: str, pin: str, account_type: str):
        if account_type.lower() == "savings":
            account = SavingsAccount(owner_name, balance, city, pin)
        elif account_type.lower() == "current":
            account = CurrentAccount(owner_name, balance, city, pin)
        else:
            print("Invalid account type. Choose either 'savings' or 'current'.")
            return None

        self.accounts[account.account_number] = account
        print(f"Account created successfully! Account Number: {account.account_number}")
        return account

    def find_account(self, account_number: str):
        account = self.accounts.get(account_number)
        if not account:
            print("Account not found.")
        return account

    def show_all_accounts(self):
        if not self.accounts:
            print("No accounts available.")
            return

        print("\n--- All Bank Accounts ---")
        for acc_no, account in self.accounts.items():
            print(f"{acc_no} | {account.owner_name} | Balance: {account.balance}")

    def total_accounts(self):
        return len(self.accounts)