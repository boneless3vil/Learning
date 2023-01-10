# page 209, 5833

def get_formatted_name(first, last, middle=''):
    """ Generate a neatly formatted full name."""
    if middle:
        full_name = f"{first.title()} {middle.title()} {last.title()}"
    else:
        full_name = f"{first.title()} {last.title()}"
    return full_name
