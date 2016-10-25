from random import randrange
from time import strftime

class Weapon:
    def __init__(self):
        raise NotImplementedError("Do not create raw Weapon objects.")

    def __str__(self):
        return self.name

class watch(Weapon):
    def __init__(self):
        self.name = "a watch"
        self.hotkey = "watch"
        self.desc = "You look at your watch.  It's: " + strftime("%H:%M:%S") + "."
        self.damage = randrange(7,11,1)
        self.value = 25

class pen():
    def __init__(self):
        self.name = "a pen"
        self.hotkey = "pen"
        self.desc = "Mightier than the sword, potentially."

class Consumable:
    def __init__(self):
        raise NotImplementedError("Do not create raw Consumable objects.")

    def __str__(self):
        return "{} (+{} HP)".format(self.name, self.healing_value)

class jerky(Consumable):
    def __init__(self):
        self.name = "a piece of jerky"
        self.hotkey = "jerky"
        self.healing_value = 5
        self.value = 5

class coffee(Consumable):
    def __init__(self):
        self.name = "a cup of coffee"
        self.hotkey = "coffee"
        self.healing_value = 7
        self.value = 7