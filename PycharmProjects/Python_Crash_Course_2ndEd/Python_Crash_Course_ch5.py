# Python crash course chapter 5

#checking for equality ==
"""
cars = ['audi', 'bmw', 'subaru', 'toyota']

for car in cars:
    if car == 'bmw':
        print(car.upper())
    else:
        print(car.title())
"""

# checking for inequality !=
"""
requested_topping = 'mushrooms'
if requested_topping != 'anchovies': #compares value of requested_topping
                                    # to ' anchovies'
    print("Hold the anchovies!")
"""
# Numerical Comparisons
"""
answer = 42
if answer != 42:
    print("that is not the correct answer. Please try again!")
else:
    print("wonderful!")
"""

# checking multiple conditions
"""
age_0 = 22
age_1 = 18
if age_0 >= 21 or age_1 >= 21:  # if either comparison = true, results: true
    print("So true, dude!")
else:
    print("totally wrong, loser!")
"""

# checking whether a value is in a list
"""
requested_toppings = ['mushrooms', 'onions', 'pineapple']
if 'mushrooms' in requested_toppings:
    print('yummy!')
else:
    print('I need my shrooms!')
"""

# checking if value is NOT in a list
"""
banned_users = ['andrew', 'carolina', 'david']
user = 'marie'

if user not in banned_users:
    print(f"{user.title()}, you can post a response if you wish.")
"""

# Boolean expressions: a conditional test, either true or false
"""
game_active = True # checks whether game is active
can_edit = False    # example, test whether one can edit the game
"""

# 5-1 conditional test
"""
car_brand = 'ford'  #not a list
print("Is a F150 produced by Ford? I predict it is.")
print(car_brand == 'ford')

print("\nIs a Renegade produced by Ford? I predict false.")
print(car_brand == 'jeep')

print("\nIs a BMW produced by Ford? I don't think it is.")
if car_brand != 'bmw':
    print("No.")
else:
    print("Yes.")
"""

# 5-2 more conditional tests:
"""
fruit = 'apple'
# ttest for equality ==, and inequality !=
print("Are apples fruits?")
if fruit == 'apple':
    print("Yes, they are fruits.")
else:
    print("No. It is not a fruit")
# Not != inequality statement
print("\nIs broccoli a fruit?")
if fruit != 'broccoli':
    print('No. It is not a fruit.')
else:
    print('Yes, it is a fruit')
# lower() check
print("\n")
if fruit == 'Apple':
    print(fruit)
else:
    print(fruit.title())
# numerical >=, <=
print("\nDo we have enough apples?")
num_apples = 19
if num_apples >= 20:
    print("We have enough apples.")
else:
    print("We do not have enough apples.")
# and, or uses
if num_apples >= 20 and num_apples < 40:
    print("\nWe have enough apples.")
if num_apples > 40 or num_apples < 20:
    print("The correct amount of apples has not been reached.")
# test: if item medicine list
fruit_list = ['apple', 'tomatoes', 'pineapple', 'strawberries']
if 'tomatoes' in fruit_list:
    print("\nTomatoes are in fruit_list")
else:
    print("No, tomatoes are not in fruit_list")

if 'blueberries' not in fruit_list:
    print("blueberries are not in fruit_list")
else:
    print("blueberries are not in fruit_list")
"""

# IF Statements
# if-else statements
"""
age = 17
if age >= 18:
    print("You are old enough to vote!")
    print("Have you registered to vote yet?")
else:
    print("Sorry, you are too young to vote.")
    print("Please register to vote as soon as you turn 18!")
"""

# if-elif-else
# the long version
"""
age = 12
if age < 4:
    print("your admission cost is $0.")
elif age < 18:
    print("Your admission cost is $25.")
else:
    print("Your admission cost is $40.")
"""
#the short version
"""
age = 12
if age < 4:
    price = 0
elif age < 18:
    price = 25
else:
    price = 40
print(f"Your admission cost is ${price}.")

"""
# multiple ELIF blocks
"""
age = 12
if age < 4:
    price = 0
elif age < 18:
    price = 25
elif age < 65:
    price = 40
else:           # else statement can be omitted
    price = 20
print(f"Your emission cost is: ${price}")
"""
# testing multiple values without ELIF, ELSE
"""
requested_toppings = ['mushrooms', 'extra cheese']

if 'mushrooms' in requested_toppings:
    print("Adding mushrooms.")
if 'pepperoni' in requested_toppings:
    print("Adding pepperoni.")
if 'extra cheese' in requested_toppings:
    print("Adding extra cheese.")

print("\nFinished making your pizza!")
"""

# 5-3 Alien Colors #1
"""
alien_color = 'green'
if 'green' == alien_color:
    print("Player has scored 5 points.")

if 'red' == alien_color:
    print("You hit the commander")
else:
    print("\nTry again.")
"""

#5-4 alien colors #2
"""
alien_color = 'green'
if alien_color == 'red':
    print("You earned 5 points.")
else:
    print("you earned 10 points.")
"""

# 5-5 alien colors #3:
"""
alien_color = 'green'
if alien_color == 'green':
    print("You earned 5 points by choosing green.")
elif alien_color == 'red':
    print("You earned 15 points by choosing red.")
else:
    print("You earned 10 points by choosing yellow.")

alien_color = 'red'
if alien_color == 'green':
    print("You earned 5 points by choosing green.")
elif alien_color == 'red':
    print("You earned 10 points by choosing red.")
else:
    print("You earned 15 points by choosing yellow.")

alien_color = 'yellow'
if alien_color == 'green':
    print("You earned 5 points by choosing green.")
elif alien_color == 'red':
    print("You earned 10 points by choosing red.")
else:
    print("You earned 15 points by choosing yellow.")
"""

# 5-6 stages of life:
"""
age = 16

if age < 2:
    print("This person is a baby.")
elif age < 4:
    print("This person is a toddler.")
elif age < 13:
    print("This person is a kid.")
elif age < 20:
    print("This person is a teenager.")
elif age < 65:
    print("This person is an adult.")
else:
    print("This person is an elder.")
"""

# 5-7 Favorite fruit:
"""
favorite_fruits = ['apple', 'strawberries', 'blueberries', 'raspberries']

if 'apple' in favorite_fruits:
    print("You really like apples.")
if 'potatoes' not in favorite_fruits:
    print("You really don't like potatoes.")
if 'blueberries' in favorite_fruits:
    print("You really like Blueberries.")
if 'raspberries' in favorite_fruits:
    print("You really like raspberries.")
         """

# IF statements with lists
"""
requested_toppings = ['mushrooms', 'green peppers', 'extra cheese']

for requested_topping in requested_toppings: #simple loop through list
    print(f"Adding {requested_topping}.")
"""

# out of green peppers? use ELSE
"""
for requested_topping in requested_toppings:
    if requested_topping == 'green peppers':
        print("Sorry, we don't have green peppers.")
    else:
        print(f"Adding {requested_topping}")
print("\nFinished making your pizza!")
"""

# checking list is NOT empty
"""
requested_toppings = []
if requested_toppings:  # this loop checks TRUE or FALSE list
    for requested_topping in requested_toppings:
        print(f"Adding {requested_topping}")
    print("\nFinished making your pizza!")
else:
    print("Are you sure you want a plain pizza?")
"""

# using multiple lists
"""
available_toppings = ['mushrooms', 'olives', 'green peppers', 'pepperoni',
                      'pineapple', 'extra cheese']
requested_toppings = ['mushrooms', 'french fries', 'extra cheese']

for requested_topping in requested_toppings:
    if requested_topping in available_toppings:
        print(f"Adding {requested_topping}")
    else:
        print(f"{requested_topping} unavailable.")
print("\nFinished making your pizza!")
"""

# 5-8 hello admin
"""
users = ['bonelessevil', 'footstool', 'admin', 'steve', 'jerry']
for user in users:
    if 'admin' == user:
        print("Hello admin!")
    else:
        print("Hello user.")
"""

# 5-9 no users:
"""
users = []
if users:   # still seems to work without this line, but using it cleaner code?
    for user in users:
        if 'admin' == user:
            print("Hello admin!")
        else:
            print("We need more users.")
else:
    print("We need more users.")
"""

# 5-10 checking usernames:
"""
current_users = ['user1', 'user2', 'uSEr3', 'user4', 'user5']
new_users = ['user6', 'USer7', 'user1', 'user8', 'user9']

current_users_lower = [user.lower() for user in current_users]
    # force list into lowercase, so you can compare names like john and JOHN,
    # and still check results

for new_user in new_users:
    if new_user.lower() in current_users_lower:
        print("Username already taken.")
    else:
        print("Username available.")
"""

# 5-11 ordinal numbers: numbers that indicate their position in a list: 1st,
    # 2nd
# 5-11: how I solved it:
"""
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

for number in numbers:
    if number > '3':
        print(f"{number}th\n")
    elif number == '1':
        print("1st\n")
    elif number == '2':
        print("2nd\n")
    elif number == '3':
        print("3rd\n")
"""
# 5-11: the better way!
"""
numbers = list(range(1, 10))    #remember number ranges in Ch. 4 range()

for number in numbers:
    if number == 1:
        print("1st\n")
    elif number == 2:
        print("2nd\n")
    elif number == 3:
        print("3rd\n")
    else:
        print(f"{number}th\n")
"""
















































