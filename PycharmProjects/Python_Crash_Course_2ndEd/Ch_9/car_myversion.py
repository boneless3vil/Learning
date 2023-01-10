

# My version 1st
class Car:
    """ A simple attempt to represent a car"""
    def __init__(self, make, model, year):
        self.make = make.title()    #not necessary to put .title() twice. Look at line 25 and 32
        self.model = model.title()
        self.year = year

    def get_descriptive_name(self):
        """ return a neatly formatted descriptive name"""
        name = f"Year: {self.year}\nMake: {self.make}\nModel: {self.model}"
        print(name)     # use return instead like line 32

car = Car('Honda', 'accord', '1982')
car.get_descriptive_name()

# their version
class Car:
    """A simple attempt to represent a car."""

    def __init__(self, make, model, year):
        """Initialize attributes to describe a car."""
        self.make = make
        self.model = model
        self.year = year

    def get_descriptive_name(self):
        """Return a neatly formatted descriptive name."""
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()

my_new_car = Car('audi', 'a4', 2019)
print(my_new_car.get_descriptive_name())

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Adding attributes:

class Car:
    """A simple attempt to represent a car."""

    def __init__(self, make, model, year):
        """Initialize attributes to describe a car."""
        self.make = make
        self.model = model
        self.year = year
        # additional attribute
        self.odometer_reading = '75,987'

    def get_descriptive_name(self):
        """Return a neatly formatted descriptive name."""
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()

    def read_odometer(self):
        """ print a statement showing the car's mileage."""
        print(f"This car has {self.odometer_reading} miles on it.")

my_new_car = Car('audi', 'a4', 2019)
print(my_new_car.get_descriptive_name())
my_new_car.read_odometer()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# MODIFYING ATTRIBUTE VALUES
# 3 DIFFERENT WAYS:
#   - change the value directly through an instance
#   - set the bow you through a method
#   - increment value (at a certain amount to it) through a method

class Car:
    """A simple attempt to represent a car."""

    def __init__(self, make, model, year):
        """Initialize attributes to describe a car."""
        self.make = make
        self.model = model
        self.year = year
        # additional attribute
        self.odometer_reading = 75643    # attribute modified directly,
        #                                    page 164

    def get_descriptive_name(self):
        """Return a neatly formatted descriptive name."""
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()

    def read_odometer(self):
        """ print a statement showing the car's mileage."""
        print(f"This car has {self.odometer_reading} miles on it.")

    def update_odometer(self, mileage): # modifying attribute through a method,
        #                               page 164
        """ set the odometer reading to the given value"""
        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("You can't rollback an odometer!")

my_new_car = Car('audi', 'a4', 2019)
print(my_new_car.get_descriptive_name())
my_new_car.read_odometer()

# modifying attribute value with a method, page 164
my_new_car.update_odometer(23)
my_new_car.read_odometer()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Incrementing an attribute's value through a method

class Car:
    """A simple attempt to represent a car."""

    def __init__(self, make, model, year):
        """Initialize attributes to describe a car."""
        self.make = make
        self.model = model
        self.year = year
        # additional attribute
        self.odometer_reading = 0    # attribute modified directly,
        #                                    page 164

    def get_descriptive_name(self):
        """Return a neatly formatted descriptive name."""
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()

    def read_odometer(self):
        """ print a statement showing the car's mileage."""
        print(f"This car has {self.odometer_reading} miles on it.")

    def update_odometer(self, mileage): # modifying attribute through a method,
        #                               page 164
        """ set the odometer reading to the given value"""
        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("You can't rollback an odometer!")

    def increment_odometer(self, miles):
        """At the given amount to the odometer reading."""
        self.odometer_reading += miles


my_new_car = Car('audi', 'a4', 2019)
print(my_new_car.get_descriptive_name())
my_new_car.read_odometer()

# modifying attribute value with a method, page 164
my_new_car.update_odometer(23)
my_new_car.read_odometer()

# incrementing an attribute value through a method
my_used_car = Car('Subaru', 'outback', 2015)
print(my_used_car.get_descriptive_name())

my_used_car.update_odometer(23_500)
my_used_car.read_odometer()

my_used_car.increment_odometer(100)
my_used_car.read_odometer()








































