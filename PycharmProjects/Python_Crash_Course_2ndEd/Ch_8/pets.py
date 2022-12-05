# pets.py
# Python crash course, 2nd edition
# chapter 8

def describe_pet(animal_type, pet_name):
    """ Display information about a Pet."""
    print(f"\nI have a {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name.title()}")

describe_pet('hamster', 'harry')
# multiple function calls
describe_pet('dog', 'willie')
# remember to order correctly!
describe_pet('fluffy', 'cat')   # a fluffy named cat? incorrect, obviously
# Keyword Arguments
describe_pet(animal_type='horse', pet_name='larry')










