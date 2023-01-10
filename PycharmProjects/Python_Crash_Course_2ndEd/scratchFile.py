


# 1) Complete the function to return the result of the conversion
def convert_distance(miles):
	km = miles * 1.6  # approximately 1.6 km in 1 mile
	return km

my_trip_miles = 55

# 2) Convert my_trip_miles to kilometers by calling the function above
my_trip_km = convert_distance(my_trip_miles)

# 3) Fill in the blank to print the result of the conversion
print(f"The distance in kilometers is " + str(my_trip_km))

# 4) Calculate the round-trip in kilometers by doubling the result,
#    and fill in the blank to print the result
print("The round-trip in kilometers is " + str((my_trip_km)*2))


# IF AND ELSE STATEMENTS
# ELSE statement not necessary if all you need to do is return false:
prompt = input("Enter a number: ")
number2 = int(prompt)

def even_odd(number):
    if number % 2 == 0:
#        print("The number is even.")
        return True
    return False    # else: statement not necessary when you're just returning False
#    else:
#        print("The number is odd.")

even_odd(number2)




























