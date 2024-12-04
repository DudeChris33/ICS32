# a2.py

# Chris Cyr
# cyrc@uci.edu
# 12436037

# L none -r -f -s -e
# C -n
# D
# R
# O

# E -usr -pwd -bio -addpost -delpost
# P -usr -pwd -bio -posts -post -all


import ui, Profile, pathlib
#ds_client, ds_protocol


def run(user: Profile.Profile, path: pathlib.Path):
    if user.username != "admin":
        user_input = ui.menu()
        if user_input == "Q":
            return
        if user_input == "1":
            user, path = ui.create_profile()
        elif user_input == "2":
            user, path = ui.open_profile(user, path)
        elif user_input == "3":
            user, path = ui.edit_profile(user, {}, path)
        elif user_input == "4":
            ui.write_post(user, path)
        elif user_input == "5":
            ui.remove_post(user. path)
        elif user_input == "6":
            pass
        elif user_input == "7":
            ui.print_profile(user, {})
        else:
            print("ERROR: Invalid input")
        print()

    else:
        print("Welcome to admin mode")
        user_input = input().split()
        if user_input[0] != "Q": assert len(user_input) > 1
        command, location, recursive, options = ui.admin_input(user_input)

        if command == "Q":
            return
        if command == "L":
            ui.list_folder_contents(location, recursive, options)
        elif command == "C":
            ui.create_file(location, options)
        elif command == "D":
            if ui.filetypecheck(location): ui.delete_file(location)
        elif command == "R":
            if ui.filetypecheck(location): ui.read_file(location)
        elif command == "O":
            if ui.filetypecheck(location): user, path = ui.open_profile(Profile.Profile().load_profile(str(location)), location)
        elif command == "E":
            if ui.filetypecheck(location): user, path = ui.edit_profile(Profile.Profile().load_profile(str(location)), options, location)
        elif command == "P":
            if ui.filetypecheck(location): ui.print_profile(Profile.Profile().load_profile(str(location)), options)
        else:
            print("ERROR: Invalid command")

    run(user, path)


if __name__ == "__main__":
    validuser = False
    while not validuser: user, validuser, path = ui.init()

    run(user, path)