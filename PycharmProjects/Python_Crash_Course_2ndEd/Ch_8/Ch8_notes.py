# CHAPTER 8
# DEFINING A FUNCTION
def greet_user():
    """ Display a simple greeting."""
    print("Hello!")
greet_user()

# PASSING INFORMATION TO A FUNCTION
def greet_user(username):   # function now expects username to be defined
    # in the call. In this case, Jesus.
    """ display a simple greeting."""
    print(f"Hello, {username.title()}")
greet_user('Jesus')

# ARGUMENTS AND PARAMETERS
# 8-1
def display_message():
    """Prints out message explaining chapter 8"""
    print("I'm learning about functions")
display_message()
# 8-2 favorite book
def favorite_book(title):
    t2 = title
    print(f"My favorite book is {t2.title()}")
favorite_book('Mere Christianity')

# PASSING ARGUMENTS
# multiple parameters may need multiple arguments

# POSITIONAL ARGUMENTS
def describe_pet(animal_type, pet_name):    # you can have many parameters
    """ display information about a pet."""
    print(f"\nI have a {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name.title()}")
describe_pet('hamster', 'Harry')    # for each parameter, you need a argument
# MULTIPLE FUNCTION CALLS
# functions can be called as many times as needed
describe_pet('dog', 'bullet')   #same function called again, but with different
#   arguments
# ORDER MATTERS IN POSITIONAL ARGUMENTS
describe_pet('Yoda', 'dog')     # mixed up order screws up print() statement
# above
# KEYWORD ARGUMENTS: name-value pair that passes to a function
describe_pet(animal_type='cat', pet_name='taco kitty')  # directly calling
#   function clears confusion if out of order call happens

# DEFAULT VALUES: a default parameter/value means if no argument, default is returned
def describe_pet(pet_name, animal_type ='dog'):     # parameters with default
    #   values must be listed last.
    """ display information about a pet"""
    print(f"\nI have a {animal_type}.") # no animal type selected, so dog is
    #   returned in print statements
    print(f"My {animal_type}'s name is {pet_name.title()}.")
describe_pet(pet_name='Willie') #
# EQUIVALENT FUNCTION CALLS:
# 8-3 T-shirt
def make_shirt(size, message):
    print(f"Your T-shirt will be size {size.title()}.\nIt will say: {message}\n")
make_shirt(size='large', message='Jesus is the reason for the season!')
make_shirt('small', 'I <3 to FUCK!')
# 8-4 large shirts
def make_shirt(message, size='large'):
    print(f'Your T-shirt will be size {size.title()} and say, "{message.title()}"')
make_shirt(message='I <3> Python')

# 8-5 cities
def describe_city(city, country='Iceland'):
    print(f"The city of {city} is in {country}")
describe_city('Reykjavik')
describe_city('Los Angeles', 'America')
describe_city('London', 'England')

# RETURN VALUES: FUNCTIONS CAN RETURN VALUES WITHOUT PRINTING TO SCREEN
def get_formatted_name(first_name, last_name):
    """ Return a full name, neatly formatted."""
    full_name = f"{first_name} {last_name}"
    return full_name.title()
musician = get_formatted_name('jimi', 'Hendrix')
print(musician)     # why not just print('Jimi Hendrix') ? Because, when
# working with many names, Separately, this method is simpler

# MAKING AN ARGUMENT OPTIONAL: users choose whether to provide extra information
def get_formatted_name(first_name, last_name, middle_name=''):
    """ Return a full name, neatly formatted."""
    if middle_name:     # page, 137: if middle name not needed, IF statement
        # helps
        full_name = f"{first_name} {middle_name} {last_name}"
    else:
        full_name = f"{first_name} {last_name}"
    return full_name.title()
musician = get_formatted_name('Jonny', 'Lee', 'hooker')
print(musician)
musician = get_formatted_name('Jimi', 'Hendrix')
print(musician)

# RETURNING A DICTIONARY
def build_person(first_name, last_name, age=None):    #function defined first
    """ Return a dictionary of information about a person."""
    person = {'first': first_name, 'last': last_name}   #dictionary containing person added
    # NONE special value, when variable has no specific value applied
    if age:
        person['age'] = age
    return person
musician = build_person('Jimi', 'hendrix')
print(musician)

# USING A FUNCTION WITH A WHILE LOOP
def get_formatted_name(first_name, last_name):
    """ Return a full name, neatly formatted."""
    full_name = f"{first_name} {last_name}"
    return full_name.title()
    # this is an infinite loop!
while True:
    print("\nPlease tell me your name:")
    print("(enter 'q' at any time to quit)")
    f_name = input("First name: ")
    if f_name == 'q':
        break
    l_name = input("Last name: ")
    if l_name == 'q':
        break
    formatted_name = get_formatted_name(f_name, l_name)
    print(f"\nHello, {formatted_name}!")

# 8-6 city names
def city_country(city, country):
    print(f"The city of {city} is in {country}.")
city_country('Los Angeles', 'the United States of America')
city_country('London', 'England')
city_country('Tokyo', 'Japan')
# 8-7 Album
# instructions
def make_album(artist, title, tracks=0):
    """Build a dictionary containing information about an album."""
    album_dict = {
        'artist': artist.title(),
        'title': title.title(),
        }
    if tracks:
        album_dict['tracks'] = tracks
    return album_dict

# User inputs:
p_title = "Enter an album you like… "   # executes while statement
p_artist = "What is the artist's name? "

# instruct how to quit
print("(Enter 'q' to quit) ")

while True:
    title = input(p_title)  # takes input from p_title and applies it to title
    if title == 'q':
        break
    artist = input(p_artist)
    if artist == 'q':
        break
    album = make_album(artist, title)
    print(album)
print("Thank you for adding your albums! ")

# 8-7 stuff """
f_album = make_album('Sting', 'Englishman in New York', 'fragile')
print(f_album)
f_album = make_album('INXS', 'listen like thieves')
print(f_album)

# 8-8 user albums: while loops """

# PASSING A LIST: gives function direct access to target list
def greet_users(names):
    """ print a simple greeting to each user in the list."""
    for name in names:
        msg = f"Hello, {name.title()}"
        print(msg)
usernames = ['hannah', 'ty', 'margo']
greet_users(usernames)

# MODIFYING A LIST IN A FUNCTION:  passing a list to a function, the function can modify it
# ! Changes are permanent
# start with some designs that need to be printed.
unprinted_designs = ['phone case', 'robot pendant', 'dodecahedron']
completed_models = []

#simulate printing each design, until none are left.
# Move each design to the completed_models after printing.
while unprinted_designs:
    current_design = unprinted_designs.pop()
    print(f"Printing model: {current_design}")
    completed_models.append(current_design)

# display all completed models
print("\nThe following models have been completed:")
for model in completed_models:
    model_reversed = sorted(model, reverse=True)
    print(model)

# previous script, restructured
def print_models(unprinted_designs, completed_models):
    """ Simulate printing each design, until none are left. Move each design to
    the completed models after printing"""
    while unprinted_designs:
        current_model = unprinted_designs.pop()
        print(f"Design to be printed: {current_model}")
        completed_models.append(current_model)

def show_completed_models(completed_models):
    """ Show all the models that were printed."""
    print(f"\nThese models were printed:")
    for model in completed_models:
        print(model)

unprinted_designs= ['phone case', 'robot pendant', 'dodecahedron']
completed_models = []
print_models(unprinted_designs, completed_models)
show_completed_models(completed_models)

# PREVENTING A FUNCTION FROM MODIFYING THE LIST
# copy the list using slice [:]
print_models(unprinted_designs[:], completed_models)

# 8-9 messages. Critique: function not necessary. Use for loop
messages = ['Hey, want Boner pills?',
            'Yes, I hid the body',
            'Aliens DID abduct me and probe my orifices, '
            'no matter what you say']
def show_messages(messages):
    """takes messages and prints them"""
    for message in messages:
        print(message)
show_messages(messages)


# 8-10
def show_messages(messages):
    """ prints unsent messages"""
    print("Showing all messages:")
    for message in messages:
        print(message)


def send_messages(messages, sent_messages):
    """takes messages and prints them"""
    print(f"\nSending all messages: ")
    while messages:
        current_message = messages.pop()
        print(current_message)
        sent_messages.append(current_message)

messages = ['Hey, want Boner pills?', 'Yes, I hid the body', 'Aliens DID abduct me and probe my orifices']
show_messages(messages)

sent_messages = []
send_messages(messages, sent_messages)

print(f"\nMessages list: {messages}")
print(f"Sent messages list: {sent_messages}")

# 8-11

def show_messages(messages):
    """ show all messages."""
    print("Showing all messages: ")
    for message in messages:
        print(message)

def send_messages(messages, sent_messages):
    """ show messages that were sent"""
    print("\nSending all messages: ")
    while messages:
        current_message = messages.pop()
        print(current_message)
        sent_messages.append(current_message)

messages = ['Hey, want Boner pills?', 'Yes, I hid the body', 'Aliens DID abduct me and probe my orifices']
show_messages(messages)

sent_messages = []
send_messages(messages[:], sent_messages)

print(f"\nShowing all messages: {messages}")
print(f"Showing all sent messages: {sent_messages}")

# PASSING AN ARBITRARY NUMBER OF ARGUMENTS
def make_pizza(*toppings):
    """ print the list of toppings that have been requested."""
    print(toppings)
make_pizza('pepperoni')
make_pizza('mushrooms', 'green peppers', 'extra cheese')
# -----
def make_pizza(*toppings):
    """summarize the pizza to be made."""
    print("\nMaking a pizza with the following toppings: ")
    for topping in toppings:
        print(f"- {topping}")
make_pizza('pepperoni')
make_pizza('mushrooms', 'green peppers', 'extra cheese')

# MIXING POSITIONAL AND ARBITRARY ARGUMENTS
#   If you want a function to accept several different kinds of arguments, the
#   parameter that accepts an arbitrary number of arguments must be placed last
#   in the function definition.
def make_pizza(size, *toppings):
    """ summarize the pizza we are about to make."""
    print(f"\nMaking a {size} pizza with the following toppings:")
    for topping in toppings:
        print(f"– {topping}")
make_pizza(16, 'pepperoni')
make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')

# USING ARBITRARY KEYWORD ARGUMENTS
def build_profile(first, last, **user_info):
    """Build a dictionary containing everything we know about a user."""
    user_info['first_name'] = first
    user_info['last_name'] = last
    return user_info

user_profile = build_profile('Albert', 'Einstein',
                             location='Princeton',
                             field='physics')
print(user_profile)

# 8-12 Sandwiches
def make_sandwiches(*toppings):
    print(f"Making your sandwich with:")
    for topping in toppings:
        print(topping)
make_sandwiches('jalapenos', 'tuna')
make_sandwiches('bacon', 'lettuce', 'tomato')
make_sandwiches('meatballs', 'mozzarella')

# 8-13 User profile
def build_profile(first, last, **user_info):
    """Build a dictionary containing everything we know about a user."""
    user_info['first_name'] = first
    user_info['last_name'] = last
    return user_info
user_profile = build_profile('Jonathan', 'Baldwin',
                             location='Canyon Lake',
                             field='writing',
                             favorite_movie = '')
print(user_profile)

# 8-14 Cars, arbitrary keyword arguments, page 148-149
def make_car(make, model, **options):
    """function to store information about a car"""
    car_dict = {        # create a dictionary
    'make': make.title(),
    'car_model': model.title(),
    }

    for option, value in options.items():   #add extra arbitrary items here
        car_dict[option] = value        # dict[Key] = Value
    return car_dict

my_subaru = make_car('Subaru', 'outback', toe_pack=True, color='blue')
print(my_subaru)

my_honda = make_car('Honda', 'accord', color='silver', doors=4)
print(my_honda)

# STORING YOUR FUNCTIONS IN MODULES
# allows you to use the import function to bring in separate modules, thereby
#   keeping your code cleaner
# IMPORTING AN ENTIRE MODULE
import pizza    # when using import, you may need to create a new .py file or
#   you might get  a: ModuleNotFoundError: No module named 'pizza'

pizza.make_pizza(16, 'pepperoni')
pizza.make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')

# IMPORTING SPECIFIC FUNCTIONS
# SYNTAX: from <module_name> import <function_name>
# SYNTAX, MULTIPLE ITEMS: from <module_name> import function_0, function_1,
#                         function_2...

# USING as TO GIVE A FUNCTION IN ALIAS
from pizza import make_pizza as mp
mp( 16, 'pepperoni')
mp(12, 'mushrooms', 'green peppers', 'extra cheese')
# USING as TO GIVE A MODULE AN ALIAS
import pizza as p
p.make_pizza(16, 'pepperoni')
p.make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')
# IMPORTING ALL FUNCTIONS IN A MODULE with *
from pizza import *
make_pizza(16, 'pepperoni')
make_pizza(12, 'mushrooms', 'green peppers', 'extra cheese')
# STYLING FUNCTIONS
# USE: descriptive names, comment that explains function + docstring
# def function_name(parameter_0, parameter_1='default value')
# (https://www.python.org/dev/peps/pep-0008/) for more information

# 8-15 printing models
# using printing_models.py as an import
# quiz file printing_models_functions.py

# 8-16 Imports






















































































































