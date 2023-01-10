# printing_models.py
# Python crash course, second edition
# chapter 8, page 142

unprinted_designs = ['1', '2', '3']
completed_models = []

# simulate printing each design, until none are left.
# Move each design to completed_models after printing.
while unprinted_designs:
    current_design = unprinted_designs.pop()
    print(f"Printing model: {current_design}")
    completed_models.append(current_design)

# Display all completed models.
print("\nThe following models have been printed:")
for completed_model in completed_models:
    print(completed_model)
