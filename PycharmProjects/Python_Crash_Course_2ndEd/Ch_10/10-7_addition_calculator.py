"""10-7. Addition Calculator: Wrap your code from Exercise 10-6 in a while loop
so the user can continue entering numbers even if they make a mistake and enter
text instead of a number."""

print("Adding Numbers Together")
print("Press 'q' to exit.")

while True:
    first_number = input("Enter first number: ")
    if first_number == 'q':
        break

    second_number = input("Enter second number: ")
    if second_number == 'q':
        break

    try:
        answer = float(first_number) + float(second_number)
    except ValueError:
        print("Input only numbers, please. ")
    else:
        print(answer)