import json
import codecs
import urllib.parse
import urllib.request
import time
import sqlite3
import time

Players = {}
Sets = []
rip_counter = 0

def load_players ():
    with open("text/playersbyid.txt") as text:
        for line in text:
            splitline = str.split(line)
            entrant = int(splitline[0])
            playerid = int(splitline[1])
            Players[entrant] = playerid
            print("{0} {1}".format(entrant, Players[entrant]))

def populate_sets ():
    global rip_counter
    print("Populating sets")
    with open("setgroups.txt", "r") as text:
        start_time = time.time()
        for line in text:
            print(line)
            split_line = str.split(line)
            sets = split_line[0]
            tournament = split_line[1]
            #print('{0} elapsed'.format(time.time()-start_time))
            response = urllib.request.urlopen(sets)
            data = json.load(reader(response))
            if 'sets' in data['entities']:
                for set in data['entities']['sets']:
                    try:
                        if(set['entrant1Id']) is not None:
                            entrant1 = Players[set['entrant1Id']]
                        else:
                            entrant1 = None

                        if(set['entrant2Id']) is not None:
                            entrant2 = Players[set['entrant2Id']]
                        else:
                            entrant2 = None

                        if(set['entrant1Score']) is not None:
                            entrant1Score = set['entrant1Score']
                        else:
                            entrant1Score = None

                        if(set['entrant2Score']) is not None:
                            entrant2Score = set['entrant2Score']
                        else:
                            entrant2Score = None

                        winner_placement = set['wPlacement'] if not (set['wPlacement'] == None) else None
                        loser_placement = set['lPlacement'] if not (set['lPlacement'] == None) else None
                        round_num = set['displayRound']
                        print('{0}: {1}, {2}: {3} {4} {5} {6} from tournament {7}'.format(entrant1, entrant1Score, entrant2, entrant2Score, winner_placement, loser_placement, round_num, tournament))
                        Sets.append('{0} {1} {2} {3} {4} {5} {6} {7}'.format(entrant1, entrant1Score, entrant2, entrant2Score, winner_placement, loser_placement, round_num, tournament))
                        #print('{0}: {1}, {2}: {3} {4}'.format(entrant1, entrant1Score, entrant2, entrant2Score, tournament))
                        #Sets.append('{0} {1} {2} {3} {4}'.format(entrant1, entrant1Score, entrant2, entrant2Score, tournament))
                    except:
                        print("rip")
                        rip_counter +=1


def write_sets():
    with open("sets.txt", "w") as text:
        for set in Sets:
            print(set, file=text)
            print('added {0}'.format(set))
        print('Done.')

load_players()
populate_sets()
write_sets()