# json-textadventure-engine
A small engine to create classic text adventures using json files.

This started out as a small project when my son and i found and old
abandoned graveyard near a school. We started to talk about how cool
it would be if we made a computer game where we could explore a graveyard
just like the one we found, but with quests and exploring of secret underground
caves and such.
I remembered the old text games from infocom, like zork, and the old collossal caves
and started to write it in python, in a way so that it would be easy to 
add to the adventure by just editing json files.

Then i added support for creating the whole game in json files, and even 
have it in your own language.

Right now the basic principle is this:
## config.json

the config.json file includes some basic config. But the main thing is the commands.
The commands are hardcoded in the python game, but you can change what they are called.
for example:

```
"take": {
      "alias": ["take","get","grab"],
      "emptyResponse": ["What do you want to take?", "You need to say what you want!", "You grab some nothing, but it slips through your fingers."],
      "errorResponse": ["You can not take ", "No you can not take "]
    },
```
The above is the take command to take some object found in a room.
The game will not react to the command take if you type it. It will react to the "alias" you give it. 
The one of the emptyResponse items in the list will be typed by the game if you dont specify what
you are taking. And the errorResponse will be typed by the game if the thing you specify dont exist in the room where you are. The thing you specified will be added to the string as well. (You can not take <thing>) 


```
    "drop": {
      "alias": ["släng","lämmna", "kasta"],
      "emptyResponse": ["Vad är det du vill slänga?","Du måste säga vad", "Släng vaddå?"],
      "response": ["Slänger ","Kastar ","Sular iväg ", "Hejdå "],
      "errorResponse": "Du kan inte slänga ",
      "nothingToThrow": "Du har inget att slänga"
    },
```
Above is the drop command, but in a game written in swedish. This game will react to "släng" etc as the swedish word for throwing away something.
The emptyResponse is the same as for the take command, but the responses are in swedish.
the response will be typed when you sucessfully drop the object. errorResponse works just tlike the take version and nothingToThrow is used if you have nothing in your inventory at all.

You also have swearwords.
Words that do not impact the game at all but you still want the game to react to them.
They are called swearwords, but do not need to be of course.

Below is in swedish. Every time the game engine detects one of the swearwords, it will randomly answer with one of the swear_responses.
```
"swearwords":
  [
    "fan","röv","helvete","skit","piss","djävla","kuk","fitta","pingvindjävul"
  ],
  "swear_responses":
  [
    "Jag förstår inte varför du skriver fula ord.",
    "Du känner hur ordet du skriver smakar illa i munnen. Tvätta genast munnen med tvål!",
    "En STOR FET DRAKE HOPPAR UPP OCH BITER HUVUDET AV DIG!! Nej jag bara skojar. Men svär inte tack!",
    "Tycker du att du låter intelligent när du skriver så?",
    "Lugna ner dig ett hekto va? måste du svära?",
    "Kan du inte några bättre ord än så?",
    "Det där hjälper knappast"
  ]
```

More to come.. This is a work in progress.
