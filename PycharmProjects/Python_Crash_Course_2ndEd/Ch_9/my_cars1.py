# IMPORTING AN ENTIRE MODULE, page 176

import car

my_beetle = car.Car('Volkswagen', 'beetle', 2019)
print(f"my_beetle.get_descriptive_name()\n")


my_tesla = car.ElectricCar('Tesla', 'roadster', 2019)
print(my_tesla.get_descriptive_name())
my_tesla.battery.describe_battery()