#lab14.py

# Starter code for lab 14 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# Chris Cyr
# cyrc@uci.edu
# 12436037

from abc import ABC, abstractmethod
import random, enum

class Appetite:
    LOW = "2"
    MEDIUM = "4"
    HIGH = "6"

class Dog:
    def __init__(self, breed, name, age, appetite: Appetite = Appetite.MEDIUM):
        self._breed = breed
        self._name = name
        self._age = age
        self.hunger_clock = 0
        self.appetite = int(appetite)

    def breed(self):
        return self._breed

    def name(self):
        return self._name
    
    def age(self):
        return self._age

    def hungry(self):
        """
        The hungry method will check the hungry clock to see if some time has
        passed since the last feeding. If clock is greater than breed typical
        appetite, hunger assessment is randomly selected, otherwise hunger clock increases
        """
        if self.hunger_clock > self.appetite:
            return bool(random.getrandbits(3))
        else:
            self.hunger_clock += 1
            return False

    def feed(self):
        """
        Feeds the dog. Hunger clock is reset
        """
        self.hunger_clock = 0

class Breeds(enum.Enum):
    GermanShepherd = Appetite.MEDIUM
    GoldenRetriever = Appetite.HIGH
    Husky = Appetite.LOW

if __name__ == '__main__':
    breed = input("What is your dog's breed? (Capitalize all words)\n")
    name = input("What is your dog's name?\n")
    try: age = int(input("What is your dog's age?\n"))
    except: raise TypeError
    breeds = {
        "German Shepherd": Breeds['GermanShepherd'].value,
        "Golden Retriever": Breeds['GoldenRetriever'].value,
        "Husky": Breeds['Husky'].value
    }
    if breed in breeds.keys(): doggy = Dog(breed, name, age, breeds[breed])
    else: doggy = Dog(breed, name, age)

    while True:
        h = ""
        if doggy.hungry() == False:
            h = "not "
        print(f"Your {doggy.breed()}, {doggy.name()} is {h}hungry.")
        feed = input(f"Would you like to feed {doggy.name()}? (y/n/q): ")

        if feed == "y":
            doggy.feed()
            print()
        elif feed == "q":
            break