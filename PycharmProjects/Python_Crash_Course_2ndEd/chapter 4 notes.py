


# chapter 4: working with lists

# RANGE()
# class range(stop)
# class range(start, stop[, step])
print("\n--- Range() function ---")
print("Syntax: class range(stop)")
print("Syntax: class range(start, stop[, step])\n")
numbers = list(range(1, 10, 2))
print(numbers)

# SLICING A LIST
print("\n--- SLICING A LIST --- (line 16)")
print("Syntax: start:stop:step")
# start:stop:step
players = ['charles', 'martina', 'michael', 'florence', 'eli']
print(players[0:4]) #make sure you use []
print(players[1:3]) # print 1-3
print(players[3:5]) # print 0-2 in list
print(players[-3:]) #print take from the end of the list
for player in players[:3]: # print only first three players
    print("This is a player: ")
    print(player.title())
print(players[:]) # print whole list
# copying a list
print("\nCopying a list (line 29)")
first_list = ['1st item', '2nd item', '3rd item']
second_list = first_list[:]
print(second_list)

# TUPLES
print("\n--- TUPLES --- (line 35)")
print("Syntax: list = (num1, num2, num3...)")
dimensions = (200, 50)  #tuple, and unchangeable value, using ()
print(dimensions[0])    # prints first index, same as when doing slicing from lists
print(dimensions[:])   # Prints all values
one_element_tuple = (3,)    # 1 element
print(one_element_tuple[0])

