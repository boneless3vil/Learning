# function:  send_messages() -> prints each text message
#   2: after printing, sends each message to sent_messages()
#   3: print each list to show the messages have been moved

def show_messages(messages):
    # print original list
    print("Showing all messages:")
    for message in messages:
        print(message)


def send_messages(messages, sent_messages):
    #   move messages to new list
    print("\nPrinting all messages:")
    while messages:
        current_messages = messages.pop()
        print(current_messages)
        sent_messages.append(current_messages)

messages = ['Hello!', 'No. Not me.', 'Will you go?']
show_messages(messages)

# set new list at empty
sent_messages = []
send_messages(messages[:], sent_messages)
    # function call with a copy * sliced * of the list of messages

print("\nFinal lists:")
print(messages)
print(sent_messages)







