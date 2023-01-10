"""10-12. Favorite Number Remembered: Combine the two programs from Exercise
10-11 into one file. If the number is already stored, report the favorite number
to the user. If not, prompt for the user’s favorite number and store it in a
file. Run the program twice to see that it works."""

import json

try:
    # tries to read file for favorite number
    with open('favorite_number.json') as fn:
        favorite_number = fn.read()

except FileNotFoundError:
    # if file not for, asks for favorite number
    answer = input("What is your favorite number? ")
    # if file exists, but nothing is in it, script won't work correctly
    with open('favorite_number.json', 'w') as fn:
        json.dump(answer, fn)
        print("I will remember your favorite number.")

else:
    print(f"I know your favorite number. It's {favorite_number}!")
