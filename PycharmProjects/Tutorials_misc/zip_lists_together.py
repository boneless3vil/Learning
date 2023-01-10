# use Python zip function to group lists  into one tuple
# Super Useful Python Function!! #python #programming #coding
# YouTuber: https://www.youtube.com/@b001
# from short: https://youtu.be/bMIcQt41hzU

# players inventory
items = [
    'mystic sword',
    'wooden shield',
    'rock'
]

rarity = [
    99,
    56,
    5
]

weight = [
    1.30,
    1.10,
    0.01
]

inv = zip(items, rarity, weight)
print(list(inv))

# reorder list as you like
inv = zip(items, weight, rarity)
print(list(inv))