
filename = 'learning_python.txt'

with open(filename) as f:
    lines = f.readlines()

for line in lines:
    print(line.rstrip().replace('Python', 'C#'))


