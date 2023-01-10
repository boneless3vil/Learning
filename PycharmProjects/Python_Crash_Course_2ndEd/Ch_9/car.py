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