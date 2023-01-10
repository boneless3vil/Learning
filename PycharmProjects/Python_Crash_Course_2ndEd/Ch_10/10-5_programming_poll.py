

filename = 'programming_poll.txt'

print("Welcome to the programming poll!")
print("(Press 'q' to quit.) ")

reasons = []

while True:

    reason = input("Why do you like programming? ")
    reasons.append(reason)

    continue_poll = input("Would anyone else like to take the poll? (y/n): ")
    if continue_poll != 'y':
        break

with open(filename, 'a') as f:
    f.write(f"{reasons}, ")
    print(f"Thank you! Your answer has been recorded.")





