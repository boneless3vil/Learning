# Python crash course chapter 6

# a simple dictionary
"""
alien_0 = {'color': 'green', 'points': 5}

print(alien_0['color'])
print(alien_0['points'])
"""

# -- working with dictionaries --
    # dictionary: collection of key-value pairs. Each key connected to a value.
    # Dictionaries are wrapped in braces {}
    # Values: numbers, or strings, or lists, or other dictionaries
#assessing values in a dictionary
"""
alien_0 = {'color': 'green'}
print(alien_0['color']) # alien_0 is dictionary, [] contains key
                        # print(dictionary['key']
"""
# unlimited number of key-value pairs in a dictionary
"""
alien_0 = {'color': 'green', 'points': 5}
# access values
new_points = alien_0['points']
print(f"You just earned {new_points} points!")
"""
#adding new key-value pairs
"""
alien_0 = {'color': 'green', 'points': 5}
print(alien_0)

alien_0['x_position'] = 0   # new key-value pair
alien_0['y_position'] = 25  #2nd new key-value pair
print(alien_0)  #Prince out additional 2 key-value pears
"""

# -- Starting with an empty dictionary {} --
"""
alien_0 = {}    #empty dictionary

alien_0['color'] = 'green'  #1st key-value added
alien_0['points'] = 5       #2nd key-value-added

print(alien_0)
"""
# modifying values in a dictionary
"""
alien_0 = {'color': 'green'}
print(f"The alien is {alien_0['color']}")

alien_0['color'] = 'yellow'
print(f"The alien is now {alien_0['color']}")
"""
# tracking alien speed
"""
alien_0 = {'x_position': 0, 'y_position': 25, 'speed': 'medium'}
print(f"Original position: {alien_0['x_position']}")

#move the alien to the right
    #determine how far to move the alien based on its current speed.
if alien_0['speed'] == 'slow':
    x_increment = 1
elif alien_0['speed'] == 'medium':
    x_increment = 2
else:
    # This must be a fast alien
    x_increment = 3
# the new position is the old position + the increment:
alien_0['x_position'] = alien_0['x_position'] + x_increment

print(f"New position: {alien_0['x_position']}")
"""
# removing key-value pairs
    # use the DEL statement to PERMANENTLY remove ke-value pairs
"""
alien_0 = {'color': 'green', 'points': 5}
print(alien_0)

del alien_0['points']
print(alien_0)  #result: 'points': 5 removed from list
"""
# creating a poll: a dictionary of similar objects
"""
favorite_languages = {  #when a list is going to be several lines,
                        #after 1st {
    'jennifer': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python',
}

language = favorite_languages['sarah'].title()
print(f"Sarah's favorite language is {language}.")
"""
# Using get() to access values
"""
alien_0 = {'color': 'green', 'speed': 'slow'}
# print(alien_0['points'])    # causes error without key-value in alien_0

point_value = alien_0.get('points', 'No point value assigned.')
print(point_value)
"""

# 6-1 Person:
"""
person = {
    'first_name': 'jonathan',
    'last_name': 'baldwin',
    'age': '51',
    'race': 'white'
}
print(person['first_name'].title())
print(person['last_name'].title())
print(person['age'].title())
print(person['race'].title())
"""
# 6-2
"""
favorite_numbers = {
    'becky': '3',
    'alan': '5',
    'nick': '2',
    'sissy': '9'
}

print(favorite_numbers['becky'].title())
print(favorite_numbers['alan'].title())
print(favorite_numbers['nick'].title())
print(favorite_numbers['sissy'].title())
"""
# 6-3 Glossary
"""
glossary = {
    'get()': 'get(): set a default value where there is none.',
    'range()': 'range(): a range of numbers',
    'len()': 'len(): returns number of items in list.',
    'list': 'list: items stored in an accessible place',
    'tuple': 'tuple: just like a list, but immutable'
}

print("Glossary of terms and their definitions:")
print(glossary['get()'])
print(glossary['range()'])
print(glossary['len()'])
print(glossary['list'])
print(glossary['tuple'])
"""

# -- Looping through a Dictionary --
#looping through ALL key-value pairs
"""
user_0 = {
    'username': 'efermi',
    'first': 'enrico',
    'last': 'fermi'
}
#  to see everything stored, use a FOR loop
for key, value in user_0.items():   # items() returns list of key-value pairs
# ! this FOR loop can be abbreviated: for k, v in user_0.items ():
    print(f"\nKey: {key}")
    print(f"\nValue: {value}")
"""
# polling question from page 97, loop
"""
favorite_languages = {
    'jennifer': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'c#'
}

for n, l in favorite_languages.items():
    print( f"{n.title()}'s favorite language is {l.title()}")
"""
# Looping through all the keys in a dictionary:
# keys(): use when you specific values in a dictionary
"""
favorite_languages = {
    'jennifer': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'c#'
}

for n in favorite_languages.keys():
    print(n.title())
#alternatively— looping through keys is default behavior, so simplified:
# for n in favorite_languages:
    # print(n.title())

"""
# looping through keys, and responding
"""
favorite_languages = {
    'jennifer': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'c#'
}

friends = ['phil', 'sarah']
for n in favorite_languages.keys():
    print(f"Hi {n.title()}")
    if n in friends:
        l = favorite_languages[n].title()
        print( f"\t{n.title()}, I see you love {l}")
"""
"""
favorite_languages = {
    'jennifer': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'c#'
}

if 'erin' not in favorite_languages.keys():
    print("Erin, please take our poll!")
"""
# Looping through a dictionary's keys: particular order
"""
favorite_languages = {
    'jennifer': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'c#'
}

for n in sorted(favorite_languages.keys()):
    print(f"{n.title()}, thank you for taking the poll!")
"""
# looping through ALL values in a dictionary
# values() return list of values without keys
"""
favorite_languages = {
    'jennifer': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'c#'
}

print("The following languages have been mentioned:")
for l in sorted(favorite_languages.values()):  # I chose to use sorted()
    print(l.title())
"""
# using the set() method: unique items in list are built-in to set
"""
favorite_languages = {
    'jennifer': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python'
}

for l in set(favorite_languages.values()):
    print(l.title())
# result: 2nd mention of Python is ignored
"""
# NOTE: set() method can be built directly using braces
    # example: languages = {'python', 'ruby', 'python', 'c'}

# 6-4 glossary 2:
"""
glossary = {
    'get()': 'set a default value where there is none.',
    'range()': 'a range of numbers',
    'len()': 'returns number of items in list.',
    'list': 'items stored in an accessible place',
    'tuple': 'just like a list, but immutable'
    }

# the convoluted way to write it:

# print("Glossary of terms:")
#for t in sorted(glossary.keys()):
#    print(t.title())
#print("\nDefinitions:")
#for d in set(glossary.values()):
#    print(d.title())
    
#the right way!

for t, d in glossary.items():
    print(f"\n{t.title()}: {d}")

"""

# 6-5 Rivers
"""
rivers = {
    'mississippi': 'north america',
    'nile': 'africa',
    'colorado': 'north america'
}
"""
# convoluted, wrong way
"""
for k, v in rivers:
    if k == 'mississippi':
        print(f"The {k.title()} is in .")
    if k == 'nile':
        print(f"The {k.title()} is in Africa.")
    if k == 'colorado':
        print(f"The {k.title()} is in North America.")
     """
# right way!
"""
for r, c in rivers.items():
    print(f"{r.title()} runs through {c.title()}")
"""

# 6-6 Polling:
"""
favorite_languages = {
       'jen': 'python',
       'sarah': 'c',
       'edward': 'ruby',
       'phil': 'python',
       }

n_poll = ['noah', 'phil', 'tim', 'robert']
for p in favorite_languages.keys():
    if p in n_poll:
        print(f"{p.title()}, please take the poll!")
    if p in
    else:
        print("Thanks for taking the pole!")
"""

# Nesting
""" store multiple dictionaries in a list, list of items as a value of
     a dictionary, or a dictionary in a dictionary"""
# a list of dictionaries
"""
alien_0 = {'color': 'green', 'points': 5}
alien_1 = {'color': 'yellow', 'points': 10}
alien_2 = {'color': 'red', 'points': 15}

aliens = [alien_0, alien_1, alien_2]

for alien in aliens:
    print(alien)
"""
# automatic alien generator (copier) list

# empty list for storing aliens
"""
aliens = []
# make 30 green aliens.
for alien_number in range(30):
    new_alien = {'color': 'green', 'points': 5, 'speed': 'slow'}
    aliens.append(new_alien)
"""
# show the 1st 5 aliens.
"""
for alien in aliens[:5]:
    print(alien)
print("…")
"""
# show how many aliens have been created.
"""
print(f"Total number of aliens: {len(aliens )}")
"""
# for loop to change aliens
    # uses slice to loop through 1st 3 aliens
"""
for alien in aliens[:3]:
    if alien['color'] == 'green':
        alien['color'] = 'yellow'
        alien['speed'] = 'medium'
        alien['points'] = 10
"""
# elif block used to turn yellow–>red, fast->worth 15 points
"""
    elif alien['color'] == 'yellow':
        alien['color'] = 'red'
        alien['speed'] = 'fast'
        alien['points'] = 15
for alien in aliens[4:10]:
    print(alien)
print("…")
"""
# show how many aliens have been created.
"""
print(f"Total number of aliens: {len(aliens )}")
"""

# list inside a dictionary: store information about a pizza being ordered.
"""
pizza = {
    'crust': 'thick',
    'toppings': ['mushrooms', 'extra cheese'],
}   #summarize order:
print(f"You ordered a {pizza['crust']}-crust pizza " # break a print() /w a " at end of 1st line
      "with the following toppings:")  # and another at beginning of 2nd line, shown here

for t in pizza['toppings']:
    print(f"\t{t}")
"""
# favorite_languages with multiple values
"""
favorite_languages = {
    'jennifer': ['python', 'ruby'],
    'sarah': ['c'],
    'edward': ['ruby', 'go'],
    'steve': ['python', 'c#', 'Java']
}

for name, languages in favorite_languages.items():   #can be abbreviated name = n, language = l, but not recommended. PEP8
# I seem to get the 1st 1 done correctly, but the rest are not stripping the [] and ''. Why?
    for language in languages:
        x = len(languages)
        if x < 2:
            print(f"\n{name.title()}'s favorite language is: {language.title()}")
    else:   # I don't know. I just can't do it LOL
        y = len(languages)
        if y == 2:
            print(f"\n{name.title()}'s favorite languages are: {language}")
"""
# dictionary in a dictionary
# many_users.py
"""
users = {
    'aeinstein': {
               'first': 'albert',
               'last': 'einstein',
               'location': 'princeton',
               },
     'mcurie': {
               'first': 'marie',
               'last': 'curie',
               'location': 'paris',
               },
}

for username, user_info in users.items():
    print(f"\nUsername: {username}")
    full_name = f"{user_info['first']} {user_info['last']}"
    location = user_info['location']

    print(f"\tFull name: {full_name.title()}")
    print(f"\tLocation: {location.title() }")
"""
# 6-7 People:
"""
people = {
    'bonelessevil': {
        'first_name': 'jonathan',
        'last_name': 'baldwin',
        'age': '51',
        'race': 'white'
    },
    'sJohansson': {
        'first_name': 'scarlett',
        'last_name': 'johansson',
        'age': '38',
        'race': 'white'
    },
    'zDeutch': {
        'first_name': 'Zoey',
        'last_name': 'Deutch',
        'age': '28',
        'race': 'white'
    },
    'jDanger': {
        'first_name': 'Jordan',
        'last_name': 'Danger',
        'age': '31',
        'race': 'white'
    }
}
for username, user_info in people.items():
    print(f"\nUsername: {username}")
    full_name = f"{user_info['first_name']} {user_info['last_name']}"
    age = user_info['age']
    race = user_info['race']

    print(f"\tName: {full_name.title()}")
    print(f"\tAge:  {age}")
    print(f"\tRace: {race.title()}")
"""
# 6-8 pets:
"""
pets = {
    'astro': {
        'owner_first': 'george',
        'owner_last': 'jetson',
        'breed': 'labrador'
    },
    'scooby': {
        'owner_first': 'norville "shaggy"',
        'owner_last': 'rogers',
        'breed': 'great dane'
    },
    'bullet': {
        'owner_first': 'jonathan',
        'owner_last': 'baldwin',
        'breed': 'yorkie'
    }
}

for pet, pet_info in pets.items():
    print(f"Pet name:  {pet.title()}")
    print(f"\tOwner: {pet_info['owner_first'].title()} "
          f"{pet_info['owner_last'].title()}")
    print(f"\tBreed: {pet_info['breed'].title()}")
"""
# 6-9 Favorite places:
"""
favorite_places = {
    'becky': {
        'no1': 'montana',
        'no2': 'new york',
        'no3': 'friends'
    },
    'alan': {
        'no1': 'las vegas',
        'no2': 'no tell motel',
        'no3': 'pot dealer'
    },
    'sissy': {
        'no1': 'las vegas',
        'no2': 'san francisco',
        'no3': 'disneyland'
    }
}

for p, p_info in favorite_places.items():
    print(f"Traveler: {p.title()}")
    print(f"\t1st Choice: {p_info['no1'].title()}")
    print(f"\t2nd Choice: {p_info['no2'].title()}")
    print(f"\t3rd Choice: {p_info['no3'].title()}")
"""
#6-10 favorite numbers:
"""
favorite_numbers = {
    'becky': {
        'fn1': 3,
        'fn2': 3.14,
        'fn3': 7
    },
    'alan': {
        'fn1': 5,
        'fn2': 1_000,
        'fn3': 7
    },
    'nick': {
        'fn1': 2,
        'fn2': 14,
        'fn3': 77
    },
    'sissy': {
        'fn1': 9,
        'fn2': 2,
        'fn3': 16
    }
}

for n, fn_info in favorite_numbers.items():
    print(f"Name: {n.title()}")
    print(f"\t1st Favorite Number: {fn_info['fn1']}")
    print(f"\t2nd Favorite Number: {fn_info['fn2']}")
    print(f"\t3rd Favorite Number: {fn_info['fn3']}")
"""
# 6-11 Cities
"""
cities = {
    'london': {
        'country': 'england',
        'pop': 8_982_000,
        'fact': 'Totally where I should meet my wife.'
    },
    'vancouver': {
        'country': 'canada',
        'pop': 675_218,
        'fact': 'Totally where I want to live, if I moved to Canada.'
    },
    'jerusalem': {
        'country': 'israel',
        'pop': 874_186,
        'fact': 'Most religious city on Earth.'
    }
}

for city, city_info in cities.items():
    print(f"City: {city.title()}")
    print(f"\tCountry: {city_info['country'].title()}")
    print(f"\tPopulation: {city_info['pop']:,}")    
    #wow! Solved this little issue with numbers and using commasÜ on my own
    print(f"\tFact: {city_info['fact']}")
"""
# 6-12 Extensions:
# did that in the previous example. :-)













































































































