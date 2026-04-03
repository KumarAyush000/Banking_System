from BankAccount import BankAccount


class CurrentAccount(BankAccount):
    overdraft_limit = 5000

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

        if self._balance + self.overdraft_limit >= amount:
            self._balance -= amount
            self._add_transaction("WITHDRAW", amount)
            print(f"Amount withdrawn: {amount}")
        else:
            print("Transaction Denied. Overdraft limit exceeded.")