 # Chapter 7: user input and while loops
"""
message = input("Tell me something, and I will repeat it back to you: ")
print(message)
"""

# 7-1 rental car
"""
car = input("Which kind of car would you like to buy?:")
print(f"Let me see if I can find you a {car.title()}")
"""

# 7-2 restaurant seating:
"""
seats = input("How many guests will be eating?: ")
seats = int(seats)
if seats < 8:
    if seats < 1:
        print("Invalid number")
    else:
        print("We can seat you right away.")
else:
    print("You will have to wait for a table.")
"""

# 7-3 multiples of 10:
"""
number = input("Input a number: ")
number = int(number)

if number % 10 == 0:
    print(f"The number is a multiple of 10.")
else:
    print(f"This number is not a multiple of 10.")
"""

# 7-4 pizza toppings:
"""
prompt = "\nWhat topping would you like on your pizza?"
prompt += "\nEnter 'quit' when you are finished: "

while True:
    topping = input(prompt)
    if topping != 'quit':
        print(f"  I'll add {topping} to your pizza.")
    else:
        break
"""
# 7-5 movie tickets
"""
prompt = "\nEnter your age to see ticket price."
prompt += "\n(Enter 'quit' when finished)"
prompt += "\n$-: "

while True:
    ticket = input(prompt)
    if ticket == 'quit':
        break

    age = int(ticket)
    if age < 3:
        print(f"\nTickets for age {age} are FREE!")
    elif age < 13:
        print(f"\nTickets for age {age} are $10.")
    else:
        print(f"\ntickets for age {age} are $15.")
"""
# 7-6 create an infinite loop
"""
prompt = "This is an infinite loop."
prompt += "\nType something: "
loop = input(prompt) # by leaving this variable outside while loop, infinite loop is created

while True:
#    loop = input(prompt)   #putting the variable inside the while loop, no infinite loop created
    if loop != 'quit':
        print(loop)
"""
# Using a wire loop with lists and dictionaries
# moving items from one list to another
# confirmed_users.py

# Removing all instances of specific values from a list
#   pets.py

# filling a dictionary with user input
#   mountain_poll.py

# 7-8 Deli:
"""
sandwich_orders = ['pastrami', 'meatloaf', 'vegetarian', 'tuna salad', 'blt',
                   'club']
finished_sandwiches = []

while sandwich_orders:      # while list has items = True, run loop
    f_sandwich = sandwich_orders.pop()          # pop items from sandwich_orders list (automatically added 
                                                # last to 1st) add them to f_sandwich
    print(f"Making your {f_sandwich.title()}")  # print each item
    finished_sandwiches.append(f_sandwich)      # move items to empty list

print(f"Finished making the following sandwiches:")
for fs in finished_sandwiches:          #for each item in final list
    print(f"{fs.title()} sandwich.")    #print item
"""

# 7-9 No pastrami:
"""
sandwich_orders = ['pastrami', 'meatloaf', 'vegetarian', 'pastrami', 'tuna salad', 'pastrami', 'blt',
                   'club']
finished_sandwiches = []
# Remove all mentions of pastrami
print(f"We don't have Pastrami.\n")
while 'pastrami' in sandwich_orders:    
    sandwich_orders.remove('pastrami')

while sandwich_orders:      # while list has items = True, run loop
    f_sandwich = sandwich_orders.pop()          # pop items from sandwich_orders list (automatically added
                                                # last to 1st) add them to f_sandwich
    print(f"Making your {f_sandwich.title()}")  # print each item
    finished_sandwiches.append(f_sandwich)      # move items to empty list

print(f"\nFinished making the following sandwiches:\n")
for fs in finished_sandwiches:          #for each item in final list
    print(f"{fs.title()} sandwich.")    #print item
"""

# 7-10 Dream Vacation:
# create a poll

name_prompt = "\nWhat is your name? "
place_prompt = "\nIf you could visit one place in the world, where would you go? "
continue_prompt = "\nDoes someone else want to answer the survey? "

# stores results in dictionary, {name: place}
poll = {}

while True:
    # retrieve answers from polling questions
    name = input(name_prompt)
    place = input(place_prompt)
    #
    poll[name] = place
    #
    repeat = input(continue_prompt)
    if repeat != 'yes':
        break

# print results
print("\n--- RESULTS ---")
for name, place in poll.items():
    print(f"{name.title()} wants to visit {place.title()}")





























































































