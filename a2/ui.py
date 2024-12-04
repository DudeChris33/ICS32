# ui.py

# Chris Cyr
# cyrc@uci.edu
# 12436037


from pathlib import Path
import os, Profile


def init():
    print("Welcome to ICS 32 Journal")
    print("Enter Q at any time to exit the program\n")
    
    print("How would you like to get started?\n")
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
    
    else:
        print("ERROR: Invalid option")
        return None, False, None


def menu():
    print("What would you like to do?\n")
    print(" 1. Create a new Profile")
    print(" 2. Open an existing Profile")
    print(" 3. Edit an existing Profile")
    print(" 4. Add an entry")
    print(" 5. Delete an entry")
    print(" 6. Post an entry online")
    print(" 7. Print profile contents\n")
    return input()


def create_profile():
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
    name = input("What name would you like to use for your profile?\n\n")
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
    if user.username != "admin":
        print("Enter new profile information\n")
        dsuserver = input("What DSU server would you like to use?\n")
        #assert len(dsuserver.split(".")) > 1
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

    print("Profile successfully edited.\n")
    return user, path


def write_post(user: Profile.Profile, path: Path):
    user.add_post(Profile.Post(input("What would you like to say?\n")))
    user.save_profile(path)


def remove_post(user: Profile.Profile, path: Path):
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


def print_profile(user: Profile.Profile, options: dict):
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
        if "-posts" in options.keys(): [print(i) for i in user._posts]
        if "-post" in options.keys(): print(options["-post"])
        if "-all" in options.keys():
            print(user.username)
            print(user.password)
            print(user.bio)
            [print(j) for j in user._posts]


def filetypecheck(location: Path):
    if location.suffix == ".dsu": return True
    else:
        print("ERROR: Invalid filetype")
        return False


def admin_input(user_input: list):
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
    os.remove(location)
    print(f"{location} DELETED\n")


def read_file(location: Path):
    with open(location) as f:
        contents = f.readlines()
        if len(contents) > 0:
            for i in contents:
                print(i)
        else:
            print("EMPTY")


def open_file(location: Path):
    with open(location, "a") as f:
        print(location, "loaded successfully, enter ':Q' to exit")
        running = True
        while running:
            words = input()
            if words == ":Q": running = False
            f.write(f"{words}\n")