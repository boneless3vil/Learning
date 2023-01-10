# Python extend function
# https://youtube.com/shorts/YjV3_rcUxg4?feature=share

""" a player with an inventory, stumbles upon a chest. They pick up the items
in the chest"""

inventory = [
    'Mystic Sword',
    'Sword of Destiny',
    'mana potion',
    'gold'
]

chest = [
    'gold',
    'broken rifle',
    'clothing',
    'hotdogs'
]

inventory.extend(chest)
print(inventory)