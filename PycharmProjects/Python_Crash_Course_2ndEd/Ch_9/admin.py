
from user import User


class Admin(User):
    """ administrator privileges class"""

    def __init__(self, first_name, last_name, username, email, location):
        super().__init__(first_name, last_name, username, email, location)

        """ initialize Privileges """
        self.privileges = Privileges()


class Privileges():
    """ class for privileges, child of Admin"""

    def __init__(self, privileges=[]):
        self.privileges = privileges

    def show_privileges(self):
        """stores administrator privileges"""
        print("List of user privileges:")
        if self.privileges:
            for privilege in self.privileges:
                print(f"– {privilege}")
        else:
            print("User has no privileges.")