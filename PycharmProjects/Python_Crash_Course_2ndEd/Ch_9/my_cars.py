from car import Car, ElectricCar

my_beetle = Car('Volkswagen', 'beetle', 2019)
print(f"my_beetle.get_descriptive_name()\n")


my_tesla = ElectricCar('Tesla', 'roadster', 2019)
print(my_tesla.get_descriptive_name())
my_tesla.battery.describe_battery()