#! /usr/local/bin/python3

import json
import sys
from random import seed
from random import choice
from datetime import datetime

from dungeon import Dungeon

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

class Player:
    def __init__(player,roomId):
        player.roomId = roomId
        player.items = []
    def listItems(player):
        lista = []
        if len(player.items) > 0:
            for i in player.items:
                lista.append(i['name'])
        app = ", "
        return app.join(lista)
    def getItemByName(player,name):
        item = []
        for i in player.items:
            if name == i['name'] and not 'pid' in i:
                return i
        return item
    def removeItem(player,id):
        c = 0
        rid = -1
        for item in player.items:
            if item['id'] == id:
                rid = c
            c += 1
        if rid > -1:
            del player.items[rid]

# nu börjar vi
seed(datetime.now())
metafil = 'config.json' # lite meta info vi sparar i dung
dmf = open(metafil)
dung = json.load(dmf)
# vi skriver ut dung['intro'] när spelet börjar
# och vi skriver ut dung['outro'] när vi kommer till ett
# rum utan någon exit. Då har vi klarat spelet.
d = Dungeon(dung['roomfile'],dung['itemfile'], dung['startRoom'])
p = Player(d.startRoom)
p.items = d.getPlayerItems()
d.enterRoom(p.roomId)

print(bcolors.BOLD + bcolors.HEADER + dung['intro'] + bcolors.ENDC + "\n\n")
# lets print the first room!
d.printRoom()


# vi initierar lite räknare och metadata saker
dung_turncount = 0 # hur många turns vi spelat.
dung_current_room = d.startRoom

# lite ord vi vill hålla koll på
# ta emot våra commandon
while True:
    data = input(bcolors.OKGREEN + choice(dung['askForInput']) + bcolors.ENDC)
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
        print("ingasvordomar laddade")

    # kolla alla commandon
    commNotIssued = True
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
                    print(choice(dung['commands']['drop']['response']) + i['name'])
                    d.addItem(p.roomId,i)
                    p.removeItem(i['id'])
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
                print(item['takeMessage'])
                # ta bort från dungeon
                d.removeItem(item['id'])
                p.items.append(item)
            else:
                print(choice(dung['commands']['take']['errorResponse']) + takething + ".")

    elif comm[0] == 'titta' or comm[0] == 'undersök' or comm[0] == 'se':
        if len(comm) < 2:
            d.printRoom()
        else:
            ritems = d.getRoomItems(p.roomId)
            if len(ritems) > 0:
                for item in ritems:
                    if comm[1] == item['name']:
                        print(item['Description'])
            for item in p.items:
                if comm[1] == item['name']:
                    print(item['Description'])

    elif comm[0] == 'gå':
        # get next part
        if len(comm) > 1 and comm[1] in d.rooms[p.roomId]['exits']:
            p.roomId = d.rooms[p.roomId]['exits'][comm[1]]
            d.enterRoom(p.roomId)
            d.printRoom()
        else:
            print("Du kan inte gå dit.")
    elif comm[0] == 'släng':
        print("slängsläng")
    elif comm[0] == 'hejdå':
        break
    else: # som sista utväg kolla exits
        if comm[0] in d.rooms[p.roomId]['exits']:
            p.roomId = d.rooms[p.roomId]['exits'][comm[0]]
            d.enterRoom(p.roomId)
            d.printRoom()
        else:
            print("Jag förstår inte vad du menar.")



print("Hejdå! Tack för att du spelade.")
