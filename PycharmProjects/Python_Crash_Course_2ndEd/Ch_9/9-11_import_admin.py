"""9-11. Imported Admin: Start with your work from Exercise 9-8 (page 173).
Store the classes User, Privileges, and Admin in one module. Create a separate
file, make an Admin instance, and call show_privileges() to show that everything
is working correctly.
"""

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from user import Admin

jonathan = Admin('Jonathan', 'Baldwin', 'boneless3vil', 'jon@sinoverpi.com', 'Canyon Lake')
jonathan.describe_user()

jonathan_privileges = [
    'can add post',
    'can delete post',
    'can ban user'
    ]
jonathan.privileges.privileges = jonathan_privileges

print(f"\n{jonathan.username} has the following privileges:")
jonathan.privileges.show_privileges()


















