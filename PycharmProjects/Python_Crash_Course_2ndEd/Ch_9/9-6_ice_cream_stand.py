"""
9-6. Ice Cream Stand: An ice cream stand is a specific kind of restaurant.
Write a class called IceCreamStand that inherits from the Restaurant class
you wrote in Exercise 9-1 (page 162) or Exercise 9-4 (page 167). Either version
of the class will work; just pick the one you like better. Add an attribute
called flavors that stores a list of ice cream flavors. Write a method that
displays these flavors. Create an instance of IceCreamStand, and call this
method.
"""

class Restaurant:
    """ a class that takes a restaurant name and cuisine type then prints it
     out"""
    def __init__(self, name, cuisine_type):
        self.name = name.title()
        self.cuisine_type = cuisine_type

    def describe_restaurant(self):
        """Describes restaurant name and type of cuisine."""
        msg = f"{self.name} serves wonderful {self.cuisine_type}"
        print(f"\n{msg}\n")

    def open_restaurant(self):
        """Method that prints a message indicating the restaurant is open"""
        msg = f"\n{self.name} is open!"
        print(msg)


class IceCreamStand(Restaurant):
    """Inherited from Restaurant class (exercise 9-1). Add an attribute to store
    flavors of ice cream and call it's method"""

    def __init__(self, name, cuisine_type='ice cream'):
        super().__init__(name, cuisine_type)
        self.flavors = []

    def show_flavors(self):
        """Display available ice cream flavors"""
        print(f"Available ice cream flavors:")
        for flavor in self.flavors:
            print(f"– {flavor.title()}")


# call instance ice_cream_flavors to display flavors
chocolate_chip_cyclone = IceCreamStand('Chocolate Chip Cyclone')
chocolate_chip_cyclone.flavors = ['vanilla', 'chocolate chips', 'bleach',
                                  'peanut butter dog food', 'public telephone']

chocolate_chip_cyclone.describe_restaurant()
chocolate_chip_cyclone.show_flavors()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# practice
class ButtFlavoredDogFood(Restaurant):
    """A dog food store with several flavors"""

    def __init__(self, name, cuisine_type='dog food'):
        super().__init__(name, cuisine_type)
        self.flavors = []
        self.cuisine_type = 'vegan dog food'

    def show_flavors(self):
        """Available flavors"""
        print("Not just for dogs! Try these flavors:")
        for flavor in self.flavors:
            print(f"– {flavor}")

butt_flavored_dog_food = ButtFlavoredDogFood('Butt Flavored Dog Food')
butt_flavored_dog_food.flavors = ['saucy butt',
                                  'peanut butt',
                                  'corn kernel lovers',
                                  'chocolate, all chocolate']

butt_flavored_dog_food.describe_restaurant()
butt_flavored_dog_food.show_flavors()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Pizza900(Restaurant):
    """Pizza 900 menu"""

    def __init__(self, name, cuisine_type='pizza'):
        super().__init__(name, cuisine_type)
        self.toppings = []
        self.cuisine_type = cuisine_type

    def pizza_toppings(self):
        """Available toppings list"""
        print("These are our available toppings:\n")
        for topping in self.toppings:
            print(f"– {topping}")


pizza900 = Pizza900('Pizza 900')
pizza900.toppings = ['pepperoni', 'green peppers', 'mushrooms',
                     'asiago cheese', 'black olives', 'spicy sauce']

pizza900.describe_restaurant()
pizza900.pizza_toppings()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class BeefJerkyPalace(Restaurant):
    """ beef jerky menu with toppings"""
    def __init__(self, name, cuisine_type='beef jerky'):
        super().__init__(name, cuisine_type)
        self.cuisine_type = cuisine_type
        self.flavors = []

    def jerky_flavors(self):
        """ beef jerky flavors added to empty list"""
        print("These are our available toppings:\n")
        for flavor in self.flavors:
            print(f"– {flavor}")

beefjerkypalace = BeefJerkyPalace('Beef Jerky Palace')
beefjerkypalace.flavors = ['venison', 'peppered', 'teriyaki',
                                 'hot peppered']
beefjerkypalace.describe_restaurant()
beefjerkypalace.jerky_flavors()














































