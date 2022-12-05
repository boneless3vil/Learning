# greeter_2.py
# Python crash course, 2nd edition
# chapter 8, page 141
"""
def get_formatted_name(first_name, last_name):
    # --> Return a full name, neatly formatted. <--
    full_name = f"{first_name} {last_name}"
    return full_name.title()
# This is an infinite loop!
while True:
    print("\nPlease tell me your name:")
    f_name = input("First name: ")
    l_name = input("Last name: ")
    formatted_name = get_formatted_name(f_name, l_name)
    print(f"\nHello, {formatted_name}!")
"""

# page 141 solution
def get_formatted_name(first_name, last_name):
    # --> Return a full name, neatly formatted. <--
    full_name = f"{first_name} {last_name}"
    return full_name.title()
# infinite loop FIXED!
while True:
    print("\nPlease tell me your name:")
    # add quit statement
    print("(enter 'q' at any time to quit)")
    f_name = input("First name: ")
    # IF statement to quit on 1st name line
    if f_name == 'q':
        break
    # IF statement to quit on last name line
    l_name = input("Last name: ")
    if l_name == 'q':
        break
    formatted_name = get_formatted_name(f_name, l_name)
    print(f"\nHello, {formatted_name}!")





























