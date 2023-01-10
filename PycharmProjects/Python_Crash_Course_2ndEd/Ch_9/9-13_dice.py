
"""9-13. Dice: Make a class Die with one attribute called sides, which has a
default value of 6. Write a method called roll_die() that prints a random
number between 1 and the number of sides the die has. Make a 6-sided die and
roll it 10 times. Make a 10-sided die and a 20-sided die. Roll each die 10
times.
"""

from random import randint

class Die:

    def __init__(self, sides=6):
        self.sides = sides

    def roll_die(self):
        return randint(1, self.sides)

d6 = Die()

results = []
for num in range(10):
    result = d6.roll_die()
    results.append(result)

print("The results from 10-d6 rolls:")
print(results)

# 10-sided die

d10 = Die(sides=10)

results = []
for num in range(10):
    result = d10.roll_die()
    results.append(result)

print("\nThe results from 10-d10 rolls:")
print(results)

# 20-sided die

d20 = Die(sides=20)

results = []
for num in range(10):
    result = d20.roll_die()
    results.append(result)

print("\nThe results from 10-d20 rolls:")
print(results) 