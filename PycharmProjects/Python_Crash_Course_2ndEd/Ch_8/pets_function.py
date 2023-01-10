

# takes an animal_type and pet_name then prints them out into separate sentences


def describe_pet(animal_type, pet_name):
    """ Display information about a Pet."""
    print(f"\nI have a {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name.title()}")

# describe_pet('Yorkshire Terrier', 'Bullet')