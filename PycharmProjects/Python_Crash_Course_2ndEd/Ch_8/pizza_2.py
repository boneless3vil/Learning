# pizza.py
#Python crash course, second edition
# chapter 8, page 146

def make_pizza(*toppings):
    """Summarize the following pizza"""
    print("\nMaking a pizza with the following toppings:")
    # replace the print() call with a loop. Function responds better, no matter the number of values
    for topping in toppings:
        print(f"- {topping}")

make_pizza('pepperoni')
make_pizza('mushrooms', 'green peppers', 'extra cheese')




