

# CHAPTER SIX NOTES:
print('\n\033[1m' + 'CHAPTER SIX NOTES' + '\033[0m')

# Simple Dictionary
print('\n\033[1m' + 'Simple Dictionary' + '\033[0m')
print('\033[1m' + 'dict = {Key, Value}' + '\033[0m')
alien_0 = {'color': 'green', 'points': 5}
print(alien_0['color'])
print(alien_0['points'])

# Assessing Values in a Dictionary
print('\n\033[1m' + 'Assessing Values in a Dictionary' + '\033[0m')
alien_0 = {'color': 'green', 'points': 5}
print(alien_0['color'])

# Adding New Key-Value Pairs
print('\n\033[1m' + 'Adding New Key-Value Pairs' + '\033[0m')
alien_0['x_position'] = 0
alien_0['y_position'] = 25
print(alien_0)

# Empty dictionary
print('\n\033[1m' + 'Empty Dictionary' + '\033[0m')
alien_0 = {}

alien_0['color'] = 'green'
alien_0['points'] = 5
print(alien_0)

# Modifying Values in a Dictionary
print('\n\033[1m' + 'Modifying Values in a Dictionary' + '\033[0m')
alien_0= {'color': 'green'}
print(f"The alien is {alien_0['color']}.")
#Change the color:
alien_0['color'] = 'yellow'
print(f"The alien is now {alien_0['color']}.")

# alien movement
print('\n\033[1m' + 'Alien Movement' + '\033[0m')
alien_0 = {'x_position': 0,
           'y_position': 25,
           'speed': 'medium'}
print(f"Original position: {alien_0['x_position']}")

# Move the alien to the right.
#   Determine how far to move the alien based on its current speed.
if alien_0['speed'] == 'slow':  # dict[Key] == Value
    x_increment = 1
if alien_0['speed'] == 'medium':
    x_increment  = 2
else:
    # alien must be going fast
    x_increment = 3

# The new position is the old position plus the increment
alien_0['x_position'] = alien_0['x_position'] + x_increment
print(f"New position: {alien_0['x_position']}")

# Removing Key-Value Pairs
print('\n\033[1m' + 'Removing Key-Value Pairs' + '\033[0m')
print(f"Original dictionary: {alien_0}")
del alien_0['speed']
print(f"Speed Key has been removed using\x1B[1;3m del\033[0m: {alien_0}")

# A Dictionary of Similar Objects
print('\n\033[1m' + 'A Dictionary of Similar Objects' + '\033[0m')
favorite_languages = {
    'jennifer': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'fred': 'c#'
}
language = favorite_languages['sarah'].title()
print(f"Sarah's favorite language is {language}")

# using get() to Access Values
print('\n\033[1m' + 'Using get() to Access Values' + '\033[0m')
alien_0 = {'color': 'green', 'speed': 'slow'}
print("\n\033[1;3mprint(alien_0['points'])    # creates trace back error. No key-value points\033[0m")

point_value = alien_0.get('points', 'No point value assigned.')
print(point_value)

# Looping Through a Dictionary
print('\n\033[1m' + 'Looping Through a Dictionary' + '\033[0m')
# Looping Through All Key-Value Pairs
print('\n\033[1m' + 'Looping Through All Key-Value Pairs' + '\033[0m')

user_0 = {
    ' username': 'efermi',
    'first': 'enrico',
    'last': 'fermi'
}
for key, value in user_0.items():   # .items() to get key, value
    print(f"\nKey: {key}")
    print(f"Value: {value}")

# Looping Through All the Keys in a Dictionary: keys()
print('\n\033[1m' + 'Looping Through All the Keys in a Dictionary: keys()' + '\033[0m')

f_l = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python'
}

for name in f_l.keys():     # keys() might make code easier to read – but not necessary
    # could easily be written "for name in f_l:" and produce the same
    print(name.title())

# Looping Through a Dictionary's Keys in a Particular Order
print('\n\033[1m' + 'Looping Through a Dictionarys Keys in a Particular Order: sorted()' + '\033[0m')

for name in sorted(f_l.keys()):
    print(f"{name.title()}, thank you for taking the poll.")

# Looping Through All Values in a Dictionary
print('\n\033[1m' + 'Looping Through All Values in a Dictionary: values()' + '\033[0m')

print("The following languages have been mentioned:")
for value in f_l.values():
    print(value.title())

# Use set() when a list contains duplicate items. Python builds new set from items
print('\n\033[1m' + 'Use set() when a list contains duplicate items. Python builds new set from items' + '\033[0m')

for value in set(f_l.values()):
    print(value.title())

# Nesting, A list of Dictionaries
print('\n\033[1m' + 'Nesting, A list of Dictionaries' + '\033[0m')

alien_0 = {'color': 'green', 'points': 5}
alien_1 = {'color': 'yellow', 'points': 10}
alien_2 = {'color': 'red', 'points': 15}

aliens = [alien_0, alien_1, alien_2]

for alien in aliens:
    print(alien)

print('\n\033[1m' + '---------' + '\033[0m')

# Make an empty list for storing aliens.
aliens = []
# Makes 30 green aliens
for alien_number in range(30):
    new_alien = {'color': 'green', 'points': 5, 'speed': 'slow'}
    aliens.append(new_alien)
# change some to read

for alien in aliens[4:7]:
    alien['color'] = 'yellow'
    if alien['color'] == 'yellow':
        alien['color'] = 'red'
        alien['speed'] = 'fast'
        alien['points'] = 15
#change characteristics, green->yellow, speed change, points change
for alien in aliens[:3]:
    if alien['color'] == 'green':
        alien['color'] = 'yellow'
        alien['speed'] = 'medium'
        alien['points'] = 10
    elif alien['color'] == 'yellow':
        alien['color'] = 'red'
        alien['speed'] = 'fast'
        alien['points'] = 15

# Show the first five aliens
for alien in aliens[:5]:    # for each alien in list aliens, return first five [:5]
    print(alien)    # print first five
print("...")
# Show how many aliens have been created
print(f"\n\033[1mNumber of aliens created: {len(aliens)}\033[0m")

# A List in a Dictionary
print('\n\033[1m' + 'A List in a Dictionary' + '\033[0m')

# Store information about a pizza being ordered.
print('\n\033[1m' + 'Store information about a pizza being ordered.' + '\033[0m')
pizza = {
    'crust': 'thick',
    'toppings': ['mushrooms', 'extra cheese'],
}
# Summarize the order.
print(f"You ordered a {pizza['crust']}-crust pizza "
      f"with the following toppings:")
for topping in pizza['toppings']:
    print(f"\t{topping}")

# favorite_languages.py with added if statement
print('\n\033[1m' + 'favorite_languages.py with added if statement' + '\033[0m')
print('\n\033[1m' + 'Finally works!' + '\033[0m')
favorite_languages = {
    'sarah': ['c#', 'javascript'],
    'jennifer': ['python', 'pascal'],
    'edward': ['java'],
    'phil': ['python', 'c++']
}

for name, languages in favorite_languages.items():
    if len(languages) == 1:  # IF len() of languages True, execute 206-207
        print(f"{name.title()}'s favorite language is: ")
        for language in languages:
            print(f"\t{language.title()}")
    else:   # more than one language? Lines 209-212 are executed
        print(f"{name.title()}'s favorite languages are: ") # this line kept getting
        # printed for each language, because it was inside the for loop below.
        for language in languages:
            print(f"\t{language.title()}")

# A dictionary in a Dictionary
print('\n\033[1mA Dictionary in a Dictionary\033[0m')
users = {
    'aeinstein': {
        'first': 'albert',
        'last': 'einstein',
        'location': 'princeton',
    },
    # second dictionary starts:
    'mcurie': {
        'first': 'marie',
        'last': 'curie',
        'location': 'paris',
    }
}
for username, user_info in users.items():
    print(f"\nUsername: {username}")
    full_name = f"{user_info['first']} {user_info['last']}"
    location = user_info['location']

    print(f"\tFull name: {full_name.title()}")
    print(f"\tLocation: {location.title()}")


































































