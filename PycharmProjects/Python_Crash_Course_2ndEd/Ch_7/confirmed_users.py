
# Start with users that need to be verified,
#   and an empty list to hold confirmed users.

unconfirmed_users = ['alice', 'brian', 'candace']
confirmed_users = []

# Verify each user until there are no more unconfirmed users.
#   Move each verified user into the list of confirmed users.

while unconfirmed_users:    # while unconfirmed_users has items in it
    current_user = unconfirmed_users.pop()  # pop() items out, last to 1st, add them to current_user
    print(f"Verifying user: {current_user}")    # print each item
    confirmed_users.append(current_user)    # move each item to empty list

# Display all confirmed users.
print(f"\nThe following users have been confirmed:")
for confirmed_user in confirmed_users:  # for each item in new list
    print(confirmed_user.title())       #print each item
