
responses = {}  # empty dictionary

# Set a flag to indicate that polling is active.
polling_active = True   # flag to activate while loop

while polling_active:
    name = input("\nWhat is your name? ")
    response = input("Which mountain would you like to climb someday? ")
    # Store the response in the dictionary.
    responses[name] = response
    # Find out if anyone else is going to take the pull.
    repeat = input("Would you like to let another person respond? (Yes/No) ")
    if repeat == 'no':
        polling_active = False
     # Polling is complete. Show the results.
    print("\n--- Poll Results ---")
    for name, response in responses.items():
        print(f"{name.title()} would like to climb {response.title()}.")
























