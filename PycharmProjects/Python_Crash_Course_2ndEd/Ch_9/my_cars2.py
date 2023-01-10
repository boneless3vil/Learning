# IMPORTING A MODULE INTO A MODULE, PAGE 177
# When you store your classes in several modules, you might find that a class in
# one module depends on a class in another module. When this happens, you can
# import the required class into the first module

from car import Car
# first way to import the class:
#   from electric_car import ElectricCar

# 2nd way, import the class as an alias
from electric_car import ElectricCar as EC

my_beetle = Car('Volkswagen', 'beetle', 2019)
print(f"{my_beetle.get_descriptive_name()}\n")


my_tesla2 = EC('Tesla', 'roadster', 2019)
print(my_tesla2.get_descriptive_name())
my_tesla2.battery.describe_battery()