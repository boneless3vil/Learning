"""9-12. Multiple Modules: Store the User class in one module, and store the
Privileges and Admin classes in a separate module. In a separate file, create
an Admin instance and call show_privileges() to show that everything is still
working correctly."""

from admin import Admin

jon = Admin('Jonathan', 'Baldwin', 'boneless3vil', 'jon@sinoverpi.com', 'Canyon Lake')
jon.describe_user()

jon_p = [      # 2nd username used to store privileges only
    'can add post',
    'can delete post',
    'can ban user'
]

jon.privileges.privileges = jon_p

print(f"\nThe admin {jon.username} has these privileges:")
jon.privileges.show_privileges()    # as seen here, main username used to access
#   provisions, not 2nd username




















