# formatted_name.py
# Python crash course, 2nd edition
# chapter 8, page 136

def get_formatted_name(first_name, last_name):
    """ Return a full name, neatly formatted."""
    full_name = f"{first_name} {last_name}"
    return full_name.title()    # returns data collected in musician var

musician = get_formatted_name('jimi', 'hendrix')
print(musician)     #outside the def, Jimi Hendrix is returned to musician where it can be printed















