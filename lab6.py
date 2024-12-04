"""
This program enables a user to input short one line notes and have them stored in a file called pynote.txt

"""

import lab6module as addon
from pathlib import Path

NOTES_PATH = "."
NOTES_FILE = "pynote.txt"

def is_int(val):
    if type(val) == int:
        return True
    else:
        return False

def save_note(note: str):
    # create path obj to notes storage file
    p = addon.buildpath(NOTES_PATH, NOTES_FILE)
    
    # open and write user note to file
    with p.open('a') as f:
        f.write(note + '\n')


def read_notes():
    p = addon.buildpath(NOTES_PATH, NOTES_FILE)

    # check if storage file exists, if not return.
    if not p.exists():
        return
    
    print("Here are your notes: \n")
    # open and write user note to file
    with p.open() as f:
        for line in f:
            print(line)
    

def remove_note() -> str:
    p = addon.buildpath(NOTES_PATH, NOTES_FILE)

    # check if storage file exists, if not return.
    if not p.exists():
        raise FileNotFoundError("Notes file has been deleted unexpectedly")
    
    print("Here are your notes: \n")
    # open and write user note to file
    with p.open() as f:
        lines = f.readlines()

        # print each note with an id and store each line in a list
        for id in range(len(lines)):
            print(f"{id+1}: {lines[id]}")

    remove_id = input("Enter the number of the note you would like to remove: ")
    if not is_int(remove_id) or int(remove_id) > len(lines):
        print ("Not a valid number, cancelling operation.")
        return ""

    # open as write to overwrite existing notes, add notes back while skipping user selection 
    with p.open('w') as f:
        removed_note = ""

        for id in range(len(lines)):
            if id == int(remove_id)-1:
                removed_note = lines[id]
            else:
                f.write(lines[id])

    return removed_note

def run():
    note = input("Please enter a note (enter :d to delete a note or :q to exit):  ")
    if note == ":d":
        try:
            note = remove_note()
            if note is None:
                assert False, "FileNotFoundError should have been raised"
            
            print(f"The following note has been removed: \n\n {note}")
        except FileNotFoundError:
            print("The PyNote.txt file no longer exists")
    elif note == ":q":
        return
    else:    
        save_note(note)
    run()


if __name__ == "__main__":
    assert is_int(5)
    assert not is_int(5.36)
    assert not is_int("five")

    print("Welcome to PyNote! \n")
    read_notes()

    run()
    
###################################################################################
#TODO: PASTE YOUR SECOND MODULE CODE BELOW BEFORE SUBMITTING!
###################################################################################
from pathlib import Path


def buildpath(path, file):
    return Path(path) / file
