#lab3.py

# Starter code for lab 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# Chris Cyr
# cyrc@uci.edu
# 12436037


from pathlib import Path


def initialize():
    p = Path()
    p = p.joinpath("pynotes.txt")
    
    f = p.open("a")
    f.close()
    
    return p


def readnotes(filename):
    print("Welcome to PyNote!")
    print("Here are your notes:\n")
    f = open(filename)
    contents = f.readlines()
    for i in contents:
        print(i)
    f.close()
    return


def main():
    filename = initialize()
    readnotes(filename)
    f = filename.open("a")
    while True:
        user_input = input('Please enter a new note (enter q to exit):\n')
        if user_input == 'q':
            f.close()
            quit()
        else:
            f.write(user_input + "\n")


if __name__ == "__main__":
    main()
