
"""9-14. Lottery: Make a list or tuple containing a series of 10 numbers and
five letters. Randomly select four numbers or letters from the list and print
a message saying that any ticket matching these four numbers or letters wins a
prize."""

from random import choice   #use "choice" for letters and numbers

lottery = (7, 420, 42, 69, 49,  911, 1945, 0, 51, 3, 'a', 'j', 'b', 'z', 'x')
winner = [] # list for random letters and numbers that were pulled

while len(winner) < 4:  #true until winner has 4 items
    pulled_item = choice(lottery)     # choose those items by random and put them in this list

    if pulled_item not in winner: # when lottery
        print(f"We pulled out a {pulled_item}!")
        winner.append(pulled_item)

