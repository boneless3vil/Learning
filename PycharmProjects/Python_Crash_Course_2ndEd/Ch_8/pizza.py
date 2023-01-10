# pizza.py
# Python crash course, second edition
# chapter 8, page 146

def make_pizza(size, *toppings):
    """Summarize the pizza we are about to make."""
    print(f"\nMaking a {size}-inch pizza with the following toppings:")
    for topping in toppings:
        print(f"– {topping}")
