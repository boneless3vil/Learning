# person.py
# Python crash course, 2nd edition
# chapter 8, page 139

def build_person(first_name, last_name, age=None):  # None --> used when
    #                            variable has no specific value assigned
    #                                a placeholder, like a False eval.
    # –--> Return a dictionary of information about a person. <---
    person = {'first': first_name, 'last': last_name}
    if age:
        person['age'] = age
    return person

musician = build_person('jimi', 'hendrix', age=27)
print(musician)

