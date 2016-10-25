import enemies
import npc
import random
import items
from items import *
import pickle
from pickle import *

#def delay_print(s):
    #for c in s:
        #sys.stdout.write( '%s' % c )
        #sys.stdout.flush()
        #time.sleep(0.25)

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

class Player():
    def __init__(self):
        self.inventory = [items.watch()]
        self.tile = StartTile
        self.x = 0
        self.y = 0
        self.hp = 100
        self.gold = 25
        self.desc = ""
        self.victory = False
        self.feats = []

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


############################################################

class StartTile():
    kind = 'maptile'
    def __init__ (self):
        self.fixtures = [door(), desk()]
        self.desc = "The room is simple with few furnishings."
        self.locked = False
    def intro_text(self):
            return """
            You are sitting on your bed after having just woken up.
            """
            #return """
            #You're standing in your room.  Why did you come in here, again?
            #"""
        #first and second instances#

class RoomTwo():
    kind = 'maptile'
    def __init__(self):
        self.first_visit = False
        self.fixtures = [door(),hallway()]
        self.desc = "You bounce on the balls of your toes anticipating action."
        self.locked = False
    def intro_text(self):
        return """ 
        Outside your room there is a bathroom to your left, a doorway in front 
        of you, and a long hallway to your right.
        """

class Hallway():
    kind = 'maptile'
    def __init__(self):
        self.first_visit = False
        self.fixtures = [hallway(), staircase(), windows(), door()]
        self.desc = "You are at the far end of a long hallway."
        self.locked = False
    def intro_text(self):
        return """ 
        At the end of the hallway there is a small room.  The hallway overlooks a foyer that has many windows.  A staircase leads downwards.
        """

class StorageRoom():
    kind = 'maptile'
    def __init__(self):
        self.first_visit = False
        self.fixtures = [door()]
        self.desc = "A narrow room filled with odds and ends."
        self.locked = True
    def intro_text(self):
        return """ 
        You are in a small storage room.
        """

class Foyer():
    kind = 'maptile'
    def __init__(self):
        self.first_visit = False
        self.fixtures = [staircase(), windows()]
        self.desc = "The room is simple with few furnishings."
        self.locked = False
    def intro_text(self):
        return """ 
        You are downstairs in an open foyer.  There are ornate, wooden doors that open to the outside.  There are three other rooms you can see from where you are standing and another hallway.
        """

class Foyer():
    kind = 'maptile'
    def __init__(self):
        self.first_visit = False
        self.fixtures = [hallway(), staircase(), windows()]
        self.desc = "The foyer is open to the second story.  You can see into several rooms from where you are standing."
        self.locked = True
    def intro_text(self):
        return """ 
        At the end of the hallway there is a small room.  The hallway overlooks a foyer that has many windows.  A staircase leads downwards.
        """

############################################################

############################################################

def help():
    print """
    To interact with the environment, you may do certain actions such as 'look', 'use', 'go', 'search'.
    For example, 'look room' will give a description of the room and things in it.
    """

def use(thing):
    player = Player()
    if thing.modify_player:
        thing.modify_player(player)
    else:
        return "That doesn't seem to work."

def go(thing):
    player = Player()
    if thing.modify_player:
        thing.modify_player(player)
    else:
        return "That doesn't seem to work."

def look(thing):
    player = Player()
    if thing.desc:
        print(thing.desc)
    else:
        try:
            if arg in player.inventory:
                print(arg.desc)
            else:
                print((player.tile).desc)
        except NameError:
            print ("Can't look at that.")

def search(thing):
    player = Player()
    if thing.modify_player:
        thing.modify_player(player)
    else:
        return "That doesn't seem to work."

############################################################

class Fixture:
    def __init__(self, hotkey, take, use, desc, search):
        self.hotkey = hotkey
        self.take = take
        self.use = use
        self.desc = desc
        self.search = search

class door(Fixture):
    def __init__(self):
        self.name = 'a door'
        self.hotkey = "door"
        self.take = False
        self.use = True
        self.desc = "Looks like the door is unlocked."
        self.search = False
        self.lookup = {StartTile:'StartTile', RoomTwo:'RoomTwo', Hallway:'Hallway', StorageRoom:'StorageRoom'}
        self.directions = {'StartTile':RoomTwo, 'RoomTwo':StartTile, 'Hallway':StorageRoom, 'StorageRoom':Hallway}
    def modify_player(self, player):
        with open('player.pkl', 'rb') as input:
            player = pickle.load(input)
        tile = player.tile
        lookup_tile = door().lookup[tile]
        if (tile)().locked == False:
            player.tile = door().directions[lookup_tile]
            print("You move.")
        else:
            print("The door is locked.")
        save_object(player, 'player.pkl')

class hallway(Fixture):
    def __init__(self):
        self.name = "a hallway"
        self.hotkey = "hallway"
        self.take = False
        self.use = True
        self.desc = "A long hallway that overlooks a foyer."
        self.search = False
    def modify_player(self, player):
        with open('player.pkl', 'rb') as input:
            player = pickle.load(input)
        if player.tile is RoomTwo:
            player.tile = Hallway
            print("""
                You walk down the hallway.
                """)
        elif player.tile is Hallway:
            player.tile = RoomTwo
            print("You walk down the hallway.")
        save_object(player, 'player.pkl')

class desk(Fixture):
    def __init__(self):
        self.name = "a desk"
        self.hotkey = "desk"
        self.take = False
        self.use = False
        self.desc = 'A well made desk sits in the corner.  There is a pen sitting on the desk.'
        self.search = True
        self.inventory = [pen()]
    def modify_player(self, player):
        with open('player.pkl', 'rb') as input:
            player = pickle.load(input)
        (player.inventory).append(items.pen())
        save_object(player, 'player.pkl')
        print("""
        You pick up a pen off the desk.
        """)

class staircase(Fixture):
    def __init__(self):
        self.name = "a staircase"
        self.hotkey = "door"
        self.take = False
        self.use = True
        self.desc = "A wide staircase with wrought iron bannisters leads downwards."
        self.search = False
    def modify_player(self, player):
        with open('player.pkl', 'rb') as input:
            player = pickle.load(input)
        if player.tile is Hallway:
            player.tile = Foyer
            print("You exit the room.")
        elif player.tile is Foyer:
            player.tile = Hallway
            print("You enter your room.")
        save_object(player, 'player.pkl')

class windows(Fixture):
    def __init__(self):
        self.name = "some windows."
        self.hotkey = "windows"
        self.take = False
        self.use = False
        self.desc = 'The windows look out over a well-kept lawn.  Beyond that you can see a stand of trees that obscures an asphalt road..'
        self.search = False


