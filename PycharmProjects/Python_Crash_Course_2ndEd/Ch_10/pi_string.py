# working with a file's contents

filename = 'pi_million_digits.txt'

with open(filename) as file_object:
    lines = file_object.readlines()

pi_string = ''  # lines 8-10, store the file in this string, then strip the
# extra spaces added using readlines()
for line in lines:
    pi_string += line.strip()

# now print the string.
print(f"{pi_string[:52]}...")
print(len(pi_string))

