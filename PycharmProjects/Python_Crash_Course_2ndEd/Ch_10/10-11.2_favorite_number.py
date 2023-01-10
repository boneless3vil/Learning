"""10-11. Favorite Number: Write a program that prompts for the user’s favorite
number. Use json.dump() to store this number in a file. Write a separate program
that reads in this value and prints the message, “I know your favorite number!
It’s _____.”"""
import json

filename = 'favoritenumber.txt'

with open(filename) as f:
    favoritenumber = json.load(f)

print(f"I know your favorite number! It's {favoritenumber}.")
    


