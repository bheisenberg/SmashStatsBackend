import json
import codecs
import urllib.parse
import urllib.request
import sqlite3
import time

conn = sqlite3.connect('melee.sqlite')
cur = conn.cursor()
reader = codecs.getreader("utf-8")

Players = []
PlayerStrings = []
Player_Dict = {}
start_time = 0

def load_dict():
    print("Loading dictionary...")
    with open('playersbyid.txt', 'r') as players:
        unique_ids = 0
        for playerline in players:
            playerid = int(playerline.split()[1])
            if(playerid not in Players):
                Players.append(playerid)
                print(playerid)
                unique_ids +=1
    print("Dictionary loaded with {0} unique ids".format(unique_ids))

def load_players():
    print("Loading players...")
    start_time = time.time()
    reader = codecs.getreader("utf-8")
    for player in Players:
        url = 'https://api.smash.gg/player/{0}'.format(player)
        response = urllib.request.urlopen(url)
        data = json.load(reader(response))
        player_entity = data['entities']['player']
        player_id = player_entity['id']
        tag = format_string(player_entity['gamerTag'])
        prefix = format_prefix(player_entity['prefix'])
        state = player_entity['state']
        country = format_string(player_entity['country'])
        player_string = '{0} {1} {2} {3} {4}'.format(player_id, tag, prefix, state, country)
        PlayerStrings.append(player_string)
        print(player_string)
        #Player_Dict[player_id] = tag
        #print('[{0}] {1} added to dict'.format(player_id, Player_Dict[player_id]))

def format_string(loaded_string):
    if loaded_string == None or loaded_string == "":
        return None
    temp_tag = loaded_string
    tag_split = temp_tag.split()
    formatted_string = ""
    for x in range(0, len(tag_split)):
        formatted_string += tag_split[x]
        if x < len(tag_split) - 1:
            formatted_string += "_"
    return formatted_string

def format_prefix(loaded_prefix):
    if loaded_prefix != None:
        if loaded_prefix != "":
            if len(loaded_prefix.split()) > 1:
                prefix = format_string(loaded_prefix)
            else:
                prefix = loaded_prefix
        else:
            prefix = None
        return prefix
    else:
        return None

def write_dict():
    print('Writing to dictionary...')
    with codecs.open('playerdict.txt', 'w', encoding='utf-8') as out:
        for player in PlayerStrings:
            out.write(player+'\n')
    print('finished in: {0}'.format(time.time() - start_time))

load_dict()
load_players()
write_dict()
