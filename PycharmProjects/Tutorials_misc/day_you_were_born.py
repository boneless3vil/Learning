# Code below created by open AI.
#   Takes your name and birthday and returns day of week you were born

import datetime

def day_of_birth(name, birth_date):
  # parse the birth date into a datetime object
  birth_date = datetime.datetime.strptime(birth_date, "%m/%d/%Y")

  # use the weekday() method to get the day of the week (0 = Monday, 6 = Sunday)
  day_of_week = birth_date.weekday()

  # convert the day of the week to a string (e.g. 0 -> "Monday")
  day_of_week_str = datetime.datetime.strftime(birth_date, "%A")

  # print the result
  print(f"{name}, you were born on a {day_of_week_str}.")

# prompt the user to enter their name and birth date
name = input("Enter your name: ")
birth_date = input("Enter your birth date (MM/DD/YYYY): ")

# call the day_of_birth function with the user-provided name and birth date
day_of_birth(name, birth_date)





































