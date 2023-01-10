
def bill(sub, tip):
    print("The cost for each of you: " + str(((sub * tip) + sub)/2))
    print("Oh,...and here is the square root of your total bill: " + str((((sub * tip) + sub)/2) ** (1/2)))
bill(100, 0.15)

def covert_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds - hours * 3600) // 60
    remaining_seconds = (seconds - hours * 3600) // 60
    return hours, minutes, remaining_seconds

hours, minutes, seconds = convert_seconds(5000)
print(hours, minutes, seconds)

# quiz or w/e
def calculate_storage(filesize):
    block_size = 4096
    # Use floor division to calculate how many blocks are fully occupied
    full_blocks = filesize // block_size
    # Use the modulo operator to check whether there's any remainder
    partial_block_remainder = block_size % filesize
    # Depending on whether there's a remainder or not, return
    # the total number of bytes required to allocate enough blocks
    # to store your data.
    if partial_block_remainder > 0:
        return 8192
    return 4096

print(calculate_storage(1))    # Should be 4096
print(calculate_storage(4096)) # Should be 4096
print(calculate_storage(4097)) # Should be 8192
print(calculate_storage(6000)) # Should be 8192


# name format function
def format_name(first_name, last_name):
	# code goes here
	if len(last_name) > 0:
		print("Name: " + last_name + ", " + first_name)
    elif not last_name:
		print("Name: " + first_name)
	elif not first_name:
		print("Name: " + last_name)
	else:
		print("")
	return string

print(format_name("Ernest", "Hemingway"))
# Should return the string "Name: Hemingway, Ernest"

print(format_name("", "Madonna"))
# Should return the string "Name: Madonna"

print(format_name("Voltaire", ""))
# Should return the string "Name: Voltaire"

print(format_name("", ""))
# Should return an empty string

# module test question
def fractional_part(numerator, denominator):
    # Operate with numerator and denominator to
    if denominator != 0:
        return (numerator / denominator) % 1    # use the "% 1" to strip
        #                                       remainder off whole number
    # keep just the fractional part of the quotient
    return 0

print(fractional_part(5, 5)) # Should be 0
print(fractional_part(5, 4)) # Should be 0.25
print(fractional_part(5, 3)) # Should be 0.66...
print(fractional_part(5, 2)) # Should be 0.5
print(fractional_part(5, 0)) # Should be 0
print(fractional_part(0, 5)) # Should be 0

# week 3: while loops
def attempts(n):
    x = 1
    while x >= n:
        print("Attempt" + str(x))
        x += 1  #  the += expression translates the line into x = x+ 1

# the function below does not properly initialize start_number
def count_down(start_number):
  current = start_number    # <-- this line needed to initialize function
  # try to use a variable without first initializing it, you'll run into
  # a NameError
  while (current > 0):
    print(current)
    current -= 1
  print("Zero!")

count_down(3)
count_down(5)

# Infinite loops

# first example: infinite loop
while x == 2 % 0:
    x = x/2
# fixed, using IF statement
if x != 0:
    while x % 2 == 0:
        x = x / 2

# another infinite loop
def print_range(start, end):
	# Loop through the numbers from start to end
	n = start
	while n <= end:
		print(n)
		n += 1  # without this line, infinite loop goes

# week 3: while loops, infinite loops quiz

def sum_divisors(n):
  sum_n = 0
  div = 1  # smallest divisor for a number
  # Return the sum of all divisors of n, not including n
  while div < n:    # largest dvisor is always n
    if n % div == 0:    # infinite loop check
      sum_n += div    # sum = sum + div
    div += 1        # div = div + 1
  return sum_n


print(sum_divisors(1))
# 0
print(sum_divisors(3)) # Should sum of 1
# 1
print(sum_divisors(36)) # Should sum of 1+2+3+4+6+9+12+18
# 55
print(sum_divisors(102)) # Should be sum of 2+3+6+17+34+51
# 114

# -----
# Not sure whether to use a for loop or a while loop? Remember that a while
# loop is great for performing an action over and over until a condition has
# changed. A for loop works well when you want to iterate over a sequence of
# elements.

# convert Fahrenheit to Celsius, iterate a range from 0-100, in blocks of 10
def to_Celsius(n):
    return (n - 32) * 5 / 9
for n in range(0, 226, 10):
    print(n, to_Celsius(n))


# To quickly recap the range() function when passing one, two, or three
# parameters:
#   One parameter will create a sequence, one-by-one, from zero to one less
#   than the parameter.
#
#   Two parameters will create a sequence, one-by-one, from the first parameter
#   to one less than the second parameter.
#
#   Three parameters will create a sequence starting with the first parameter
#   and stopping before the second parameter, but this time increasing each
#   step by the third parameter.

# nested for loops can greatly slow down a computer

for x in [25]:  # using [] by themselves creates list in this case. Very cool!
    print(x)

# common in error in a for loop
def greeting_friends(friends):
    for friend in friends:
        print("hi " + friend)

greeting_friends(['Taylor', 'Louisa', 'Jamaal', 'Eli'])
greeting_friends('Schwarzenegger')  # prints each and every letter. This is
#   because it's not in a list.

# FOR loops:  iterates over a sequence of elements, executing the body of the
# loop for each element in the sequence.

# WHILE loops: used when there’s an unknown number of operations to be
# performed, and a condition needs to be checked at each iteration.

# RANGE() function: generates a sequence of integer numbers.
#   It can take one, two, or three parameters:
#   range(start, end, interval)


#


