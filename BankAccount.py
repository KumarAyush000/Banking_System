import itertools

class BankAccount:
    id_generator = itertools.count(1001)
    _branch_code_generator = itertools.count(1100)
    rate = 5
    min_balance = 1000
    min_balance_fee = 50

    branch_codes = {"city1": "CT1",
                    "city2": "CT2",
                    "city3": "CT3",
                    "city4": "CT4"
                    }
    
    # Store ID as key and name as value
    _account_holders_details = {}

    def __init__(self, owner_name: str, balance: float, city: str):
        self.account_number = f"AC{BankAccount.branch_codes.get(city.lower(), "GEN")}{next(BankAccount.id_generator)}"

        # branch_code generator 
        prefix = BankAccount.branch_codes.get(city.lower(), "GEN") 
        suffix = next(BankAccount._branch_code_generator)
        self.branch_code = f"{prefix}-{suffix}"

        self._owner_name = owner_name
        self._balance = balance
        
        BankAccount._account_holders_details[self.account_number] = self._owner_name

    @property
    def balance(self):
        return self._balance
    
    def _check_min_balance(self):
        if self._balance < BankAccount.min_balance:
            print(f"BEYOND MINIMUM: Applying fee of {BankAccount.min_balance_fee}")
            self._balance -= BankAccount.min_balance_fee

    def withdraw(self, amount: float):
        if amount <= 0:
            print("Invalid amount. Use a positive number.")
            return
        
        if self._balance > amount:
            self.balance -= amount
            print(f"Amount withdrawn: {amount}")
            self._check_min_balance()
        else:
            print("Transaction Denied. Insufficient fund.")
        
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"Deposited: {amount}. New Balance: {self._balance}")
        else:
            print("Deposit amount must be positive.")

    @classmethod
    def bank_account_guidelines(cls):
        print(f"--- Bank Guidelines ---")
        print(f"Rate of interest: {cls.rate}%")
        print(f"Minimum balance required: {cls.min_balance}")
        print(f"Minimum balance fees: {cls.min_balance_fee}")

# Usage
print(BankAccount.bank_account_guidelines())
account1 = BankAccount("John", 1500.00,"city1")
account1.withdraw(600) 
print(BankAccount._account_holders_details)