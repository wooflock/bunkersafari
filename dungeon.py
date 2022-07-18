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
        print(dungeon.rooms[dungeon.currentroom]['name'])
        print(dungeon.rooms[dungeon.currentroom]['enterDescription'])
        dungeon.printItems()
        # ladda utgångar
        e = dungeon.rooms[dungeon.currentroom]['exits']
        sep = ', '
        exits = sep.join(e)
        if len(exits) > 1:
            print("Det finns utgångar " + exits)
