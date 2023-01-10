"""10-9. Silent Cats and Dogs: Modify your except block in Exercise 10-8 to fail
silently if either file is missing."""

file_cats = 'cats.txt'
file_dogs = 'dogs.txt'
file_giraffes = 'giraffes.ext'  #this file produces error

try:
    with open('cats.txt') as cats:
        contents = cats.read()
    print(contents)

    with open('dogs.txt') as dogs:
        contents = dogs.read()
    print(contents)

    with open('giraffes.txt') as g:
        contents = g.read()
except FileNotFoundError:
    pass
