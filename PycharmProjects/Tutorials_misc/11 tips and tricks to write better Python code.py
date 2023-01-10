# 11 tips and tricks to write better Python code
# https://youtu.be/8OKTAedgFYg

# 2: Use List Comprehensions Instead of FOR raw loops
squares =  []
for i in range(10):
        squares.append(i*i)

print(squares)
# List Comprehension method
squares = [i*i for i in range(0,1_100,50)]
print(squares)

# 3: Sort complex deliverables with sorted()
data = [3, 5, 1, 10, 9]     # Can do the same with a tuple
sorted_data = sorted(data)
# or reversed
sorted_data_reversed = sorted(data, reverse=True)

print(f"\nThis is sorted: {sorted_data}\nThis is the same, but"
      f" in reverse: {sorted_data_reversed}")
# or with a dictionary
data = [{"name": "Max", "age": 6},
        {"name": "Lisa", "age": 20},
        {"name": "Ben", "age": 9}]

sorted_data = sorted(data, key=lambda x: x["age"])  #1 line function that
# returns age. I'm not sure why "lambda" is used
print(sorted_data)


# 4: Store unique values with sets
my_list = [1, 2, 3, 4, 5, 6, 7, 7, 7]
my_set = set(my_list)  # a SET is a on ordered list that REMOVES duplicate items
print(my_set)   # notice that duplicate 7's are not printed

primes = {2, 3, 5, 7, 11, 13, 17, 19}   # using curly braces here allows
#   Python to do more, but what? Need to look up {} with lists, dictionaries, etc.
print(primes)

# 5: Save memory with generators
import sys

my_list = [i for i in range(10_000)]
print(sum(my_list))
print(sys.getsizeof(my_list), "bytes")

my_gen = (i for i in range(10_000))
print(sum(my_gen))
print(sys.getsizeof(my_gen), "bytes")


# 6: Define default values in dictionaries with .get() and .setdefault()
my_dict = {'item': 'football', 'price': 10.00}
count = my_dict.get('count', 0) # this gets the count, but if you add the zero
# after the ",", it sets the default?
print(count)

count = my_dict.setdefault('count', 0)  # sets default count
print(count)
print(my_dict)

# 7: Count hashable objects with collections.counter.
from collections import Counter # import this to count items, similar to a
# set with duplicate items, but this will return with ({"item: count})

my_list = [10, 10, 10, 5, 5, 2, 9, 9, 9, 9, 9, 9]
counter = Counter(my_list)

print(counter)
print(counter[10])  # assess count of individual items with []
# Use most_common to list the items, in this example,
# from most common to least common
most_common = counter.most_common()
print(most_common)
print(most_common[0][0])  # returns most common item "9" and not count


# 8: format strings with f"string"
name = "Alex"
my_string = f"Hello {name}"
print(my_string)
# a) write expressions that will be evaluated at runtime
i = 10
print(f"{i} squared is {i*i}")

#9: concatenate string with .join()
list_of_strings = ['Hello', 'my', 'friend']
# BAD way! VERY slow for large lists
my_string = ""
for i in list_of_strings:
    my_string  += i + " "
print(my_string)
# GOOD: use.join(), faster, more concise joining of list items
my_string = " ".join(list_of_strings)
print(my_string)

# 10: merge 2 dictionaries (Python 3.5+)
d1 = {"name": "Alex", "age": 25}
d2 = {"name": "Alex", "city": "New York"}
merged_dict = {**d1, **d2}
print(merged_dict)

# 11: simplify IF statement for multiple checks
colors = ['red', 'green', 'blue']
# WRONG way.
c ="red"
if c == "red" or c == "green" or c == "blue":
    print(f"{c} is main color")
# CORRECT way
if c in colors:
    print(f"{c} is main color")
































































