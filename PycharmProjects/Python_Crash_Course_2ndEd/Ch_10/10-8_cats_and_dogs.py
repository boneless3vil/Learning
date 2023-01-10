"""10-8. Cats and Dogs: Make two files, cats.txt and dogs.txt. Store at least
three names of cats in the first file and three names of dogs in the second
file. Write a program that tries to read these files and print the contents of
the file to the screen. Wrap your code in a try-except block to catch the
FileNotFound error, and print a friendly message if a file is missing. Move one
of the files to a different location on your system, and make sure the code in
the except block executes properly."""

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
    print(f"File not found. Please check your spelling.")






