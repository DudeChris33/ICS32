# a4.py

# Chris Cyr
# cyrc@uci.edu
# 12436037

# C:\Users\Christopher Cyr\Documents\School\First Year\Winter\ICS 32\a3\Chris.dsu

# server: 168.235.86.101
# port: 3021

# L none -r -f -s -e
# C -n
# D
# R
# O

# E -usr -pwd -bio -addpost -delpost
# P -usr -pwd -bio -posts -post -all


import ui, Profile, pathlib, os


def run(user: Profile.Profile, path: pathlib.Path):
    """
    Main program function, calls other functions as needed.
    """
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
            ui.send_post(user)
        elif user_input == "7":
            ui.print_profile(user, {})
        # elif user_input == "8":
        #     ui.weather_report()
        else:
            print("ERROR: Invalid input")
        print()

    else:
        user_input = input().split()
        if user_input[0] != "Q": assert len(user_input) > 1
        command, location, options = ui.admin_input(user_input)
        profile = Profile.Profile()
        profile.load_profile(pathlib.Path(os.path.join(".", "admin.dsu")))

        if command == "Q":
            return
        if command == "L":
            ui.list_folder_contents(location, options)
        elif command == "C":
            ui.create_file(location, options)
        elif command == "D":
            ui.delete_file(location)
        elif command == "R":
            ui.read_file(location)
        elif command == "O":
            user, path = ui.open_profile(profile, location)
        elif command == "E":
            user, path = ui.edit_profile(profile, options, location)
        elif command == "P":
            ui.print_profile(profile, options)
        else:
            print("ERROR: Invalid command")

    run(user, path)


if __name__ == "__main__":
    validuser = False
    while not validuser: user, validuser, path = ui.init()

    run(user, path)