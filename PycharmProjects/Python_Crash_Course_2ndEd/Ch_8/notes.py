# ---> CHAPTER 8: FUNCTIONS <--- #

# FUNCTIONS: named blocks of code, designed to do one specific job
#   – when a task needs to be performed multiple times in a program
#   – modules: functions stored as separate files. Helped organize main program

# Defining a function

# greeter.py

# arguments and parameters
#   – greeter.py use of user name = "parameter"
#       – the value 'jesse' = argument
#       – essentially: 'jesse' passed to the function greed_user() and the
#           value assigned to the perimeter' username'

# 8-1 Message
"""
def display_message():
    print("Hello everyone! I'm learning about Python Functions.")

display_message()
"""

# 8-2 favorite book
"""
def favorite_book(title):   # def function(parameter)
    print(f"My favorite book is {title.title()}")   #call to parameter

favorite_book('alice in wonderland')    # Alice in Wonderland = argument
"""

# Passing arguments
#    positional arguments: same order the parameters were written;
#       keyword arguments, variable name and value; lists and dictionaries
#       of values

# positional arguments
#   – order of arguments must be matched
# pets.py

# Multiple Function Calls
#   - you can call functions as many times as needed
# pets.py

# order matters in positional arguments
#    – do NOT mix up arguments or you get unexpected results
# pets.py

# KEYWORD ARGUMENTS
#   – name-value pair —>passed to a function
#   – up to this point keyword arguments were sort of automatic
#   – now, when the function is called, the call itself matches the parameters
# pets.py

# DEFAULT VALUES
#   – keyword-argument supersedes default values: if a keyword argument is used
#       (see above), Python uses the explicit argument, not the defaults.
# pets.py
"""
def describe_pet(pet_name, animal_type='dog'): # NOTE: order of parameters changed.
#   Still a positional argument, so pet name would be 1st. (See page 135)
    print(f"\nI have a {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name}.")

describe_pet(pet_name='willie')
"""

# EQUIVALENT FUNCTION CALLS
#   – it doesn't matter which style you use as long as your calls produce
#       the results you want. Use what's easiest

# AVOIDING ARGUMENT ERRORS
"""
def describe_pet(animal_type, pet_name):
    print(f"\nI have an animal named {pet_name}")
    print(f"My animal type is {animal_type}")

describe_pet()  #creates error, as there's no argument
"""

# 8-3 T-shirt:
"""
def make_shirt(shirt_size, message):
    # printout size of shirt and message on it
    print(f"\nThe size of the shirt is {shirt_size.title()}")
    print(f"Message on shirt: {message.upper()}")
# function call: positional argument
make_shirt('large', 'just do it')
# function call: keyword-argument
make_shirt(shirt_size='large', message='just do it')
"""

# 8-4 Large Shirts:
"""
def make_shirt(message_shirt='i love python', size_shirt='large'):
    print(f"\nSize of shirt: {size_shirt.title()}")
    print(f"Comment on shirt: {message_shirt.upper()}")
# default shirt
make_shirt()
# medium shirt
make_shirt(size_shirt='medium')
"""

# 8-5 Cities:
"""
def describe_city(city_name='reykjavik', city_country='iceland'):
    print(f"\n{city_name.title()} is in the country of {city_country.title()}.")

describe_city()
describe_city('san francisco', 'america')
describe_city(city_name='london', city_country='great britain')
"""

# RETURN VALUES

#   – functions that display output INDIRECTLY
#   – moves a lot of grunt work into functions which simplify the program

# Returning a simple value
# formatted_name.py

# MAKING AN ARGUMENT OPTIONAL
#   – users can add extra information if needed
#   – default values are good here

"""
def get_formatted_name(first_name, last_name, middle_name=''):  # empty argument makes middle_name optional
    #  Return a full name, neatly formatted. #
    if middle_name:     # if-else added for if user provides middle name
        full_name = f"{first_name} {middle_name} {last_name}"
    else:
        full_name = f"{first_name} {last_name}"
    return full_name.title()

musician = get_formatted_name('john', 'lee', 'hooker')  # IF-else triggered
print(musician)
musician = get_formatted_name('tom', 'smith')   # else: no middle name provided
print(musician)
"""

# RETURNING A DICTIONARY
"""   – functions can return any value: lists and dictionaries too
# person.py

# USING A FUNCTION WITH A WIRE LOOP
#    – eeverything learned in the book so far can be used in a def function
 greeter.py 
"""

# 8-6 City Names:
"""
def city_country(city='laguna beach', country='america'):
    # returns "city, country"
    full_name = f"{city}, {country}"
    return full_name.title()

city = city_country('santiago', 'chile')
print(city)
city = city_country(city='los angeles', country='america')
print(city)
city = city_country()
print(city)
"""

# 8-7 album:
"""
def make_album(artist='', title='', year=''):
    # assigns artist, album to dictionary
    album = {
        'artist': artist,
        'title': title}
    if year:
        album['year'] = year
    return album

total = make_album('sting', 'englishman in new york', '1988')
print(total)
total = make_album('inxs', 'listen like thieves', ' 1986')
print(total)
total = make_album('depeche mode', 'music for the masses', '1987')
print(total)
"""

# 8-8 user albums

# make_album_mine.py
# Python crash course, 2nd edition
# here, I tried to do exercise chapter 8-7, but added inputs, so I can build
# the dictionary from scratch... It doesn't seem to work just yet

"""
def make_album(artist, title, year):
    # assigns artist, album to dictionary
    album = {
        'artist': artist.title(),
        'title': title.title()}
    if year:
        album['year'] = year
    return album
# organize inputs or whatever
print("\nAdd an Album to the Dictionary")
print("(enter 'q' at any time to quit)")
# while loop
while True:
    artist = input("\nArtist: ")
    if artist == 'q':
        break
    title = input("Album: ")
    if title == 'q':
        break
    year = input("Year: ")
    if year == 'q':
        break
# album_d = make_album()
    total = make_album(artist, title, year)
    print(total)

print("\nEnjoy your albums!")
"""

# PASSING THE LIST: greet_users.py

# MODIFYING A LIST IN A FUNCTION: printing_models.py --  when you need to move items from
#   one list to another. every function should have one job, specific.

# preventing a function from modifying a list by sending a copy of the list:
#   function_name(list_name[:])     # slice copies list and sends to function
#   example:
#   previous exercise: print_models(printed_designs[:], completed_models)

#8-9 Messages:

"""
def show_messages(texts):
    # pass messages and print #
    for text in texts:
        print(text)

messages = ['hey there!', 'No. not coming.', 'yes, you are.']
show_messages(messages)
"""

# 8-10 sending messages

# function:  send_messages() -> prints each text message
#   2: after printing, sends each message to sent_messages()
#   3: print each list to show the messages have been moved
"""
def show_messages(messages):
    print("Showing all messages:")
    for message in messages:
        print(message)


def f_messages(messages, sent_messages):
    print("\nPrinting all messages:")
    while messages:
        current_messages = messages.pop()
        print(current_messages)
        sent_messages.append(current_messages)

messages = ['Hello!', 'No. Not me.', 'Will you go?']
show_messages(messages)

sent_messages = []
f_messages(messages, sent_messages)

print("\nFinal lists:")
print(messages)
print(sent_messages)
"""

# Passing an arbitrary number of arguments– pizza.py

#Mixing positional and arbitrary arguments –
















