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




























