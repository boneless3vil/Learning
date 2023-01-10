# Making a list of lines from a File

filename = 'pi_digits.txt'

with open(filename) as file_object:
    for line in file_object:
        print(line)     # calling print creates line spacing between each line
        # removed by adding  .rstrip()

""" can also be written with readlines()
with open(filename) as file_object:
    lines = file_object.readlines()

for lines in lines:
    print(line.rstrip())
"""