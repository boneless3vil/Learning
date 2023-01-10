

# alien movement
print('\n\033[1m' + 'Alien Movement' + '\033[0m')
alien_0 = {'x_position': 0,
           'y_position': 25,
           'speed': 'medium'}
print(f"Original position: {alien_0['x_position']}")

# Move the alien to the right.
#   Determine how far to move the alien based on its current speed.
if alien_0['speed'] == 'slow':  # dict[Key] == Value
    x_increment = 1
if alien_0['speed'] == 'medium':    # dict[Key] == Value
    x_increment  = 2
else:
    # alien must be going fast
    x_increment = 3

# The new position is the old position plus the increment
alien_0['x_position'] = alien_0['x_position'] + x_increment
print(f"New position: {alien_0['x_position']}")

# my poisonous pizza
print('\n\033[1m' + 'Poisoned Pizza' + '\033[0m')
pizza = {'flavor': 'pepperoni',
         'size': 'small',
         'chef': 'leonardo'}
if pizza['flavor'] == 'vegetarian':
    print(f"Pizza does not have poison.")
if pizza['size'] == 'small':
    print("Warning: this pizza is poisonous")



