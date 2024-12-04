#C C:\Users\Christopher Cyr\Documents\School\First Year\Winter\ICS 32 -n temp

from pathlib import Path
import os


def eval_input(user_input):
    command = user_input[0]
    user_input.pop(0)
    
    recursive = False
    for i in user_input:
        if i == '-r':
            recursive = True
            user_input.remove('-r')
    
    option = "none"
    for i in user_input:
        if i.startswith('-'):
            option = i
            break

    target = "none"
    if option != "none":
        target = ''
        for i in range(user_input.index(option) + 1, len(user_input)):
            target += user_input[i] + ' '
        target = target[:-1]
        user_input = user_input[:user_input.index(option)]
    
    location = ''
    for i in user_input:
        location += i + ' '
    location = location[:-1]
    location = Path(location)

    return command, location, recursive, option, target


def list_contents(location, recursive, option, target):
    if recursive:
        recursive_list(location, option, target)
    else:
        if option == "none":
            for i in location.iterdir():
                if i.is_file():
                    print(location / i)
            for i in location.iterdir():
                if i.is_dir():
                    print(location / i)
        elif option == "-f":
            for i in location.iterdir():
                if i.is_file():
                    print(location / i)
        elif option == "-s":
            for i in location.iterdir():
                if i.is_file() and Path(i).name == Path(target).name:
                    print(location / i)
        elif option == "-e":
            for i in location.iterdir():
                if i.is_file() and Path(i).suffix == f".{target}":
                    print(location / i)
        else:
            print("ERROR")


def recursive_list(location, option, target):
    if option == "none":
        for i in location.iterdir():
            if i.is_file():
                print(location / i)
        for i in location.iterdir():
            if i.is_dir():
                print(location / i)
                recursive_list(location / i, option, target)
    elif option == "-f":
        for i in location.iterdir():
            if i.is_file():
                print(location / i)
        for i in location.iterdir():
            if i.is_dir():
                recursive_list(location / i, option, target)
    elif option == "-s":
        for i in location.iterdir():
            if i.is_file() and Path(i).name == Path(target).name:
                print(location / i)
        for i in location.iterdir():
            if i.is_dir():
                recursive_list(location / i, option, target)
    elif option == "-e":
        for i in location.iterdir():
            if i.is_file() and Path(i).suffix == f".{target}":
                print(location / i)
        for i in location.iterdir():
            if i.is_dir():
                recursive_list(location / i, option, target)
    else:
        print("ERROR")


def creation(location, option, target):
    if option == "-n":
        p = Path(location)
        p = p.joinpath(f"{target}.dsu")

        f = p.open("w")
        f.close()
        print(p)


def deletion(location):
    if location.suffix == ".dsu":
        os.remove(location)
        print(location, "DELETED")
    else:
        print("ERROR")


def print_contents(location):
    if location.suffix == ".dsu":
        f = open(location, "r")
        contents = f.readlines()
        f.close()
        if len(contents) > 0:
            for i in contents:
                print(i)
        else:
            print("EMPTY")
    else:
        print("ERROR")


if __name__ == "__main__":
    while True:
        user_input = input().split()
        command, location, recursive, option, target = eval_input(user_input)

        if command == "Q":
            quit()
        elif os.path.exists(location):
            if command == "L":
                list_contents(location, recursive, option, target)
            elif command == "C":
                creation(location, option, target)
            elif command == "D":
                deletion(location)
            elif command == "R":
                print_contents(location)
        else:
            print("ERROR")
                        
        
        
        
        
