"""9-15. Lottery Analysis: You can use a loop to see how hard it might be to win
 the kind of lottery you just modeled. Make a list or tuple called my_ticket.
 Write a loop that keeps pulling numbers until your ticket wins. Print a message
  reporting how many times the loop had to run to give you a winning ticket. """

from random import choice   #use "choice" for letters and numbers

def get_winning_ticket(possibilities):
    """Return a winning ticket from a set of possibilities."""
    winning_ticket = []

    # We don't want to repeat winning numbers or letters, so we'll use a
    #   while loop.
    while len(winning_ticket) < 4:
        pulled_item = choice(possibilities)

        # Only add the pulled item to the winning ticket if it hasn't
        #   already been pulled.
        if pulled_item not in winning_ticket:
            winning_ticket.append(pulled_item)

    return winning_ticket


def check_ticket(played_ticket, winning_ticket):
    #check the items in return. false if not winning ticket 
    for element in played_ticket:
        if element not in winning_ticket:
            return False

    # must have a winning ticket
    return True


def make_random_ticket(possibilities):
    """ return a random ticket number from a list of possibilities"""
    ticket = []
    # don't repeat letters. Perhaps, use a wire loop
    while len(ticket) < 4:
        pulled_i = choice(possibilities)
        #only pull the item, if it's not already in ticket list
        if pulled_i not in ticket:
            ticket.append(pulled_i)

    return ticket

possibilities = (420, 42, 69, 49,  911, 'a', 'b', 'c', 'd')
winning_ticket = get_winning_ticket(possibilities)

plays = 0
won = False

# Let's set a max number of tries, in case this takes forever!
max_tries = 1_000_000

while not won:
    new_ticket = make_random_ticket(possibilities)
    won = check_ticket(new_ticket, winning_ticket)
    plays += 1
    if plays >= max_tries:
        break

if won:
    print("We have a winning ticket!")
    print(f"Your ticket: {new_ticket}")
    print(f"Winning ticket: {winning_ticket}")
    print(f"It only took {plays} tries to win!")
else:
    print(f"Tried {plays} times, without pulling a winner. :(")
    print(f"Your ticket: {new_ticket}")
    print(f"Winning ticket: {winning_ticket}")