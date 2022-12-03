# changing, adding and removing elements
"""
motorcycles = ['honda','suzuki','yamaha','kawasaki']
print(f"\n(Line 1) Original motorcycle list: {motorcycles}")

#modifying the elements in the list
motorcycles[0] = 'ducati'
print(f"\n(Line 6) Modifying the elements in a list: {motorcycles}")

#adding elements
motorcycles.append('harley davidson')
print(f"\n(Line 10) Adding elements to a list: {motorcycles}")

#building from an empty list
refrigerators = []
refrigerators.append('maytag')
refrigerators.append('viking')
refrigerators.append('kenmore')
refrigerators.append('LG')

print(f"\n(line 14) Building from an empty list: {refrigerators}")

#Inserting Elements into a List
motorcycles.insert(0,'triumph')
print(f"\n(Line 23) Inserting Elements into a List: {motorcycles}")

#Removing Elements from a List
del motorcycles[0]

print(f"\n(Line 27) Removing Elements into a List: {motorcycles}")
"""
#Removing LAST Item Using the pop() Method
"""
motorcycles = ['honda','suzuki','yamaha','kawasaki']

popped_motorcycle = motorcycles.pop()
print(f"\nRemoving and Item Using the pop() Method:")
print(f"\n\t(Line 32) motorcycles printed: {motorcycles}")
print(f"\n\t(Line 35) popped_motorcycle printed(note: removes last item by default): {popped_motorcycle}")

#Removing SPECIFIC Item Using the pop() Method
motorcycles = ['honda','suzuki','yamaha','kawasaki']

popped_motorcycle = motorcycles.pop(0)
print(f"\n\t(Line 40) Removing SPECIFIC Item Using the pop(<LIST NUMBER>) Method: {popped_motorcycle}")
"""

#Removing an Item by Value
"""
print(f"\nRemoving an Item by Value")
motorcycles = ['honda','suzuki','yamaha','kawasaki']
motorcycles.remove('yamaha')
print(motorcycles)

#remove an item by value in a separate list
too_expensive = 'suzuki'
motorcycles.remove(too_expensive)
print(motorcycles)
print(f"\n\tA {too_expensive} is too expensive for me.")
"""

#3-4 Guest list
"""
guests = ['CS Lewis', 'Jesus', 'Christopher Hitchens']

print(f"\n\tDear {guests[0]}, I would like to invite you to dinner.")
print(f"\n\tDear {guests[1]}, I would like to invite you to dinner.")
print(f"\n\tDear {guests[2]}, I would like to invite you to dinner.")
"""
#3-5 changing guest list
"""
#Jesus cannot attend
guests.remove('Jesus')
guests.insert(1,'Augustine')
print(f"\n\tDear {guests[1]}, Jesus could not attend. I would like you to come.")
print(f"\n\tline 74 {guests}")
#3-6 adding 3 more guests
guests.insert(0, 'Moses')
guests.insert(2, 'Paul')
guests.append('JRR Tolkien')

print(f"\n\tDear {guests[0]}, I would like to invite you to dinner.")
print(f"\n\tDear {guests[1]}, I would like to invite you to dinner.")
print(f"\n\tDear {guests[2]}, I would like to invite you to dinner.")
print(f"\n\tDear {guests[3]}, I would like to invite you to dinner.")
print(f"\n\tDear {guests[4]}, I would like to invite you to dinner.")
print(f"\n\tDear {guests[5]}, I would like to invite you to dinner.")
"""

#3-7 shrinking guest list
"""
not_coming = guests.pop()
print(f"\n\tDear {not_coming}, You can't come!")

not_coming = guests.pop()
print(f"\n\tDear {not_coming}, You can't come!")

not_coming = guests.pop()
print(f"\n\tDear {not_coming}, You can't come!")

not_coming = guests.pop()
print(f"\n\tDear {not_coming}, You can't come!")



print(f"\n\tDear {guests[0]}, I would like to invite you to dinner.")
print(f"\n\tDear {guests[1]}, I would like to invite you to dinner.")
# Empty out the list.
del(guests[0])
del(guests[0])

print(guests)
"""

# sorting a list permanently with sort() method
"""
cars = ['audi', 'zebra power']
print(cars)
cars.sort(reverse=True) #reverses order
print(cars)
"""

# Sorting a List Temporarily with the sorted() Function
"""
cars = ['BMW', 'Audi', 'Toyota']
print("Here is the original list:")
print(cars)

print("\nHere is the sorted list:")
print(sorted(cars))

print("\nHere is the original list again:")
print(cars)

#printing a list in reverse order

cars.reverse()
print(cars)

# len() to determine the number of items in a list.
len(cars)
"""

# 3-8 seeing the world
"""
travel_list = ['england', 'japan', 'australia', 'israel', 'france']
print("Raw list printed:")
print(f"\n\t{travel_list}")

# prints in reverse order, alphabetically
print(f"\nSorted list:")
print(f"\n\t{sorted(travel_list)}")
print(f"\n\tRaw again:")
print(f"\n\t{travel_list}")

# use reverse ()
print("\nList reversed:")
travel_list.reverse()
print(f"\n\t{travel_list}")
print(f"\n\tRaw again:")
travel_list.reverse()
print(f"\n\t{travel_list}")

# use sort ()
print("\nList sort():")
travel_list.sort()
print(f"\n\t{travel_list}")

travel_list.sort(reverse=True)
print(f"\n\tRaw again:")
print(f"\n\t{travel_list}")
"""

# 3-9 dinner guests
"""
guests = ['CS Lewis', 'Jesus', 'Christopher Hitchens']

print(f"\n\tDear {guests[0]}, I would like to invite you to dinner.")
print(f"\n\tDear {guests[1]}, I would like to invite you to dinner.")
print(f"\n\tDear {guests[2]}, I would like to invite you to dinner.")

print(f"\n Number of guests: {len(guests)}")
"""

# 3-10 Every Function "My list of movies"

movies = ['gladiator', 'star trek', 'indiana jones', 'lord of the rings']
print(f"Raw list: \n\t{movies}")
# starting with empty list
bad_movies = []
# sorted() function
print(f"\nSorted: \n\t{sorted(movies)}")
print(f"\nUnsorted again: \n\t{movies}")
# reverse()
print(f"Reversed list: ")
movies.reverse()
print(f"\t{movies}")
movies.reverse()
print(f"Raw list again: \n\t{movies}")
# append()
movies.append('matrix')
print(f"\nAppended Matrix: \n\t{movies}")
# insert()
movies.insert(1, 'hobbit')
print(f"\n Inserted Hobbit: \n\t{movies}")
# remove() – often used when you don't know the value of an item
print(f"\nRemoved Star Trek: ")
movies.remove('star trek')
print(f"\n\t{movies}")
# printing specific items from a list
print(f"\nThis movie is about the Romans: {movies[0].title()}")
print(f"This movie is last on the list: {movies[4].title()}")
# len()
print(len(movies))
# pop() then re-print len()
movies.pop()
print(len(movies))
# modify list
movies[0] = 'spartacus'
print(movies)


