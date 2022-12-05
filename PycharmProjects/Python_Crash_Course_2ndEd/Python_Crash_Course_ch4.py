# Python Crash Course Chapter 4

# looping through an entire list
# for loops: most common programming to automate tasks
"""
magicians = ['alice', 'david', 'carolina']
temps = []
"""
# basically, "for every magician in the list magicians,the magicians name".
#   It will keep going through this loop until all the items on the list are
#   exhausted. naming conventions help with these temporary variables,
#   "for cat in cats", "for dog in dogs" and so on
"""
for magician in magicians:
   # print(magician)
# Doing More Work Within a for Loop
    print(f"{magician.title()}, that was a great trick!")
    print(f"I can't wait to see your next trick, {magician.title()}.\n")
"""
# doing something after a for loop
"""
print("Thank you, everyone. That was a great magic show!")
"""
# avoiding indentation errors– ONLY indent when you have a specific reason to
# do so the temporary variable "magician" can only be called within the for
# loop. See line 14 don't forget the ":" or you get a syntax error
"""
for magician in magicians:
print(f"{magician.title()} should produce an error") 
        #no indentation of print() produces an error

magicians = ['alice', 'david', 'carolina']
for magician in magicians:
       print(f"{magician.title()}, that was a great trick!")
  print(f"I can't wait to see your next trick, {magician.title()}.\n") 
    #indentation error created
"""

#4-1 Pizzas
"""
pizzas = ['cheese', 'pepperoni', 'mushroom', 'margherita']
for pizza in pizzas:
    print(pizza.title())
print("These are our pizzas")
"""

# 4-2 Animals
"""
animals = ['yorkshire terrier', 'chihuahua', 'labrador']
for animal in animals:
    print(f"\nA {animal.title()}, would make a good pet.")
"""

# MAKING NUMERICAL LISTS

# using the range() function
"""
for value in range(1, 5):
    print(value)    #notice: it does not print 5. Range starts counting at 1st value and stops at/before
    # 2nd value you give it
for value in range(1, 6):
    print(value)    #again, doesn't print 2nd value listed, but up to it
#pass range() starts the sequence at 0 and goes to the number value
for value in range(7):
    print(value)    # prints numbers 1-6
"""

# Using range() to make a list of numbers
"""
numbers = list(range (1, 6))
print(numbers)
# skip numbers in a given range() function
even_numbers = list(range(2, 11, 2))    #range(starting value, ending value, skip value)
print(even_numbers)
"""

# squaring numbers using **
"""
# squares every number between 1-10, prints values
squares = []
for value in range(1, 11):
    square = value ** 2
    squares.append(square)
print(squares)

# simplified code
squares = []
for value in range(1, 11):
    squares.append(value ** 2)
"""

# SIMPLE STATISTICS WITH A LIST OF NUMBERS
#List comprehensions – 1 line of code List!
"""
squares = [value**2 for value in range(1, 11)]  
    # NO colon with this simplified method
print(squares)
"""

# 4-3 counting to 20
"""
count = [value++1 for value in range(0, 20)]
print(count)
"""
# 4-4 1 million
"""
mil = [value++1 for value in range(0, 1_000_000)]
print(mil)
"""

# 4-5 summing a million
"""
mil = [value++1 for value in range(0, 1_000_000)]
print(f"Starting number: {min(mil)}")
print(f"\nMaximum number: {max(mil)}")
print(f"\nSum of all numbers from 1 to 1 million: {sum(mil)}")
"""
# 4-6 odd numbers: list of odd numbers from 1 to 20
"""
odds = [value+2 for value in range(1, 19, 2)]
print(odds)
"""

# 4-7 threes: list multiples of 3 from 3 to 30.
"""
threes = list(range(3, 31, 3))    #range(starting value, ending value, skip value)
print(threes)
"""

# 4-8 cubes: list 1st 10 cubes³ from 1 through 10
"""
cubes = [value**3 for value in range(1, 11)]
print(cubes)
"""

# 4-9 cube comprehension: list comprehension of 1st 10 cubes
"""
cube = [value**3 for value in range(1, 11)]
print(cube)
"""

#~ WORKING WITH PART OF A LIST

# slicing the list
"""
players = ['charles', 'martina', 'michael', 'florence', 'eli']
print(f"\nPlayers 1-3: {players[0:3]}") #did NOT print out last name
print(f"\nPlayers 2-4: {players[1:4]}")
print(f"\nPlayers 1-4: {players[:4]}") #omitting the 1st index, results: list starts at beginning
print(f"\nPlayers 3-5: {players[2:]}")
print(f"\nLast three players: {players[-3:]}") #using a negative number counts back from the LAST
                                                # item on the list
                                                """

# Looping through a slice
"""
players = ['charles', 'martina', 'michael', 'florence', 'eli']
print("Here are the first three players on my team:")
for player in players[:3]:
    print(player.title())
"""

# Copying a list
"""
my_foods = ['pizza', 'falafel', 'carrot cake']
friend_foods = my_foods[:]  # [:] tells Python: begin slice at 1st item
                            # — end with last item, a complete copy
print("My favorite foods are:")
print(my_foods)
print("\nMy friend's favorite foods are:")
print(friend_foods)
# proof they are 2 different lists:
my_foods.append('canoli')
print(f"\nMy favorite foods: \n{my_foods}")
print(f"\nMy friends favorite foods: ")
print(friend_foods)

friend_foods.append('ice cream')
print("\nMy favorite foods also include cannoli:")
print(my_foods)
print("\nMy friend's favorite foods also include ice cream:")
print(friend_foods)
"""

# 4-10 slices:
"""
list = ['item 1', 'item 2', 'item 3', 'item 4', 'item 5']
print("The 1st 3 items in the list are:\n")
print(list[0:3])

print("\n3 items from the middle of the list are:\n")
print(list[1:4])

print("\nThe last 3 items in the list are:\n")
print(list[2:5])
"""

# 4-11 my pizzas, your pizzas
"""
pizzas = ['cheese', 'pepperoni', 'mushroom', 'margherita']
friend_pizzas = pizzas[:] # Do NOT forget the [:] or every time you update the 
                          # 1st list, the 2nd list will gather the items as well

print("These are our pizzas:\n")
pizzas.append('goat cheese')
for pizza in pizzas:
    print(pizza.title())

friend_pizzas.append('tequila shot')
print("\nThese are my friends pizzas:\n")
for pizza in friend_pizzas:
    print(pizza.title())
"""

# 4-12 more loops
"""
my_foods = ['drop bears', 'gelato', 'cheese', 'tacos']
my_friends_foods = my_foods[:]

my_foods.append('flan')
print("My favorite foods:\n")
for my_food in my_foods:
    print(my_food)

my_friends_foods.append('liverwurst')
print("\nMy friend's favorite foods:\n")
for my_friends in my_friends_foods:
    print(my_friends)
"""

# TUPLES: creating lists that CANNOT change. "Immutable" but simple data
# structures

# defining a tuple: looks like a list, but uses (), NOT []
"""
dimensions = (200, 50)
print(dimensions[0])
print(dimensions[1])

# dimensions[0] = 250 #expected error: cause dimensions is defined as tuple

# NOTE: If you want to define a tuple with one element, you need to include a 
    # trailing comma: my_t = (3,)

# Looping through all values in the tuple
for dimension in dimensions:
    print(dimension)
# writing over a tuple
print("\nOriginal dimensions:")
for dimension in dimensions:
    print(dimension)

dimensions = (400, 100)     # reassigning a variable is valid, so no errors here
print("\nModified dimensions:")
for dimension in dimensions:
    print(dimension)
"""
# 4-13 Buffet:
"""
menu = ('double double', 'single single', 'milkshake', 'fries')
print("Menu items:\n")
for item in menu:
    print(item.title())
"""
#no indentation creates error
"""
menu.append('secret menu')
for item in menu:
    print(item.title())
"""

# update tuple list, the right way
"""
menu = ('double double', 'single single', 'coke', 'fries')
print("\nMenu items (updated):\n")
for item in menu:
    print(item.title())
"""

























