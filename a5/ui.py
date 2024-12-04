# ui.py

# Chris Cyr
# cyrc@uci.edu
# 12436037


from pathlib import Path
import os, Profile
import ds_client as dsc
from OpenWeather import OpenWeather


def init():
    """
    Initializes the interface by making the user pick an active profile.
    If user enters "admin", an admin profile will be created for them
    """
    print("Welcome to ICS 32 Journal")
    print("Enter Q at any time to exit the program\n")
    
    print("How would you like to get started?\n")
    print(" Q. Quit")
    print(" 1. Create a new Profile")
    print(" 2. Open an existing Profile\n")
    
    user_input = input()

    if user_input == "Q":
            quit()


    elif user_input == "1":
        user, path = create_profile()
        return user, True, path


    elif user_input == "2":
        print("Enter profile information\n")
        path = Path(input("Please enter the path to your profile\n"))
        if os.path.exists(path) and path.suffix == ".dsu":
            user = Profile.Profile()
            user.load_profile(path)
            print("Profile open.\n")
            return user, True, path
        else:
            print("Invalid profile")
            return None, False, None


    elif user_input == "admin":
        print("Welcome to admin mode")
        path = "."
        name = "admin.dsu"

        file = Path(os.path.join(path, name))

        if os.path.exists(file):
            user = Profile.Profile()
            user.load_profile(file)
            return user, True, file

        else:
            dsuserver = "168.235.86.101"
            username = "admin"
            password = "adminpassword"
            bio = ""

            user = Profile.Profile(dsuserver, username, password)
            user.bio = bio

            file.touch()
            user.save_profile(file)
            return user, True, file
    

    else:
        print("ERROR: Invalid option")
        return None, False, None

def menu():
    """
    Prints the main menu of the interface.
    """
    print("What would you like to do?\n")
    print(" Q. Quit")
    print(" 1. Create a new Profile")
    print(" 2. Open an existing Profile")
    print(" 3. Edit an existing Profile")
    print(" 4. Add an entry")
    print(" 5. Delete an entry")
    print(" 6. Post an entry online")
    print(" 7. Print profile contents")
    print(" 8. Weather report\n")
    return input()

def create_profile():
    """
    Asks the user for input to help make a new profile, returns the profile as well as the path to it
    """
    print("Enter new profile information\n")
    dsuserver = input("What DSU server would you like to use?\n")
    assert len(dsuserver.split()) <= 1
    username = input("What username would you like to use? (no spaces)\n")
    assert len(username.split()) <= 1
    password = input("What password would you like to use? (no spaces)\n")
    assert len(password.split()) <= 1
    bio = input("Enter a short description for your personal bio (press enter to leave blank)\n")
    path = input("Where would you like to store your profile? (enter a valid path)\n")
    assert os.path.exists(path)
    name = input("What name would you like to use for your profile?\n")
    assert len(path.split(".")) == 1

    user = Profile.Profile(dsuserver, username, password)
    user.bio = bio

    file = os.path.join(path, f"{name}.dsu")
    if os.path.exists(file):
        print("Profile already exists, opening instead\n")
        user = Profile.Profile()
        user.load_profile(file)
        return user, file

    else:
        Path(file).touch()
        user.save_profile(file)

        print("Profile created, opening\n")
        return user, file

def open_profile(user: Profile.Profile, path: Path):
    """
    Opens a profile given where it is.
    """
    if user.username != "admin":
        print("Enter profile information\n")
        path = Path(input("Please enter the path to your profile\n"))
        assert os.path.exists(path) and path.suffix == ".dsu"
        user.load_profile(path)
        print("Profile open.\n")
        return user, path
    
    else:
        assert os.path.exists(path) and path.suffix == ".dsu"
        user = Profile.Profile()
        user.load_profile(path)
        return user, path

def edit_profile(user: Profile.Profile, options: dict, path: Path):
    """
    Lets a user painstakingly edit their profile prompt by prompt
    """
    assert os.path.exists(path) and path.suffix == ".dsu"
    if user.username != "admin":
        print("Enter new profile information\n")
        dsuserver = input("What DSU server would you like to use? (press enter to leave blank)\n")
        username = input("What username would you like to use? (no spaces)\n")
        assert len(username.split()) == 1
        password = input("What password would you like to use? (no spaces)\n")
        assert len(password.split()) == 1
        bio = input("Enter a short description for your personal bio (press enter to leave blank)\n")

        user.dsuserver = dsuserver
        user.username = username
        user.password = password
        user.bio = bio
    
    else:
        if "-usr" in options: user.username = options['-usr']
        if "-pwd" in options: user.password = options['-pwd']
        if "-bio" in options: user.bio = options['-bio']
        if "-addpost" in options.keys(): user.add_post(Profile.Post(options["-addpost"]))
        if "-delpost" in options.keys(): user.del_post(options["-delpost"] - 1)

    user.save_profile(path)

    if user.username != "admin": print("Profile successfully edited.\n")
    return user, path

def write_post(user: Profile.Profile, path: Path):
    """
    Adds a post to the active profile given said profile and where it is stored
    """
    post = Profile.Post(input("What would you like to say?\n"))
    if len(post) > 0: user.add_post(post)
    user.save_profile(path)

def remove_post(user: Profile.Profile, path: Path):
    """
    Removes a post from the active profile given said profile and where it is stored
    """
    print("Which post would you like to delete?")
    i = 1
    for j in user.get_posts():
        print(f"{i}: {j}")
        i += 1
    post = input()
    try: post = int(post)
    except: raise TypeError
    user.del_post(post-1)
    user.save_profile(path)
    print(f"Post {post} deleted")

def send_post(user: Profile.Profile):
    """
    Gathers the necessary information to send a post to the server before using the ds_client module to send it.
    """
    if user.username != "admin":
        assert len(user.dsuserver.split(".")) > 1
        port = input("What server port would you like to connect to?\n")
        try: port = int(port)
        except: raise ValueError
        assert port == 3021
        print("Which post would you like to send to the server?\n")
        print("0: None")
        [print(f"{i+1}: {user._posts[i]['entry']}") for i in range(len(user._posts))]
        try: postid = int(input())
        except: raise TypeError
        messages = [j for j in user._posts]
        if postid == 0:
            postid = 1
            messages = [None, None]
        send_bio = input("Would you like to post your bio? (y/n)\n")
        if send_bio == "y":
            if dsc.send(user.dsuserver, port, user.username, user.password, messages[postid-1], user.bio): print("Successfully sent to server")
            else: print("Something went wrong")
        elif send_bio == "n" and messages[0] != None:
            if dsc.send(user.dsuserver, port, user.username, user.password, messages[postid-1], None): print("Successfully sent to server")
            else: print("Something went wrong")
        
        return

def print_profile(user: Profile.Profile, options: dict):
    """
    Prints the contents of a profile given the profile and what is to be printed
    """
    if user.username != "admin":
        print("What would you like to print? (enter choices lowest to highest without spaces)\n")
        print(" 1. Username")
        print(" 2. Password")
        print(" 3. Bio")
        print(" 4. All posts")
        print(" 5. A specific post")
        print(" 6. Everything\n")
        choices_input = input()
        choices_output = []
        for i in range(len(choices_input)):
            choices_output.append(choices_input[i])

        if "1" in choices_output:
            print(f"Username:\n{user.username}")
        if "2" in choices_output:
            print(f"Password:\n{user.password}")
        if "3" in choices_output:
            print(f"Bio:\n{user.bio}")
        if "4" in choices_output:
            print("Posts:")
            [print(f"{i+1}: {user._posts[i]['entry']}") for i in range(len(user._posts))]
        if "5" in choices_output:
            try: post = int(input("Which post would you like to print?\n"))
            except: raise TypeError
            print(user._posts[post-1]['entry'])
        if "6" in choices_output:
            print(f"Username:\n{user.username}")
            print(f"Password:\n{user.password}")
            print(f"Bio:\n{user.bio}")
            print("Posts:")
            [print(f"{i+1}: {user._posts[i]['entry']}") for i in range(len(user._posts))]
