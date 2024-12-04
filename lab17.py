# lab17.py

# Chris Cyr
# cyrc@uci.edu
# 12436037


from abc import ABC, abstractmethod
import random, enum, time


class Appetite:
    LOW = 3
    MEDIUM = 4
    HIGH = 5

class Dog(ABC):
    def __init__(self, name, age, appetite) -> None:
        self.hunger_clock = 0
        self._name = name
        self._age = age 
        self.appetite = appetite

    @abstractmethod
    def breed(self):
        pass
    
    def name(self):
        return self._name
    
    def age(self):
        return self._age

    def hungry(self, func: callable):
        """
        The hungry method will check the hungry clock to see if some time has
        passed since the last feeding. If clock is greater than breed typical
        appetite, hunger assessment is randomly selected, otherwise hunger clock increases
        """
        if self.hunger_clock > self.appetite:
            if bool(random.getrandbits(1)):
                print(f"Your {self.breed()}, {self.name()} is hungry.")
                feed = input(f"Would you like to feed {self.name()}? (y/n/q): ")
                if feed == 'y':
                    func(self)
                elif feed == "n":
                    return
                elif feed == 'q':
                    quit()
        else:
            self.hunger_clock += 1
            return

    def feed(self):
        """
        Feeds the dog. Hunger clock is reset
        """
        self.hunger_clock = 0

class GermanShepherd(Dog):
    def __init__(self, name, age):
        super().__init__(name, age, appetite=Appetite.MEDIUM)

    def breed(self):
        return "German Shepherd"

class GoldenRetriever(Dog):
    def __init__(self, name, age):
        super().__init__(name, age, appetite=Appetite.MEDIUM)

    def breed(self):
        return "Golden Retriever"

class AnatolianShepherd(Dog):
    def __init__(self, name, age):
        super().__init__(name, age, appetite=Appetite.MEDIUM)

    def breed(self):
        return "Anatolian Shepherd"
    
def feed_dog(dog: Dog):
    dog.hunger_clock = 0
    print(f"{dog._name} has been fed \U0001F415")

if __name__ == '__main__':
    dog = None
    breed = input("What breed of dog would you like to care for? \n\n 1. German Shepherd \n 2. Golden Retriever \n 3. Anatolian Shepherd \n: ")
    name = input("What would you like to name your dog? ")
    age = input("How old would you like your dog to be? ")
    age = int(age)
    if breed == "1":
        dog = GermanShepherd(name, age)
    elif breed == "2":
        dog = GoldenRetriever(name, age)
    elif breed == "3":
        dog = AnatolianShepherd(name, age)
    else:
        print("I didn't understand your entry, please run again.")

    while True:
        dog.hungry(feed_dog)
        time.sleep(3)
        