# greet_users.py
# Python crash course, second edition
# chapter 8, page 142

def greet_users(names):
    """ print a simple greeting to each user in the list."""
    for name in names:
        msg = f"Hello, {name.title()}"
        print(msg)
usernames = ['hannah', 'ty', 'margot', 'moron']
greet_users(usernames)






