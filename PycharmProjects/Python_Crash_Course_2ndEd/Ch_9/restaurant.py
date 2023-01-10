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
