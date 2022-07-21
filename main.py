#! /usr/local/bin/python3

import json
import sys
from random import seed
from random import choice
from datetime import datetime

from dungeon import Dungeon
from player import Player

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# nu börjar vi
seed(datetime.now())
metafil = 'config.json' # lite meta info vi sparar i dung
dmf = open(metafil)
dung = json.load(dmf)
# vi skriver ut dung['intro'] när spelet börjar
# och vi skriver ut dung['outro'] när vi kommer till ett
# rum utan någon exit. Då har vi klarat spelet.
d = Dungeon(dung['roomfile'],dung['itemfile'], dung['eventfile'],dung['startRoom'])
p = Player(d.startRoom)
p.items = d.getPlayerItems()
d.enterRoom(p.roomId)

print(bcolors.BOLD + bcolors.HEADER + dung['intro'] + bcolors.ENDC + "\n\n")
# lets print the first room!
d.printRoom()

# vi initierar lite räknare och metadata saker

dung_current_room = d.startRoom

# lite ord vi vill hålla koll på
# ta emot våra commandon
while True:
    d.playerItems = p.items
    data = input(bcolors.OKGREEN + choice(dung['askForInput']) + bcolors.ENDC)
    if len(data) < 1:
        data = "nonsense" # so we always act on something. even just return.
    comm = data.split()
    # först kollar vi lite svordomar..
    try:
        if len(dung['swearwords']) > 0:
            found_swear = 0
            for w in comm:
                if w in dung['swearwords']:
                    print(choice(dung['swear_responses']))
                    found_swear = 1
            if found_swear == 1:
                comm[0] = 'h'
    except NameError:
        pass
        #print("ingasvordomar laddade")

    # only count commands we understand and care about. Not help, or iventory
    # will check this at the end. of loop
    something_happened = False

    # check for triggers and run events
    #d.checkTriggers()

    # help command
    if comm[0] in dung['commands']['help']['alias']:
        print(choice(dung['commands']['help']['responses']))
        print(dung['commands']['help']['response'])

    # inventory command
    elif comm[0] in dung['commands']['inventory']['alias']:
        print(choice(dung['commands']['inventory']['response']))
        print(p.listItems())

    # drop command
    elif comm[0] in dung['commands']['drop']['alias']:
        if len(comm) == 1: # only a single drop command but not what to drop
            print(choice(dung['commands']['drop']['emptyResponse']))
        else: # at least 1 thing has been named to be dropped.
            if len(p.items) > 0: # Ites the player has exists.
                comm.pop(0)
                throwthing = " ".join(comm)
                i = p.getItemByName(throwthing)
                if len(i) > 0:
                    d.count += 1
                    print(choice(dung['commands']['drop']['response']) + i['name'])
                    d.addItem(p.roomId,i)
                    p.removeItem(i['id'])
                    something_happened = True
                else:
                    print(dung['commands']['drop']['errorResponse'] + throwthing)
            else: # player has nothing to throw
                print(dung['commands']['drop']['nothingToThrow'])
    # take command
    elif comm[0] in dung['commands']['take']['alias']:
        if len(comm) < 2:
            print(choice(dung['commands']['take']['emptyResponse']))
        else:
            comm.pop(0)
            takething = " ".join(comm)
            item = d.getRoomItemByName(p.roomId, takething)
            if len(item) > 0:
                d.count += 1
                # ta bort från dungeon
                d.removeItem(item['id'])
                p.items.append(item)
                print(item['takeMessage'])
                something_happened = True
            else:
                print(choice(dung['commands']['take']['errorResponse']) + takething + ".")
    # look command
    elif comm[0] in dung['commands']['look']['alias']:
        if len(comm) < 2:
            d.count += 1
            d.printRoom()
            something_happened = True
        else:
            comm.pop(0)
            lookthing = " ".join(comm)
            ritems = d.getRoomItems(p.roomId)
            if len(ritems) > 0:
                for item in ritems:
                    if lookthing == item['name']:
                        d.count += 1
                        print(item['Description'])
                        something_happened = True
            for item in p.items:
                if lookthing == item['name']:
                    d.count += 1
                    print(item['Description'])
                    something_happened = True
    # go command
    elif comm[0] in dung['commands']['go']['alias']:
        if len(comm) < 2:
            print(choice(dung['commands']['go']['emptyResponse']))
        else:
            comm.pop(0)
            place = " ".join(comm)
            if place in d.rooms[p.roomId]['exits']:
                d.count += 1
                p.roomId = d.rooms[p.roomId]['exits'][place]
                d.enterRoom(p.roomId)
                d.printRoom()
                something_happened = True
            else:
                print(choice(dung['commands']['go']['errorResponse']))

    elif comm[0] == dung['endCommand']:
        break
    else: # som sista utväg kolla exits
        if comm[0] in d.rooms[p.roomId]['exits']:
            d.count += 1
            p.roomId = d.rooms[p.roomId]['exits'][comm[0]]
            d.enterRoom(p.roomId)
            d.printRoom()
            something_happened = True
        else:
            print(choice(dung['dontUnderstand']))

#    dung_turncount += 1
#    if something_happened:




print(dung['gamestop'])
