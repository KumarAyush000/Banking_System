import itertools
from datetime import datetime


class BankAccount:
    id_generator = itertools.count(1001)
    _branch_code_generator = itertools.count(1100)

    rate = 5
    min_balance = 1000
    min_balance_fee = 50

    branch_codes = {
        "city1": "CT1",
        "city2": "CT2",
        "city3": "CT3",
        "city4": "CT4"
    }

    _account_holders_details = {}

    def __init__(self, owner_name: str, balance: float, city: str, pin: str):
        self.account_number = self._generate_account_number(city)
        self.branch_code = self._generate_branch_code(city)

        self._owner_name = owner_name
        self._balance = balance
        self.city = city
        self._pin = pin
        self.is_active = True
        self.transactions = []

        BankAccount._account_holders_details[self.account_number] = self._owner_name

        self._add_transaction("ACCOUNT_CREATED", balance)

    @classmethod
    def _generate_account_number(cls, city: str):
        prefix = cls.branch_codes.get(city.lower(), "GEN")
        return f"AC{prefix}{next(cls.id_generator)}"

    @classmethod
    def _generate_branch_code(cls, city: str):
        prefix = cls.branch_codes.get(city.lower(), "GEN")
        suffix = next(cls._branch_code_generator)
        return f"{prefix}-{suffix}"

    @property
    def balance(self):
        return self._balance

    @property
    def owner_name(self):
        return self._owner_name

    def verify_pin(self, pin: str):
        return self._pin == pin

    def _add_transaction(self, txn_type: str, amount: float):
        self.transactions.append({
            "type": txn_type,
            "amount": amount,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance_after": self._balance
        })

    def _check_min_balance(self):
        if self._balance < BankAccount.min_balance:
            print(f"BELOW MINIMUM BALANCE: Applying fee of {BankAccount.min_balance_fee}")
            self._balance -= BankAccount.min_balance_fee
            self._add_transaction("MIN_BALANCE_FEE", BankAccount.min_balance_fee)

    def deposit(self, amount: float):
        if not self.is_active:
            print("Account is inactive.")
            return

        if amount <= 0:
            print("Deposit amount must be positive.")
            return

        self._balance += amount
        self._add_transaction("DEPOSIT", amount)
        print(f"Deposited: {amount}. New Balance: {self._balance}")

    def withdraw(self, amount: float, pin: str):
        if not self.is_active:
            print("Account is inactive.")
            return

        if not self.verify_pin(pin):
            print("Invalid PIN.")
            return

        if amount <= 0:
            print("Invalid amount. Use a positive number.")
            return

        if self._balance >= amount:
            self._balance -= amount
            self._add_transaction("WITHDRAW", amount)
            print(f"Amount withdrawn: {amount}")
            self._check_min_balance()
        else:
            print("Transaction Denied. Insufficient funds.")

    def transfer(self, target_account, amount: float, pin: str):
        if not self.is_active or not target_account.is_active:
            print("One of the accounts is inactive.")
            return

        if not self.verify_pin(pin):
            print("Invalid PIN.")
            return

        if amount <= 0:
            print("Transfer amount must be positive.")
            return

        if self._balance >= amount:
            self._balance -= amount
            target_account._balance += amount

            self._add_transaction("TRANSFER_SENT", amount)
            target_account._add_transaction("TRANSFER_RECEIVED", amount)

            print(f"Transferred {amount} to {target_account.account_number}")
            self._check_min_balance()
        else:
            print("Insufficient funds for transfer.")

    def show_transaction_history(self):
        print(f"\n--- Transaction History for {self.account_number} ---")
        for txn in self.transactions:
            print(txn)

    def display_account_info(self):
        print("\n--- Account Details ---")
        print(f"Owner Name     : {self._owner_name}")
        print(f"Account Number : {self.account_number}")
        print(f"Branch Code    : {self.branch_code}")
        print(f"City           : {self.city}")
        print(f"Balance        : {self._balance}")
        print(f"Status         : {'Active' if self.is_active else 'Inactive'}")

    def deactivate_account(self):
        self.is_active = False
        print(f"Account {self.account_number} deactivated.")

    def activate_account(self):
        self.is_active = True
        print(f"Account {self.account_number} activated.")

    @classmethod
    def bank_account_guidelines(cls):
        print(f"\n--- Bank Guidelines ---")
        print(f"Rate of interest       : {cls.rate}%")
        print(f"Minimum balance        : {cls.min_balance}")
        print(f"Minimum balance fee    : {cls.min_balance_fee}")