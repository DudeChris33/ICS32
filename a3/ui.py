# ui.py

# Chris Cyr, Justin Lee
# cyrc@uci.edu, justisl9@uci,edu
# 12436037, 39257953


from pathlib import Path
import os, Profile
import ds_client as dsc


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
        assert os.path.exists(path)
        assert filetypecheck(path)
        user = Profile.Profile()
        user.load_profile(path)
        print("Profile open.\n")
        return user, True, path


    elif user_input == "admin":
        print("Welcome to admin mode")
        dsuserver = "168.235.86.101"
        username = "admin"
        password = "adminpassword"
        bio = ""
        path = "."
        name = "admin.dsu"

        user = Profile.Profile(dsuserver, username, password)
        user.bio = bio

        file = Path(path) / name
        #file = os.path.join(path, f"{name}.dsu")
        if os.path.exists(file):
            user = Profile.Profile()
            user.load_profile(file)
            return user, True, file

        else:
            Path(file).touch()
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
    print(" 7. Print profile contents\n")
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
    assert filetypecheck(path)
    assert user.username
    if user.username != "admin":
        print("Enter profile information\n")
        path = Path(input("Please enter the path to your profile\n"))
        assert os.path.exists(path)
        assert filetypecheck(path)
        print("Profile open.\n")
        return user, path
    
    else:
        assert os.path.exists(path)
        assert filetypecheck(path)
        user = Profile.Profile()
        user.load_profile(path)
        print("Profile open.\n")
        return user, path


def edit_profile(user: Profile.Profile, options: dict, path: Path):
    """
    Lets a user painstakingly edit their profile prompt by prompt
    """
    assert filetypecheck(path)
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
            print(user.username)
        if "2" in choices_output:
            print(user.password)
        if "3" in choices_output:
            print(user.bio)
        if "4" in choices_output:
            [print(i) for i in user._posts]
        if "5" in choices_output:
            print("Which post would you like to print?\n")
            [print(f"{i+1}: {user._posts[i]['entry']}") for i in range(len(user._posts))]
            post = input()
            try: int(post)
            except: raise ValueError
            print(user._posts[int(post)-1]["entry"])
        if "6" in choices_output:
            print(user.username)
            print(user.password)
            print(user.bio)
            [print(f"{j+1}: {user._posts[j]['entry']}") for j in range(len(user._posts))]

    else:
        if "-usr" in options.keys(): print(user.username)
        if "-pwd" in options.keys(): print(user.password)
        if "-bio" in options.keys(): print(user.bio)
        if "-posts" in options.keys(): [print(f"{i+1}: {user._posts[i]['entry']}") for i in range(len(user._posts))]
        if "-post" in options.keys(): print(options["-post"])
        if "-all" in options.keys():
            print(user.username)
            print(user.password)
            print(user.bio)
            [print(f"{j+1}: {user._posts[j]['entry']}") for j in range(len(user._posts))]


def filetypecheck(location: Path) -> bool:
    """
    Checks that a file has the .dsu suffix and returns a bool
    """
    if location.suffix == ".dsu": return True
    else:
        print("ERROR: Invalid filetype")
        return False


def admin_input(user_input: list):
    """
    Interprets the admin mode input commands
    """
    command = user_input[0]
    user_input.pop(0)
    
    recursive = False
    for i in user_input:
        if i == "-r":
            recursive = True
            user_input.remove("-r")

    options = []
    for i in user_input:
        if i.startswith('-'): options.append(i)
    
    targets = []
    if len(options) > 0:
        for i in range(len(options) - 1):
                temp_target = user_input[user_input.index(options[i]) + 1:user_input.index(options[i+1])]
                target = ""
                for j in temp_target:
                    target += j + " "
                targets.append(target[:-1])
        temp_target = user_input[user_input.index(options[-1]) + 1:]
        target = ""
        for i in temp_target:
            target += i + " "
        targets.append(target[:-1])
    
    optionstargets = {}
    assert len(options) == len(targets)
    for i in range(len(options)):
        optionstargets[options[i]] = targets[i]
    
    location = ""
    for i in user_input:
        location += i + " "
    location = Path(location[:-1])

    return command, location, recursive, optionstargets


def list_folder_contents(location: Path, recursive: bool, options: dict):
    """
    Lists folder contents given and specific options the user wants
    """
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
    assert filetypecheck(location)
    os.remove(location)
    print(f"{location} DELETED\n")


def read_file(location: Path):
    """
    Reads a .dsu file and prints its contents
    """
    assert filetypecheck(location)
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
    assert filetypecheck(location)
    with open(location, "a") as f:
        print(location, "loaded successfully, enter ':Q' to exit")
        running = True
        while running:
            words = input()
            if words == ":Q": running = False
            f.write(f"{words}\n")