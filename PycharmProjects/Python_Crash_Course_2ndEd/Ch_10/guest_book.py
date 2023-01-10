


filename = 'guest_book.txt'

print("(Press 'q' to quit.) ")
while True:
    name = input("What is your name? ")
    if name == 'q':
        break
    else:
        with open(filename, 'a') as f:
            f.write(f"{name}, ")
        print(f"Hello, {name}! You have been added to the guestbook.")




