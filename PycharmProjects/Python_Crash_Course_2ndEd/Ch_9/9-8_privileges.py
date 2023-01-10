
"""
9-7. Admin: An administrator is a special kind of user. Write a class called
    Admin that inherits from the User class you wrote in Exercise 9-3 (page 162)
    or Exercise 9-5 (page 167). Add an attribute, privileges, that stores a list
    of strings like "can add post", "can delete post", "can ban user", and so
    on. Write a method called show_privileges() that lists the administrator’s
    set of privileges. Create an instance of Admin, and call your method.
"""

""" DOES NOT WORK. NO CLUE WHY"""

class User():
    """Represent a simple user profile."""

    def __init__(self, first_name, last_name, username, email, location):
        """Initialize the user."""
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.username = username
        self.email = email
        self.location = location.title()
        self.login_attempts = 0

    def describe_user(self):
        """Display a summary of the user's information."""
        print(f"\n{self.first_name} {self.last_name}")
        print(f"  Username: {self.username}")
        print(f"  Email: {self.email}")
        print(f"  Location: {self.location}")

    def greet_user(self):
        """Display a personalized greeting to the user."""
        print(f"\nWelcome back, {self.username}!")

    def increment_login_attempts(self):
        """Increment the value of login_attempts."""
        self.login_attempts += 1

    def reset_login_attempts(self):
        """Reset login_attempts to 0."""
        self.login_attempts = 0

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


jonathan = Admin('Jonathan', 'Baldwin', 'boneless3vil', 'jon@sinoverpi.com',
                 'Canyon Lake')
jonathan.describe_user()

jonathan.privileges.show_privileges()

print("\nAdding privileges...")
jonathan.privileges = ['can add post',
                       'can delete post',
                       'can ban user'
                       ]

jonathan_privileges = jonathan.privileges.privileges
jonathan.privileges.show_privileges()























