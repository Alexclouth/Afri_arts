#!/usr/bin/python3
""" Test delete feature
"""
from models.engine.file_storage import FileStorage
from models.user import User

fs = FileStorage()

# All States
all_user = fs.all(User)
print("All User: {}".format(len(all_user.keys())))
for user_key in all_user.keys():
    print(all_user[user_key])

# Create a new User
new_user = User()
new_user.name = "California"
fs.new(new_user)
fs.save()
print("New user: {}".format(new_user))

# All States
all_user = fs.all(User)
print("All User: {}".format(len(all_user.keys())))
for user_key in all_user.keys():
    print(all_user[user_key])

# Create a new User
new_user = User()
new_user.name = "California"
fs.new(new_user)
fs.save()
print("New user: {}".format(new_user))

# All States
all_user = fs.all(User)
print("All User: {}".format(len(all_user.keys())))
for user_key in all_user.keys():
    print(all_user[user_key])


# Delete the new State
fs.delete(new_user)

# All States
all_user = fs.all(User)
print("All User: {}".format(len(all_user.keys())))
for user_key in all_user.keys():
    print(all_user[user_key])

