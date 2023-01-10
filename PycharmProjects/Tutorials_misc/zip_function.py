# tutorial on Python's zip function
# https://youtube.com/shorts/bMIcQt41hzU?feature=share

weapons = ['sword', 'chainsaw', 'staff']

strength = [45, 40, 10]

magic = [10, 15, 45]

weight = [12, 20, 20]

inv = zip(weapons, strength, magic, weight)
print(list(inv))