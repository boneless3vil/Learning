

# --- CHAPTER FIVE: IF STATEMENTS ---

#simple example
print('\033[1m' + 'Simple IF statement' + '\033[0m')    #extra arguments for bold text
cars = ['audi', 'bmw', 'subaru', 'toyota']
for car in cars:
    if car == 'bmw':
        print(car.upper())
    else:
        print(car.title())

# Conditional Test
print('\033[1m' + '\nConditional test' + '\033[0m')
print("equality operator == ")
for car in cars:
    if car == 'bmw':
        print(f"BMW = True")
    else:
        print(car)
#Checking for inequality
print('\033[1m' + '\nChecking for inequality: !=' + '\033[0m')
for car in cars:
    if car != 'bmw':
        print(f"BMW = False")
    else:
        print("This is a BMW")

# Checking for multiple conditions
print('\033[1m' + '\nChecking for multiple conditions' + '\033[0m')
age = 22
age1 = 15
if age >= 13 and age1 <= 19:
    print("True")
else:
    print("False")
print("\nChecking for one number")
if age >= 13 and age <= 45:
    print("True")
else:
    print("False")

# Checking whether a value is in a list
print('\033[1m' + '\nChecking whether a value is in a list' + '\033[0m')
if 'subaru' in cars:
    print(f"True, Subaru is on the last.")
else:
    print(f"False, Subaru is not a car on the list.")
# checking whether a value is NOT in a list
print("Checking whether a value is NOT in a list")
if 'tesla' not in cars:
    print("Tesla is not on the list")
else:
    print("Tesla is on the list.")

# IF statements
print('\033[1m' + '\nSimple if statements' + '\033[0m')
print("Syntax: if conditional_test:\n"
      "        do something")
age = 19
if age >= 18:
    print("You are old enough to vote!")

# if-else statements
print('\033[1m' + '\nif-else statements' + '\033[0m')
age = 17
if age >= 18:
    print("You are old enough to vote!")
else:
    print("Sorry, you are too young yet to vote.")

# the if-elif-else chain
print('\n\033[1m' + 'The if-elif-else chain' + '\033[0m')
age = 12
if age < 4:
    print("Admission for anyone under age 4 is free.")
elif age < 18:
    print("Admission for anyone between the ages of four and 18 is $25.")
else:
    print("Admission for anyone age 18 or older is $40.")

# using multiple elif blocks
print('\n\033[1m' + 'Using multiple ELIF blocks' + '\033[0m')
age = 15
if age <4:
    price = 0
elif age < 18:
    price = 25
elif age > 65:
    price = 40
else:
    price = 20
print(f"Your admission cost is ${price}.")

# testing multiple conditions: IF-ELIF-ELSE
print('\n\033[1m' + 'testing multiple conditions: IF-ELIF-ELSE' + '\033[0m')
requested_toppings = ['mushrooms', 'extra cheese']
if 'mushrooms' in requested_toppings:
    print("Adding mushrooms.")
if 'extra cheese' in requested_toppings:
    print("Adding extra cheese.")
if 'pepperoni' in requested_toppings:
    print("Adding pepperoni.")
print("\nfinished making your pizza!")

# Using IF statements with lists
print('\n\033[1m' + 'Using IF statements with lists' + '\033[0m')
print("Requested toppings but what if a topping is unavailable?")
for requested_topping in requested_toppings:
    if requested_topping == 'green peppers':
        print("Sorry, that topping is unavailable.")
    else:
        print(f"Adding {requested_topping}")
print("\nFinished making your pizza!")

# Checking that a list is not empty
print('\n\033[1m' + 'Checking that a list is not empty' '\033[0m')
requested_toppings = []
if requested_toppings:
    for requested_topping in requested_toppings:
        print(f"Adding {requested_topping}.")
else:
    print("Are you sure you want a plain pizza?")

# Using Multiple Lists
print('\n\033[1m' + 'Using Multiple Lists' + '\033[0m')
available_toppings = ['mushrooms', 'olives', 'green peppers', 'pepperoni', 'pineapple', 'extra cheese']
requested_toppings = ['mushrooms', 'french fries', 'extra cheese']

for requested_topping in requested_toppings:
    if requested_topping in available_toppings:
        print(f"Adding {requested_topping}")
    else:
        print(f"Sorry, we don't have {requested_topping}")
print("\nFinished making your pizza!")










