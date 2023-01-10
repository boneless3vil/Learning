

class Car:  # parent class comes before child class (line 36)
    """A simple attempt to represent a car."""

    def __init__(self, make, model, year):
        """Initialize attributes to describe a car."""
        self.make = make
        self.model = model
        self.year = year
        # additional attribute
        self.odometer_reading = 0    # attribute modified directly,
        #                                    page 164
        self.hvac = True

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

    def hvac_install(self):
        if self.hvac:
            print("This vehicle comes with an air conditioner.")
        else:
            print("This vehicle does not come with an air conditioner.")


class Battery:  # no need for inheritance from parental class
    """A simple attempt to model a battery for an electric car."""
    def __init__(self, battery_size=75):
        """Initialize the battery's attributes."""
        self.battery_size = battery_size

    def describe_battery(self):
        """Print a statement describing the battery size."""
        print(f"This car has a {self.battery_size}-kWt battery.")

    def get_range(self):
        """Print a statement about the range this battery provides."""
        if self.battery_size == 75:
            range = 260
        elif self.battery_size == 100:
            range = 315
        print(f"This car can go about {range} miles on a full charge.")

    def upgrade_battery(self):
        if self.battery_size == 75:
            self.battery_size = 100
            print("Battery upgraded to 100 kWt.")
        else:
            print("Battery already upgraded.")


class ElectricCar(Car): # class child(parent) and parent class must be included
    # with the child

    """ Represents aspects of a car, specific to electric vehicles."""

    def __init__(self, make, model, year):  # __init __ takes info from parent
        # for child

        """ Initialize attributes of the parent class. Then initialize attributes
        specific to an electric car."""

        super().__init__(make, model, year)
        # super() special function, allows child class to call a method from parent

        # page 169: defining attributes and methods for the child class
        # Updated on page 170, instances as attributes moved describe_battery to
        # Battery class
        self.battery = Battery()


    def fill_gas_tank(self):    # Overriding parent class, page 170
        """Electric cars don't have gas tanks."""
        print("Electric cars have gas tanks? Whoa...")

my_tesla = ElectricCar('Tesla', 'model S', 2019)   # instance assigned to my_tesla

print("Car Model:\n")
print(my_tesla.get_descriptive_name())
my_tesla.battery.describe_battery() # here, Python is told, look at my_tesla -->
# find battery attribute --> call describe_battery() method
my_tesla.battery.get_range()    # page 171

# upgraded battery
print("\nBattery upgraded to 100 kWt:\n")
print("Car Model:\n")
print(my_tesla.get_descriptive_name())
my_tesla.battery.upgrade_battery()
my_tesla.battery.get_range()

print("\nGas tank size:")
my_tesla.fill_gas_tank()

my_tesla.hvac_install()

















