import classes
from classes import *
import items
from items import *
import pickle
from pickle import *
import sys
import time

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def delay_print(s):
    for c in s:
        sys.stdout.write( '%s' % c )
        sys.stdout.flush()
        time.sleep(0.1)

def cock(player):
    chickens_out = 1
    while not chickens_out in player.feats and (action_counter % 4) == 0:
            print("\tYou hear a muffled rooster's crow from somewhere outside.")
            break

def play():
    print("\n")
    #delay_print("""
    #In a serene forest in a small town there sits a large, white brick house.  The house is settled comfortably on well-kept land with towering pine trees pressing in on all sides.  A large forest opposes the back of the house.  There are two buildings outside. Welcome to...
    #""")
    print("""
       _            _       _    _               _              _                  _   _         _      
      /\ \         / /\    / /\ /\ \            /\ \           / /\               /\_\/\_\ _    /\ \    
      \_\ \       / / /   / / //  \ \          /  \ \         / /  \             / / / / //\_\ /  \ \   
      /\__ \     / /_/   / / // /\ \ \        / /\ \_\       / / /\ \           /\ \/ \ \/ / // /\ \ \  
     / /_ \ \   / /\ \__/ / // / /\ \_\      / / /\/_/      / / /\ \ \         /  \____\__/ // / /\ \_\ 
    / / /\ \ \ / /\ \___\/ // /_/_ \/_/     / / / ______   / / /  \ \ \       / /\/________// /_/_ \/_/ 
   / / /  \/_// / /\/___/ // /____/\       / / / /\_____\ / / /___/ /\ \     / / /\/_// / // /____/\    
  / / /      / / /   / / // /\____\/      / / /  \/____ // / /_____/ /\ \   / / /    / / // /\____\/    
 / / /      / / /   / / // / /______     / / /_____/ / // /_________/\ \ \ / / /    / / // / /______    
/_/ /      / / /   / / // / /_______\   / / /______\/ // / /_       __\ \_\ /_/    / / // / /_______\   
\_\/       \/_/    \/_/ \/__________/   \/___________/ \_\___\     /____/_/        \/_/ \/__________/   
                                                                                                        
    """)
    raw_input("Press Enter to continue.")

    player = Player()
    save_object(player, 'player.pkl')
    global action_counter
    action_counter = 1
    while player.is_alive() and not player.victory:
        cock(player)
        with open('player.pkl', 'rb') as input:
            player = pickle.load(input)
        print((player.tile)().intro_text())
        do_action(player)
        action_counter += 1
    if player.victory:
        print("You win!")
    elif not player.is_alive():
        print("You have died an early death.")

def get_fixtures(player):
    global in_room 
    in_room = []
    for item in (player.tile)().fixtures:
        in_room.append(item.hotkey)

def get_inventory(player):
    global in_inv
    in_inv = []
    for item in player.inventory:
        in_inv.append(item.hotkey)

def get_actions(player):
    global avail_act
    avail_act = []
    for fix in (player.tile)().fixtures:
        if fix.use:
            avail_act.append('use')
        if fix.use:
            avail_act.append('go')
        if fix.take:
            avail_act.append('take')
        if fix.search:
            avail_act.append('search')
        if fix.desc or (player.tile).desc:
            avail_act.append('look')
        else:
            pass

def choose_action():
    action = None
    while not action:
        print("What would you like to do?")
        action_input = '{}'.format(raw_input("&:"))
        action_input = action_input.lower()
        #this cannot handle non-lowercase yet#
        action_split = action_input.split(" ")
        return(action_split)

def do_action(player):
    try:
        get_fixtures(player)
        get_inventory(player)
        get_actions(player)
        global act_dict
        global act_noun
        global act_verb
        act_verb = []
        act_noun = []
        act_dict = choose_action()

        if len(act_dict) > 1:
            for word in act_dict:
                if word in zip(in_room, in_inv):
                    act_noun = word
                    #remove item?#
                #if word in in_inv:
                    #act_noun = word
                if word in avail_act:
                    act_verb = word
                if word == 'room':
                    act_noun = 'player.tile'
                else:
                    pass  
            act_noun = eval(act_noun)
            act_verb = eval(act_verb)
            print("\n")
            act_verb(act_noun())

        if len(act_dict) == 1:
            print("\n")
            for word in act_dict:
                if word == 'help':
                    help()
                if word in avail_act:
                    act_verb = word
                if word == 'look':
                    for item in (player.tile)().fixtures:
                        print "You see: " + item.name
                    for item in (player.inventory):
                        print "You have: " + item.name
                #if word == 'inventory' or 'items':
                    #print(player.inventory)
                else:
                    pass
    except TypeError:
            print("""
            What?""")
            #add exception#

            #thing not in the room or otherwise not callable#
            #what if they type in two items?#

play()

