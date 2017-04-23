import json
import codecs
import urllib.parse
import urllib.request
import time

Tournaments = {}

class Player:
    players = []

    def __init_(self, name, wins, losses):
        self.name = name
        self.wins = wins
        self.losses = losses
        Player.players.append(self)

    def add_win (self, amount):
        self.wins += amount

    def add_loss (self, amount):
        self.losses += amount

    def add_to_record (self, wins, losses):
        self.wins += wins
        self.losses += losses


class Tournament:
    def __init__(self, name, phase_groups_slug, entrants_slug, date, tid):
        api = 'https://api.smash.gg/'
        self.name = name
        self.date = date
        self.tid = tid
        self.phase_groups_url = '{0}{1}'.format(api, phase_groups_slug)
        self.entrants_url = '{0}{1}'.format(api, entrants_slug)

    def get_name(self):
        return self.name

    def get_phase_groups_url(self):
        return self.phase_groups_url

    def get_entrants_url(self):
        return self.entrants_url



def melee_slug(num_events, top_events):
    for x in range(0, num_events):
        if top_events[x]['name'] == "Melee Singles":
            return top_events[x]['slug']
        else:
            return None


def load_tournaments():
    reader = codecs.getreader("utf-8")
    start_time = time.time()
    per_page = 100
    pages = int(json.load(reader(urllib.request.urlopen('http://api.smash.gg/public/tournaments/schedule?expand[]&page=1&per_page=1')))['total_count']/per_page)
    print(pages)
    tournaments = 0
    #data = None

    #response = urllib.request.urlopen('https://api.smash.gg/public/tournaments/schedule?expand[]&page=1&per_page={0}'.format(per_page))
    #data = json.load(reader(response))

    for x in range (1, pages):

        url = 'https://api.smash.gg/public/tournaments/schedule?expand[]&page={0}&per_page={1}'.format(x, per_page)
        response = urllib.request.urlopen(url)
        data = json.load(reader(response))
        for tournament in data['items']['entities']['tournament']:
            raw_name = tournament['name']
            split_line = str.split(raw_name)
            name = ""
            for x in range(0, len(split_line)):
                name += split_line[x]
                if x < len(split_line)-1:
                    name+="_"

            tid = str(tournament['id'])
            num_events = tournament['mutations']['cardData'][tid]['eventData']['count']
            top_events = tournament['mutations']['cardData'][tid]['eventData']['topEvents']
            complete = bool(tournament['mutations']['cardData'][tid]['hasRegistrationEnded'])
            slug = melee_slug(num_events, top_events)
            date = tournament['startAt']
            if slug is not None and complete:
                tournaments += 1
                t = Tournament(name,slug+'/phase_groups?expand=[]groups&per_page=100', slug+'/standings?expand[0]=entrants', date, tid)
                print('{0} added to tournaments'.format(name))
                Tournaments[name] = t
                print('{0} {1}'.format(Tournaments[name].phase_groups_url, Tournaments[name].name))
    print('Tournaments: {0}'.format(tournaments))
    print('Finished in {0} seconds'.format(time.time()-start_time))

    with codecs.open("tournaments.txt", "w", encoding='utf-8') as text:
        for tourney in Tournaments:
            text.write('{0} {1} {2} {3}'.format(Tournaments[tourney].phase_groups_url, Tournaments[tourney].name, Tournaments[tourney].date, Tournaments[tourney].tid)+'\n')
    #data = json.load(reader(response))
    #for tournament in data['items']['entities']['tournament']:
        #if tournament['hasRegistrationEnded'] == 'true':
        #
        #print(tid)
        #complete = bool(tournament['mutations']['cardData'][tid]['hasRegistrationEnded'])
        #if complete:
        #print (tournament['name'])

#print(data['items']['entities']['tournament'][0]['id'])
load_tournaments()
#for event in data['items']['entities']['event']:
    #if event['name'] == "Melee Singles":
        #print(event['name'])


