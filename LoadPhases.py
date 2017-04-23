import json
import codecs
import urllib.parse
import urllib.request
import time
import sqlite3

conn = sqlite3.connect('melee.sqlite')
cur = conn.cursor()

groups = []
setgroups = []

def load_groups():
    reader = codecs.getreader("utf-8")
    with open("tournaments.txt", "r") as text:
        for line in text:
            split_line = str.split(line)
            url_line = split_line[0]
            tournament = split_line[3]
            response = urllib.request.urlopen(url_line)
            data = json.load(reader(response))
            print(line)
            if data['total_count'] > 1:
                for entity in data['items']['entities']['groups']:
                    groups.append('http://api.smash.gg/phase_group/{0}?expand[]=entrants'.format(entity['id']))
                    setgroups.append('http://api.smash.gg/phase_group/{0}?expand[]=sets {1}'.format(entity['id'], tournament))
                    #print('phase {0} from tournament {1} added to phases'.format(entity['id'], tournament))
            elif data['total_count'] == 1:
                item = data['items']['entities']['groups']['id']
                groups.append('http://api.smash.gg/phase_group/{0}?expand[]=entrants'.format(item))
                setgroups.append('http://api.smash.gg/phase_group/{0}?expand[]=sets {1}'.format(item, tournament))
                #print('{0} added to phases (single group)'.format(item))

def write_player_groups():
    with open("groups.txt", "w") as text:
        for item in groups:
            print(item, file=text)
            print('{0}added to text'.format(item))
        print('Done.')

def write_set_groups():
    with open("setgroups.txt", "w") as text:
        for item in setgroups:
            print(item, file=text)
            print('{0}added to text'.format(item))
        print('Done.')

load_groups()
write_player_groups()
write_set_groups()
