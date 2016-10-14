from random import randrange

class Weapon:
    def __init__(self):
        raise NotImplementedError("Do not create raw Weapon objects.")

    def __str__(self):
        return self.name

class guns(Weapon):
    def __init__(self):
        self.name = "guns"
        self.desc = "Two single action pistols."
        self.damage = randrange(7,11,1)
        self.value = 25
        

class pen():
    def __init__(self):
        self.name = "pen"
        self.desc = "Mightier than the sword, potentially."
        

class Consumable:
    def __init__(self):
        raise NotImplementedError("Do not create raw Consumable objects.")

    def __str__(self):
        return "{} (+{} HP)".format(self.name, self.healing_value)

class Jerky(Consumable):
    def __init__(self):
        self.name = "Jerky"
        self.healing_value = 5
        self.value = 5

class Coffee(Consumable):
    def __init__(self):
        self.name = "Coffee"
        self.healing_value = 7
        self.value = 7
