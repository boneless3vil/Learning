

# MAKING AN INSTANCE FROM A CLASS
# page 160,

class Dog:  # names of classes are capitalized
    """ A simple attempt to model a dog."""

    def __init__(self, name, age):
        """Initialize name and age attributes."""
        self.name = name    # self.parameter = variable
        self.age = age
    def sit(self):
        """Simulate a dog sitting in response to a command."""
        print(f"{self.name} is now sitting.")
    def roll_over(self):
        """ Simulate rolling over in response to a command."""
        print(f"{self.name} rolled over!")

# assessing attributes
my_dog = Dog('Willie', 6)
# calling methods
my_dog.sit()    # instance.method() call
my_dog.roll_over()  # another instance.method() call

print(f"My dog's name is {my_dog.name}.")
print(f"My dog is {my_dog.age} years old.")

# 9-1
# Creating MULTIPLE INSTANCES
class Restaurant:
    """ a class that takes a restaurant name and cuisine type then prints it
     out"""
    def __init__(self, name, cuisine_type):
        self.name = name.title()
        self.cuisine_type = cuisine_type

    def describe_restaurant(self):
        """Describes restaurant name and type of cuisine."""
        msg = f"{self.name} serves wonderful {self.cuisine_type}"
        print(f"\n{msg}")

    def open_restaurant(self):
        """Method that prints a message indicating the restaurant is open"""
        msg = f"\n{self.name} is open!"
        print(msg)


# making instance called restaurant
restaurant = Restaurant('Rosetta Coffee Brewing Co.', 'coffee')
print(restaurant.name)
print(restaurant.cuisine_type)

# - - - - - - - - - - - - - - - - - - - - - - - - -

# 9-2 Three restaurants, ONLY: describe_restaurant function in class Restaurant
class Restaurant:
    """ expanding on 9-1, create 3 different instances from class and call on
     describe_restaurant() for each instance"""
    def __init__(self, name, cuisine_type):
        self.name = name.title()
        self.cuisine_type = cuisine_type

    def describe_restaurant(self):
        msg = f"{self.name} serves wonderful {self.cuisine_type}"
        print(f"\n{msg}")

    def restaurant_open(self):
        msg = f"{self.name} is open!"
        print(f"\n{msg}")

rosetta_coffee = Restaurant('Rosetta Coffee Brewing Co.', 'coffee')
rosetta_coffee.describe_restaurant()
mcdonald_s = Restaurant("McDonald's", 'hamburgers')
mcdonald_s.describe_restaurant()
in_n_out = Restaurant("In N' Out", 'hamburgers')
in_n_out.describe_restaurant()

# - - - - - - - - - - - - - - - - - - - - - - - - -

class Home:
    """ describing the people and gender in my house"""
    def __init__(self, name, gender):
        self.name = name.title()
        self.gender = gender.title()

    def person(self):
        msg = f"Name: {self.name} is {self.gender}"
        print(msg)

alan_ = Home('Alan Keith', 'male')
print(f"{alan_.name} is a {alan_.gender}")
becky = Home('Becky Keith', 'female')
print(f"{becky.name} is a {becky.gender} ")
sissy = Home('Stephanie Rubalcava', 'female')
print(f"{sissy.name} is a {sissy.gender}")

# - - - - - - - - - - - - - - - - - - - - - - - - -
# 9-3 Users
class User:
    """ first_name and last_name, plus additional attributes"""
    def __init__(self, first_name, last_name, email, address, phone):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email
        self.address = address
        self.phone = phone

    def describe_user(self):
#        name = f"{self.first_name} {self.last_name}"
        msg = f"Name: {self.first_name} {self.last_name}\n" \
              f"Email: {self.email}\n" \
              f"Address: {self.address}\n" \
              f"Phone: {self.phone}"
        print(msg)

    def greet_user(self):
        print(f"Welcome back, {self.first_name}\n")


jonathan = User('Jonathan',
                 'Baldwin',
                 'jon@sinoverpi.com',
                 '22379 San Joaquin Dr. W.',
                 '949_243_5825')
jonathan.greet_user()
jonathan.describe_user()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# WORKING WITH CLASSES AND INSTANCES
# The car class
# car.py

# Setting a default value for an attribute
# adding an attribute

# 9-4 Number Served

class Restaurant:
    """ a class that takes a restaurant name and cuisine type then prints it
     out"""
    def __init__(self, name, cuisine_type):
        self.name = name.title()
        self.cuisine_type = cuisine_type.title()
        self.number_served = 0

    def describe_restaurant(self):
        """Describes restaurant name and type of cuisine."""
        msg = f"{self.name} serves wonderful {self.cuisine_type}"
        print(f"\n{msg}")

    def open_restaurant(self):
        """Method that prints a message indicating the restaurant is open"""
        msg = f"\n{self.name} is open!"
        print(msg)
    def set_number_served(self, number_served):
        """Allows user to change number served"""
        self.number_served = number_served
    def update_number_served(self, update_served):
        self.number_served += update_served

# making instance called restaurant
restaurant = Restaurant('Rosetta Coffee Brewing Co.', 'coffee')
print(restaurant.name)
print(restaurant.cuisine_type)
print(f"Number served: {restaurant.number_served}")
restaurant.number_served = 2_507
print(f"Updated number served (10/31/2000): {restaurant.number_served}")
restaurant.update_number_served(2_987)
print(f"Additional numbers served (12/31/2000): {restaurant.number_served}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 9-5 Login Attempts
# Add an attribute called login_attempts to your User class from Exercise 9-3
# (page 162). Write a method called increment_login_attempts() that increments
# the value of login_attempts by 1. Write another method called
# reset_login_attempts() that resets the value of login_attempts to 0. Make an
# instance of the User class and call increment_login_attempts() several times.
# Print the value of login_attempts login_attempts to make sure it was
# incremented properly, and then call reset_login_attempts(). Print
# login_attempts again to make sure it was reset to 0.


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
        print(f"Welcome back, {self.first_name}\n")

    def total_login_attempts(self, login_attempts):
        self.login_attempts = login_attempts

    def increment_login_attempts(self):
        self.login_attempts += 1

    def reset_login_attempts(self):
        self.login_attempts = 0


jonathan = User('Jonathan',
                 'Baldwin',
                 'jon@sinoverpi.com',
                 '22379 San Joaquin Dr. W.',
                 '949_243_5825')
jonathan.greet_user()
jonathan.describe_user()
jonathan.total_login_attempts(3)
print(f"Total login attempts: {jonathan.login_attempts}")
jonathan.increment_login_attempts()
jonathan.increment_login_attempts()
jonathan.increment_login_attempts()
print(f"You have now attempted to login: {jonathan.login_attempts}")
jonathan.reset_login_attempts()
print(f"Resetting login attempts: {jonathan.login_attempts}")

# INHERITANCE: already have a class? Use inheritance to borrow from it
# parent class > child class

# The __init__() Method for a child class
# electric_car.py

# DEFINING ATTRIBUTES AND METHODS FOR THE CHILD CLASS
# and new attributes do child that differentiate from parent
# electric_car.py

# OVERRIDING METHODS FROM THE PARENT CLASS
# how: defining method in the child class with the same name is the method
#   you want to override

# INSTANCES AS ATTRIBUTES
# electric_car.py

# IMPORTING CLASSES: storing classes and modules and importing them

# STORING MULTIPLE CLASSES IN A MODULE
# car.py
























































































































