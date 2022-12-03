"""
prompt = "\nTell me something, and I will repeat it back to you:"
prompt += "\nEnter 'quit' to end the program. "
message = ""     # empty variable message to keep track of whatever user input
while message != 'quit':    # checks message for "quit". If NO, continues loop
    message = input(prompt) #
    print(message)
"""
# ISSUE: Prince the word 'quit' as actual message. Simple IF test fix that
"""
prompt = "\nTell me something, and I will repeat it back to you:"
prompt += "\nEnter 'quit' to end the program. "     # += adds message to end of line above

message = ""
while message != 'quit':       # as long as the message doesn't say QUIT, any input will be printed
    message = input(prompt)  #– remember, input at prompt, not message.
    print(message)
"""

# Using flags: many events could cause a program to stop running: your player
# ran out of ships or all your cities were destroyed.

# A flag variable can determine whether the ENTIRE program is active.

prompt = "\nTell me something, and I will repeat it back to you:"
prompt += "\nEnter 'quit' to end the program. "

active = True   # flag sets program to active
while active:
    message = input(prompt)
# IF check ends program if message changes to "quit"
    if message == 'quit':
        active = False
    else:
        print(message)
















