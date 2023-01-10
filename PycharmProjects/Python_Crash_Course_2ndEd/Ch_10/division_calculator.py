
print("Give me 2 numbers, and I'll divide them.")
print("Enter 'q' to quit.")

while True:
    first_number = input("\nFirst number: ")
    if first_number == 'q':
        break
    second_number = input("Second number: ")
    if second_number == 'q':
        break

    try:
        answer = float(first_number) / float(second_number)
    except ZeroDivisionError:
        print("You can't divide by zero!")
    else:
        print(answer)