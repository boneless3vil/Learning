# takes a number and squares it, returns the number
def ex_number(number, exp):
    number = number ** exp
    print(number)

ex_number(3, 3)
ex_number(5, 3)
ex_number(3, 5)
ex_number(0.5, 3)
ex_number(103, 1/2)

# takes a number and sums up all the preceding numbers starting from zero, but not
# including final number
def sum_of_number(number):
    n2 = 0
    while n2 < (number - 1):
        n2 += 1
        print(n2)

sum_of_number(5)


# takes a file name, checks for *.PDF ext and changes it to *.lol
def pdf_to_lol(file):
    if *.pdf:




