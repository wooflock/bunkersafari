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
