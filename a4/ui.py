# ui.py

# Chris Cyr
# cyrc@uci.edu
# 12436037


from pathlib import Path
import os, Profile
import ds_client as dsc
from WebAPI import WebAPI
from OpenWeather import OpenWeather
from LastFM import LastFM


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
    # print(" 8. Weather report\n")
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
        try: len(str(user.dsuserver.split("."))) > 1
        except:
            print("Invalid dsuserver, defaulting to 168.235.86.101")
            user.dsuserver = "168.235.86.101"
        port = input("What server port would you like to connect to?\n")
        try: port = int(port)
        except:
            print("Invalid port ID: Defaulting to 3021")
            port = 3021
        assert port == 3021

        print("Which post would you like to send to the server?\n")
        print("0: None")
        [print(f"{i+1}: {user._posts[i]['entry']}") for i in range(len(user._posts))]
        try: postid = int(input())
        except: raise TypeError
        messages = [j for j in user._posts]
        if postid == 0: messages = [None, None]
        send_bio = input("Would you like to post your bio? (y/n)\n")

        if input("Are you using any API's? (y/n)\n") == "y":
            webapi = []
            if input("Are you using the OpenWeather API? (y/n)\n") == "y":
                try: zip = int(input("What zip code would you like the weather of? "))
                except: print("Invalid option")
                ccode = input("What country code would you like to use? (no spaces)")
                webapi.append(OpenWeather())
                apikey = input("Please enter your apikey for OpenWeather: ")
                webapi[-1].set_apikey(apikey)
                webapi[-1].load_data()
            if input("Are you using the LastFM API? (y/n)\n") == "y":
                ccode = input("What country's top artist would you like to know? (no spaces) ")
                webapi.append(LastFM())
                apikey = input("Please enter your apikey for LastFM: ")
                webapi[-1].set_apikey(apikey)
                webapi[-1].load_data()
            for i in webapi:
                messages[postid-1]['entry'] = i.transclude(messages[postid-1]['entry'])
        
        if send_bio == "y":
            if dsc.send(user.dsuserver, port, user.username, user.password, messages[postid-1], user.bio): print("Successfully sent to server")
            else: print("Something went wrong")
        elif send_bio == "n" and messages[0] != None:
            if dsc.send(user.dsuserver, port, user.username, user.password, messages[postid-1]): print("Successfully sent to server")
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
        for i in range(len(choices_input)): choices_output.append(choices_input[i])

        if "1" in choices_output: print(f"Username:\n{user.username}")
        if "2" in choices_output: print(f"Password:\n{user.password}")
        if "3" in choices_output: print(f"Bio:\n{user.bio}")
        if "4" in choices_output:
            print("Posts:")
            [print(f"{i+1}: {user._posts[i]['entry']}") for i in range(len(user._posts))]
        if "5" in choices_output:
            print("Which post would you like to print?\n")
            [print(f"{i+1}: {user._posts[i]['entry']}") for i in range(len(user._posts))]
            try: post = int(input())
            except: raise TypeError
            print(user._posts[post-1]['entry'])
        if "6" in choices_output:
            print(f"Username: {user.username}")
            print(f"Password: {user.password}")
            print(f"Bio: {user.bio}")
            print("Posts:")
            [print(f"{i+1}: {user._posts[i]['entry']}") for i in range(len(user._posts))]

    else:
        if "-usr" in options.keys(): print(f"Username: {user.username}")
        if "-pwd" in options.keys(): print(f"Password: {user.password}")
        if "-bio" in options.keys(): print(f"Bio: {user.bio}")
        if "-posts" in options.keys():
            print("Posts:")
            [print(f"{i+1}: {user._posts[i]['entry']}") for i in range(len(user._posts))]
        if "-post" in options.keys(): print(user._posts[options["-post"]]['entry'])
        if "-all" in options.keys():
            print(user.username)
            print(user.password)
            print(user.bio)
            [print(f"{j+1}: {user._posts[j]['entry']}") for j in range(len(user._posts))]

def admin_input(user_input: list):
    """
    Interprets the admin mode input commands
    """
    command = user_input[0]
    try: command = str(command)
    except: raise TypeError
    user_input.pop(0)

    options = []
    for i in user_input:
        if i.startswith('-'): options.append(i)
    
    targets = []
    if len(options) > 0:
        for i in range(len(user_input)):
            if user_input[i-1].startswith('-') and not user_input[i].startswith('-'):
                targets.append(user_input[i])
            elif user_input[i-1].startswith('-') and user_input[i].startswith('-'):
                targets.append("")
    
    optionstargets = {}
    assert len(options) == len(targets)
    for i in range(len(options)):
        optionstargets[options[i]] = targets[i]
    
    for i in range(len(user_input)):
        if user_input[i].startswith("-"):
            user_input = user_input[:i]
            break
    
    if user_input == []:
        path = "."
        name = "admin.dsu"

        location = Path(os.path.join(path, name))
    else:
        location = ""
        for i in user_input:
            location += i + " "
        location = Path(location[:-1])

    return command, location, optionstargets

def list_folder_contents(location: Path, options: dict):
    """
    Lists folder contents given and specific options the user wants
    """
    if "-r" in options.keys(): recursive = True
    else: recursive = False

    if len(options.keys()) == 0:
        for i in location.iterdir():
            if i.is_file():
                print(location / i)
        for i in location.iterdir():
            if i.is_dir():
                print(location / i)
                if recursive:
                    list_folder_contents(location / i, recursive, options)
    if "-f" in options.keys():
        for i in location.iterdir():
            if i.is_file():
                print(location / i)
            elif recursive and i.is_dir():
                list_folder_contents(location / i, recursive, options)
    if "-s" in options.keys():
        for i in location.iterdir():
            if Path(i).name == f"{options['-s']}":
                print(location / i)
                if recursive and i.is_dir():
                    list_folder_contents(location / i, recursive, options)
    if "-e" in options.keys():
        for i in location.iterdir():
            if Path(i).suffix == f".{options['-e']}":
                print(location / i)
                if recursive and i.is_dir():
                    list_folder_contents(location / i, recursive, options)

def create_file(location: Path, options: dict):
    """
    Creates a .dsu file, used exclusively in admin mode.
    """
    if "-n" in options.keys():
        p = location.joinpath(f"{options['-n']}.dsu")
        if p.exists():
            print("ERROR: File already exists, opening instead")
            open_file(p)
            return
        else:
            p.touch()
        print(p, "successfully created")

        user = Profile.Profile()
        user.dsuserver = input()
        user.username = input()
        user.password = input()
        user.bio = input()

        user.save_profile(str(p))
    else:
        print("ERROR: Invalid option")

def delete_file(location: Path):
    """
    Deletes a .dsu file
    """
    assert os.path.exists(location) and location.suffix == ".dsu"
    os.remove(location)
    print(f"{location} DELETED\n")

def read_file(location: Path):
    """
    Reads a .dsu file and prints its contents
    """
    assert os.path.exists(location) and location.suffix == ".dsu"
    with open(location) as f:
        contents = f.readlines()
        if len(contents) > 0:
            for i in contents:
                print(i)
        else:
            print("EMPTY")

def open_file(location: Path):
    """
    Opens a .dsu file for editing
    """
    assert os.path.exists(location) and location.suffix == ".dsu"
    with open(location, "a") as f:
        print(location, "loaded successfully, enter ':Q' to exit")
        running = True
        while running:
            words = input()
            if words == ":Q": running = False
            f.write(f"{words}\n")