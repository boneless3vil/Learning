
"""
9-7. Admin: An administrator is a special kind of user. Write a class called
    Admin that inherits from the User class you wrote in Exercise 9-3 (page 162)
    or Exercise 9-5 (page 167). Add an attribute, privileges, that stores a list
    of strings like "can add post", "can delete post", "can ban user", and so
    on. Write a method called show_privileges() that lists the administrator’s
    set of privileges. Create an instance of Admin, and call your method.
"""

class User:
    """ first_name and last_name, plus additional attributes"""
    def __init__(self, first_name, last_name, email, address, phone):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email
        self.address = address
        self.phone = phone
        self.login_attempts = 0

    def describe_user(self):
#        name = f"{self.first_name} {self.last_name}"
        msg = f"Name: {self.first_name} {self.last_name}\n" \
              f"Email: {self.email}\n" \
              f"Address: {self.address}\n" \
              f"Phone: {self.phone}"
        print(msg)

    def greet_user(self):
        print(f"\nWelcome back, {self.first_name}\n")

    def total_login_attempts(self, login_attempts):
        self.login_attempts = login_attempts

    def increment_login_attempts(self):
        self.login_attempts += 1

    def reset_login_attempts(self):
        self.login_attempts = 0

class Admin(User):
    """ administrator privileges class"""
    def __init__(self, first_name, last_name, username, email, location):
        super().__init__(first_name, last_name, username, email, location)
        self.privileges = []


    def show_privileges(self):
        """stores administrator privileges"""
        print("List of administrator privileges: ")
        for privilege in self.privileges:
            print(f"– {privilege}")


jonathan = Admin('Jonathan', 'Baldwin', 'boneless3vil', 'jon@sinoverpi.com', 'Canyon Lake')
jonathan.describe_user()

jonathan.greet_user()

jonathan.privileges = ['can add post', 'can delete post', 'can ban user']
jonathan.show_privileges()
































































































