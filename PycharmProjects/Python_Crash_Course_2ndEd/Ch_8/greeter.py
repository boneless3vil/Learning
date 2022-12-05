# greeter.py
# Python crash course, 2nd edition
# chapter 8
"""
def greet_user():   # function definition name():
    # anything indented after the definition, called docstrings, make up
    #   body of function"""
    # """Display a simple greeting."""
"""    print("Hello!")

greet_user()    # call the function with its name
"""
# Passing information to a function
#   – Using above def, pass information into function– > enter username into ()

def greet_user(username):   # 'username' = parameter
    #   'greet_user' = function
    # """ display a simple greeting"""
    print(f"Hello, {username.title()}")

greet_user('jesse')     # 'jesse' = argument

# arguments and parameters
#   – greeter.py use of user name = "parameter"
#       – the value 'jesse' = argument
#       – essentially: 'jesse' passed to the function greed_user() and the
#           value assigned to the perimeter' username'



















