#lab16.py

# Starter code for lab 16 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# Chris Cyr
# cyrc@uci.edu
# 12436037

"""
This program enables a user to input short one line notes and have them stored in a file called pynote.txt

"""
import webbrowser
from pathlib import Path
from note import Note
from bookmarker import Bookmarker

BOOKMARK_PATH = "."
BOOKMARK_FILE = "pybookmark.txt"

# input/output messages. Keeping them together for easy translation and editing!
INPUT_MAIN_MENU = "What would you like to do? \n 1. Add a bookmark\n 2. Open a bookmark\n 3. View all bookmarks\n 4. Find a bookmark\n 5. Remove a bookmark\n 6. Quit\n"
INPUT_ADD = "Great. What bookmark would you like to add?\n"
INPUT_OPEN = "What bookmark would you like to open (enter item number)?\n"
INPUT_REMOVE = "What bookmark would you like to remove (enter item number)?\n"
INPUT_FIND = "Great. Enter a few words associated with the bookmark you want to find:\n"
MSG_OPEN_MENU = "Here is a list of your current bookmarks:\n"
MSG_EMPTY = "You currently do not have any bookmarks saved.\n"


class BookmarkException(Exception):
    def __init__(self, err_msg: str, ex: Exception):
        print(err_msg)
        raise ex


def print_bookmarks(bookmarks:list):
    print(MSG_OPEN_MENU)
    id = 0
    for b in bookmarks:
        print(f"{id}: {b}")
        id+=1

# abstract exception handling to a single location, keeps menu conditional table clean
def call(func, param):
    try:
        return func(param)
    except Exception as ex:
        raise BookmarkException(ex)

def run(bookmarker: Bookmarker):
    if len(bookmarker.all_notes) < 1:
        print(MSG_EMPTY)

    resp = input(INPUT_MAIN_MENU)
    while resp != '6':
        if resp == '1':
           call(bookmarker.add, input(INPUT_ADD))
        elif resp == '2':
            print_bookmarks(bookmarker.all_notes) 
            call(bookmarker.open, input(INPUT_OPEN))
        elif resp == '3':
            print_bookmarks(bookmarker.all_notes) 
        elif resp == '4':
            results = call(bookmarker.find, input(INPUT_FIND))
            print_bookmarks(results)
        elif resp == '5':
            print_bookmarks(bookmarker.all_notes) 
            call(bookmarker.remove_by_id, input(INPUT_REMOVE))
        
        resp = input(INPUT_MAIN_MENU)

if __name__ == "__main__":
    print("Welcome to PyBookmarker! \n")

    # the file used to store bookmarks
    p = Path(BOOKMARK_PATH) / BOOKMARK_FILE

    # if file does not exist, create it.
    if not p.exists():
        p.touch()

    # instantiate the bookmark class and pass to run 
    bm = Bookmarker(p)
    try:
        run(bm)
    except: 
        print("Uh oh. The programming team for pybookmark has clearly missed handling a critical error. Please direct all complaints to the TAs! :)")
