import json
import codecs
import urllib.parse
import urllib.request
import time
import sqlite3
import time

conn = sqlite3.connect('melee.sqlite')
cur = conn.cursor()
reader = codecs.getreader("utf-8")

Players = {}
Entrants = []
rip_counter = 0

with open("groups.txt", "r") as text:
    start_time = time.time()
    for line in text:
        print(line)
        response = urllib.request.urlopen(line)
        data = json.load(reader(response))
        if 'entrants' in data['entities']:
            for entrant in data['entities']['entrants']:
                if entrant['id'] not in Players:
                    entrant_id = (entrant['id'])
                    participant = entrant['participantIds'][0]
                    try:
                        if type(entrant['playerIds']) == dict:
                            player = entrant['playerIds'][str(participant)]
                        else:
                            player = entrant['playerIds'][0]
                        Players[entrant_id] = player
                        print('{0} {1}'.format(entrant_id, Players[entrant_id]))
                    except:
                        print("rip")
                        rip_counter+=1

    with codecs.open('playersbyid.txt', 'w', encoding='utf-8') as out:
        for participant in Players:
            out.write('{0} {1}'.format(participant, Players[participant])+'\n')
    print('finished in: {0} with {1} rips'.format(time.time() - start_time, rip_counter))
