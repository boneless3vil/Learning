
beginning_list = ['item 1', 'item 2', 'item 3']
ending_list = []

while beginning_list:
    item_ending_list = beginning_list.pop() #each item popped out of beginning_list --> item_ending_list
    print(f"Item in ending_list: {item_ending_list}")   #print each item as it enters item_ending_list
    ending_list.append(item_ending_list)    # now add each item in that list to ending_list

print(f"\nEnding_list items:")
for e_u in ending_list: # grab each item in the list, one by one
    print(e_u.title())  # print each item














