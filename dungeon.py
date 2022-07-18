import json

class Dungeon:
    def __init__(dungeon,roomfile,itemsfile,startRoom):
        dungeon.roomfile = roomfile
        dungeon.rf = open(dungeon.roomfile)
        dungeon.rooms = json.load(dungeon.rf)
        dungeon.itemsfile = itemsfile
        dungeon.itf = open(dungeon.itemsfile)
        dungeon.items = json.load(dungeon.itf)
        dungeon.startRoom = startRoom
    def getPlayerItems(dungeon):
        playerItems = []
        for item in dungeon.items:
            if 'pid' in dungeon.items[item]:
                playerItems.append(dungeon.items[item])
                playerItems[-1]['id'] = item

        if len(playerItems) > 0:
            for ritem in playerItems:
                dungeon.removeItem(ritem['id'])
        return playerItems

    def getRoomItems(dungeon, rid):
        dungeon.currentItems = []
        for item in dungeon.items:
            if 'pid' in dungeon.items[item]:
                continue
            irid = dungeon.items[item]['rid']
            if irid == dungeon.currentroom:
                dungeon.currentItems.append(dungeon.items[item])
                dungeon.currentItems[-1]['id'] = item
        return dungeon.currentItems

    def getRoomItemByName(dungeon, rid, name):
        items = dungeon.getRoomItems(rid)
        empty = []
        for item in items:
            if 'pid' not in item:
                if name == item['name']:
                    return item
        return empty

    def removeItem(dungeon,id):
        del dungeon.items[id]
    def addItem(dungeon, rid, additem):
        additem['rid'] = rid
        additem['hint'] = additem['hint2']
        dungeon.items[additem['id']] = additem
    def enterRoom(dungeon, rid):
        dungeon.currentroom = rid
        #dungeon.currentItems = dungeon.getItems(dungeon.currentroom)
    def printItems(dungeon):
        items = dungeon.getRoomItems(dungeon.currentroom)
        if len(items) > 0:
            for item in items:
                print(item['hint'])
    def printRoom(dungeon):
        try: # check if we have defined a colour for our room..
            dungeon.rooms[dungeon.currentroom]['colour']
        except KeyError:
            dungeon.rooms[dungeon.currentroom]['colour'] = None

        colour = dungeon.rooms[dungeon.currentroom]['colour']
        colourstr = ''
        endcolourstr = '\033[0m'

        if colour == 'blue':
            colourstr = '\033[94m'
        elif colour == 'cyan':
            colourstr = '\033[96m'
        elif colour == 'mauve':
            colourstr = '\033[95m'
        elif colour == 'yellow':
            colourstr = '\033[93m'
        elif colour == 'green':
            colourstr = '\033[92m'
        elif colour == 'red':
            colourstr = '\033[91m'
        else:
            endcolourstr = ''

        print("\n" + colourstr + dungeon.rooms[dungeon.currentroom]['name'] + endcolourstr)

        #if colour is not None and (colour == 'blue' or colour == 'cyan' or colour == 'mauve' or colour == 'yellow' or colour == 'green' or colour == 'red'):

        print(dungeon.rooms[dungeon.currentroom]['enterDescription'])
        dungeon.printItems()
        # ladda utgångar
        e = dungeon.rooms[dungeon.currentroom]['exits']
        sep = ', '
        exits = sep.join(e)
        if len(exits) > 1:
            print("Det finns utgångar " + exits)
