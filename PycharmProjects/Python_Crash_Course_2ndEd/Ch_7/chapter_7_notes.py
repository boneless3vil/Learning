

# CHAPTER 7: USER INPUT AND WHILE LOOPS
print("\033[1mCHAPTER 7: USER INPUT AND WHILE LOOPS\033[0m")

# HOW THE INPUT() FUNCTION WORKS
print("\n\033[1mHOW THE INPUT() FUNCTION WORKS\033[0m")

message = input("Tell me something, and I will repeat it back to you: ")
print(message)

# WRITING CLEAR PROMPTS
print("\n\033[1mWRITING CLEAR PROMPTS\033[0m")
# write easy to follow prompts when using input()
name = input("Please enter your name: ")
print(f"\nHello, {name}!")
# inputting at prompt
prompt = "If you tell us who you are, we can personalize the messages you see."
prompt += "\nWhat is your last name? "
name = input(prompt)
print(f"\nHello, Mr. {name}")

# USING INT() TO ACCEPT NUMERICAL INPUT
print("\n\033[1mUSING int() FUNCTION TO ACCEPT NUMERICAL INPUT\033[0m")
age = input("How old are you? ") # use input() to create prompt
age = int(age)  # when answer will be numerical, = prompt with int()
print(f"\nRecording your age as: {age}")

# THE MODULO OPERATOR
print("\n\033[1mTHE MODULO OPERATOR\033[0m")
print("\n\033[1mmodulo (%): divides one number by another number and returns the remainder\033[0m")

number = input("Enter a number, and I'll tell you if it's even or odd: ")
number = int(number)
if number % 2 == 0: # if the inputted number is divisible by 2, it's even.
    print(f"\nThe number {number} is even.")
else:
    print(f"\nThe number {number} is odd.")


# INTRODUCING WHILE LOOPS
print("\n\033[1mINTRODUCING WHILE LOOPS\033[0m")
# THE WHILE LOOP IN ACTION
print("\n\033[1mTHE WHILE LOOP IN ACTION\033[0m")

current_number = 1
while current_number <= 5:
    print(current_number)
    current_number += 1     # += operator shorthand for (var = var + 1)

# LETTING THE USER CHOOSE WHEN TO QUIT
# parrot.py

prompt = "\nTell me something, and I will repeated back to you:"
prompt += "\nEnter 'quit' to the end of the program.  "
message = ""
while message != 'quit':
    message = input(prompt)
    if message != 'quit':   # While it works to just print the message and not
        # have this IF statement, without it, program will print "quit" when one
        # types quit
        print(message)

# USING A FLAG, PAGE 119
# parrot.py

prompt = "\nTell me something, and I will repeated back to you:"
prompt += "\nEnter 'quit' to the end of the program.  "
active = True   #set variable to True
while active:   # while True, take input
    message = input(prompt)
    # if message quit, exit program
    if message == 'quit':
        active = False
    else:
        print(message)

# USING BREAK TO EXIT A LOOP
# cities.py

prompt = "\nPlease into the name of a city you have visited:"
prompt += "\n(Enter ' quit' when you are finished.)"

while True:
    city = input(prompt)

    if city == 'quit':
        break
    else:
        print(f"I'd love to go to {city.title()}!")

# USING CONTINUE IN A LOOP
# counting.py

# USING A while LOOP WITH LISTS AND DICTIONARIES
# MOVING ITEMS FROM ONE LIST TO ANOTHER

# Start with users that need to be verified,
#   and an empty list to hold confirmed users.
unconfirmed_users = ['Alice', 'Jerry', 'Steve']
confirmed_users = []
# Verify each user until there are no more unconfirmed users.
#   Move each verified user into the list of confirmed users.
print(f"Verifying user:")
for u_user in unconfirmed_users:
    print(u_user)
while unconfirmed_users:
    current_users = unconfirmed_users.pop()
    confirmed_users.append(current_users)
# Display all confirmed users.
print("\nList of confirmed users: ")
for c_user in sorted(confirmed_users):  # sorts confirmed_users, BEFORE printing
    # each user, so Steve is last again.
    print(c_user)


# REMOVING ALL INSTANCES OF SPECIFIC VALUES FROM A LIST
# PAGE 124
# pets.py

pets = ['dog', 'cat', 'dog', 'goldfish', 'cat', 'rabbit', 'cat']
print(pets)

while 'cat' in pets:
    pets.remove('cat')  #removes all references to cat

print(pets)

# FILLING A DICTIONARY WITH USER INPUT
# mountain_poll.py

responses = {}

# set flag to indicate that polling is active.
polling_active = True
while polling_active:
    # prompt for the person's name and response.
    name = input("\nWhat is your name? ")
    response = input("Which mountain would you like to climb some day? ")

    # Store the response in the dictionary.
    responses[name] = response

    # find out if anyone else is going to take the poll.
    repeat = input("Would you like to let another person respond? (yes/no) ")
    if repeat == 'no':
        polling_active = False
    # Polling is complete. Show the results.
    print("\n--- Poll Results ---")
    for name, response in responses.items():
        print(f"{name} would you like to climb {response}.")

# 7-8 Deli
sandwich_orders = ['pastrami', 'BLT', 'club', 'pastrami', 'pastrami',]
finished_sandwiches = []
# 7-9 remove unavailable item: pastrami
print("We apologize, but we do not have any Pastrami")
while 'pastrami' in sandwich_orders:
    sandwich_orders.remove('pastrami')

#create loop
while sandwich_orders:  # while sandwich_orders has items in list  = True
    current_sandwich = sandwich_orders.pop()    # 2nd list populates from 1st with pop()
    print(f"Making {current_sandwich}")
    finished_sandwiches.append(current_sandwich)    # 3rd list append() from 2nd list

for sandwich in finished_sandwiches:
    print(f"{sandwich.title()} order is up!")

# 7-10 dream vacation:
responses = {}  # var to store answers
# set polling active.
polling_active = True   # start polling by setting interactive
while polling_active:
    name = input("\nWhat is your name? ")   # store name
    response = input("If you could visit one place in the world, where would "
                     "you go? ")    # store response
    # store the response in the dictionary
    responses[name] = response  # formatting/adding to dict[key] = value
    # Find out if anyone else is going to take the poll.
    repeat = input("Would anyone else like to take the poll? (yes/no) ")
    if repeat == 'no':  # exit
        polling = False
    # polling is complete. Show the results
    print("\n--- Poll Results ---")
    for name, response in responses.items():    # printout each name, response
        # for each respondent
        print(f"{name} would like to visit {response}. ")









































































