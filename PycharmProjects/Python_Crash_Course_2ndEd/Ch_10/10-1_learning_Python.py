
filename = 'learning_python.txt'

print("— Contents printed by reading entire file:")
with open(filename) as file_object:
    contents = file_object.read()
print(f"    – {contents}")

print("— Print by looping over the file object:")
with open(filename) as file_object:
    for line in file_object:
        print(f"    – {line.strip()}")

print("\n— Store the lines in a list and then work with them outside the with block")
with open(filename) as file_object:
    lines = file_object.readlines()

for line in lines:
    print(f"    – {line.strip()}")
