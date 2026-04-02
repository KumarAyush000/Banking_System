from BankAccount import BankAccount

class SavingsAccount(BankAccount):
    interest_rate = 6

    def apply_iterest(self):
        interest = (self.balance * self.interest_rate) /100
        self.balance += interest
        self._add_transaction("INTEREST_CREDITED", interest)
        print(f"Interest of {interest} applied to {self.account_number}")