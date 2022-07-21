import json

class Dungeon:
    def __init__(dungeon,roomfile,itemsfile,eventtriggerfile,startRoom):
        dungeon.rooms = json.load(open(roomfile))
        dungeon.items = json.load(open(itemsfile))
        dungeon.dynamic = json.load(open(eventtriggerfile))

        dungeon.startRoom = startRoom
        dungeon.count = 1
        dungeon.playerItems = [] # so we know what the players have
        dungeon.ExtraMessage = ""
        dungeon.enterRoom(startRoom)


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
        # add a counter for how many turns we spend here if it does not exist.
        dungeon.rooms[rid]['count'] = dungeon.rooms[rid].get('count',0) + 1
        if dungeon.rooms[rid]['count'] > dungeon.count:
            dungeon.rooms[rid]['count'] = dungeon.count
        #dungeon.currentItems = dungeon.getItems(dungeon.currentroom)
    def printItems(dungeon):
        items = dungeon.getRoomItems(dungeon.currentroom)
        if len(items) > 0:
            for item in items:
                print(item['hint'])
    def checkTriggers(dungeon, function="unknown"):
        # go through all triggers and see if something has triggerd
        crid = dungeon.currentroom # so its easier to get
        croom = dungeon.rooms[crid]
        for tid in dungeon.dynamic['triggers']:
            trigger = dungeon.dynamic['triggers'][tid]
            # check the type. we have
            if trigger['type'] == 'counter': # trigger on how many turns have passed
                if trigger['value'] == dungeon.count:
                    print("EventTriggered: " + tid)
                    dungeon.triggerEvent(trigger['eventId'],function)
            elif trigger['type'] == 'roomCounter': # trigger turns in this room
                if trigger['roomId'] == crid and trigger['value'] == croom['count']:
                    print("EventTriggered: " + tid)
                    dungeon.triggerEvent(trigger['eventId'], function)
            elif trigger['type'] == 'enterRoom': # trigger reacts when someone enters room.
                if trigger['roomId'] == crid and trigger['times'] != 0:
                    trigger['times'] -= 1
                    print("EventTriggered: " + tid)
                    dungeon.triggerEvent(trigger['eventId'], function)

            elif trigger['type'] == 'itemInRoom' and trigger['times'] != 0:# trigger on item in a room
                print("itemInRoom found")
                if trigger['roomId'] == crid:
                    print("room id is correct " + crid )
                    for pi in dungeon.playerItems: # check for player items
                        if pi['id'] == trigger['itemId']:
                            print("Player itemId found" + trigger['itemId'])
                            trigger['times'] -= 1
                            dungeon.triggerEvent(trigger['eventId'], function)
                    for di in dungeon.getRoomItems(crid):
                        if di['id'] == trigger['itemId'] and di['rid'] == crid:
                            print("finding item " + di['id'] + " in room that has same event it " + trigger['itemId'])
                            trigger['times'] -= 1
                            dungeon.triggerEvent(trigger['eventId'], function)

    def triggerEvent(dungeon, triggerdEvent, function):
        event = dungeon.dynamic['events'][triggerdEvent]
        # check the event type
        if event['type'] == 'addItemToRoom':
            if event['roomId'] == 'current':
                event['roomId'] = dungeon.currentroom
            print("Event " + triggerdEvent)
            dungeon.items[event['itemId']]['rid'] = event['roomId']
        elif event['type'] == 'addExitToRoom':
            dungeon.rooms[event['roomId']]['exits'].update(event['exit'])
            dungeon.rooms[event['roomId']]['enterDescription'] += event['addEnterDescription']
            print("Event " + triggerdEvent)
        elif event['type'] == 'delExitToRoom':
            del dungeon.rooms[event['roomId']]['exits'][event['exit']]
            dungeon.rooms[event['roomId']]['enterDescription'] += event['addEnterDescription']
            print("Event " + triggerdEvent)
        elif event['type'] == 'writeMessage':

            if function == 'printRoom':
                dungeon.ExtraMessage = event['message']
            else:
                print(event['message'])

            print("Event " + triggerdEvent)


    def printRoom(dungeon):

        # chek for triggers
        dungeon.checkTriggers('printRoom')
        #print("counter " + str(dungeon.count))
        #print("RoomCount " + str(dungeon.rooms[dungeon.currentroom]['count']))

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
        if len(dungeon.ExtraMessage) > 1:
            print(dungeon.ExtraMessage)
            dungeon.extraMessage = "" # place it to zero again now we used it.
        dungeon.printItems()
        # ladda utgångar
        e = dungeon.rooms[dungeon.currentroom]['exits']
        sep = ', '
        exits = sep.join(e)
        if len(exits) > 1:
            print("Det finns utgångar " + exits)
