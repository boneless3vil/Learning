

class Employee:
    """ store employee information"""

    def __init__(self, f_name, l_name, salary):
        self.first = f_name.title()
        self.last = l_name.title()
        self.salary = salary

    def give_raise(self, amount=5_000):
        self.salary += amount

Employee('jonathan', 'baldwin', '50000')
