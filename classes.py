import enemies
import npc
import random
import items

class Player():
    def __init__(self):
        self.inventory = [items.guns()]
        self.tile = None
        self.x = 0
        self.y = 0
        self.hp = 100
        self.gold = 25
        self.desc = ""
        self.victory = False

    def description(self):
        print(str(self.desc))
 
    def is_alive(self):
        return self.hp > 0
 
    def print_inventory(self):
        print("Inventory:")
        for item in self.inventory:
            print('*' + str(item))
        print("Gold: {}".format(self.gold))

    def heal(self):
        consumables = [item for item in self.inventory
                       if isinstance(item, items.Consumable)]
        if not consumables:
            print("You don't have anything to heal yourself with.")
            return
        for i, item in enumerate(consumables, 1):
            print("Choose an item to use to heal:")
            print("{}. {}.".format(i, item))

        valid = False
        while not valid:
            choice = input("")
            try:
                to_eat = consumables[int(choice) -1]
                self.hp = min(100, self.hp + to_eat.healing_value)
                self.inventory.remove(to_eat)
                print("Current HP:{}".format(self.hp))
                valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again.")

    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None
        for item in self.inventory:
            try:
                if item.damage> max_damage:
                    best_weapon = item.damage
            except AttributeError:
                pass
        return best_weapon

    def attack(self):
        best_weapon = self.most_powerful_weapon()
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        print("You use{} against {}".format(bestweapon.name, enemy.name))
        #add some flavor text#
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print("You killed {}.".format(enemy.name))
        else:
            print("{} has {} HP remaining.".format(enemy.name, enemy.hp))

    def trade(self):
        #room = world.tile_at(self.x, self.y)
        room.check_if_trade(self)

player = Player()
############################################################

class MapTile:
    def intro_text(self):
        raise NotImplementedError("Create a subclass instead!")
    def modify_player(self, player):
        pass

class StartTile(MapTile):
    def __init__ (self):
        self.fixtures = [door(), desk()]
        self.desc = "This will be a fun little description."
    def intro_text(self):
        return """
        You are sitting on your bed after having just woken up.
        """
        #first and second instances#

class room_two(MapTile):
    def __init__(self):
        self.first_visit = False
        self.fixtures = []
    def intro_text(self):
        return """ 
        Outside your room there is a bathroom to your left, a doorway in front of you, and a long hallway to your right.
        """

class FindItemTile(MapTile):
    pass

############################################################

def use(thing):
    if thing.modify_player:
        thing.modify_player()
    else:
        return "That doesn't seem to work."

def look(arg):
    if arg.desc:
        print(arg.desc)
    else:
        try:
            pass
            #items????
        except NameError, TypeError:
            print "Can't look at that."

def search(thing):
    if thing.modify_player:
        thing.modify_player()
    else:
        return "That doesn't seem to work."


############################################################

class Fixture:
    def __init__(self, name, hotkey, take, use, desc, search):
        self.name = name
        self.hotkey = hotkey
        self.take = take
        self.use = use
        self.desc = desc
        self.search = search

class door(Fixture):
    def __init__(self):
        self.name = "a door"
        self.hotkey = "door"
        self.take = False
        self.use = True
        self.desc = "Looks like the door is unlocked."
        self.search = False
    def modify_player(self):
        player.tile = room_two()
        print("You exit the room")

class desk(Fixture):
    def __init__(self):
        self.name = "a desk"
        self.hotkey = "desk"
        self.take = False
        self.use = False
        self.desc = 'A well made desk sits in the corner.'
        self.search = True
    def modify_player(self):
        player.inventory = player.inventory.append(items.pen())
        return"""
        You pick up a pen off the desk.
        """

