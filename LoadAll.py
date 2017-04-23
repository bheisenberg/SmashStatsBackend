import json
import codecs
import urllib.parse
import urllib.request
import time

Tournaments = {}

class Player:
    def __init_(self, id, name):
        self.id = id
        self.name = name

class TournamentData:
    def __init__(self, name, phase_groups_slug, entrants_slug):
        api = 'https://api.smash.gg/'
        self.name = name.encode('utf-8')
        self.phase_groups_url = '{0}{1}'.format(api, phase_groups_slug)
        self.entrants_url = '{0}{1}'.format(api, entrants_slug)

    def get_name(self):
        return self.name

    def get_phase_groups_url(self):
        return self.phase_groups_url

    def get_entrants_url(self):
        return self.entrants_url

class Set:
    def __init__(self, tournament_id, entrant1Id, entrant2Id, entrant1Score, entrant2Score):
        self.tournament_id = tournament_id
        self.entrant1Id = entrant1Id
        self.entrant2Id = entrant2Id
        self.entrant1Score = entrant1Score
        self.entrant2Score = entrant2Score






def melee_slug(num_events, top_events):
    for x in range(0, num_events):
        if top_events[x]['name'] == "Melee Singles":
            return top_events[x]['slug']
        else:
            return None


def load_tournaments():
    start_time = time.time()
    per_page = 100
    pages = 25
    tournaments = 0
    #data = None
    reader = codecs.getreader("utf-8")
    #response = urllib.request.urlopen('https://api.smash.gg/public/tournaments/schedule?expand[]&page=1&per_page={0}'.format(per_page))
    #data = json.load(reader(response))

    for x in range (1, pages):

        url = 'https://api.smash.gg/public/tournaments/schedule?expand[]&page={0}&per_page={1}'.format(x, per_page)
        response = urllib.request.urlopen(url)
        data = json.load(reader(response))
        for tournament in data['items']['entities']['tournament']:
            name = tournament['name']
            tid = str(tournament['id'])
            num_events = tournament['mutations']['cardData'][tid]['eventData']['count']
            top_events = tournament['mutations']['cardData'][tid]['eventData']['topEvents']
            complete = bool(tournament['mutations']['cardData'][tid]['hasRegistrationEnded'])
            slug = melee_slug(num_events, top_events)
            if slug is not None and complete:
                tournaments += 1
                t = Tournament(name,slug+'/phase_groups?expand=[]groups&per_page=100', slug+'/standings?expand[0]=entrants')
                print('{0} added to tournaments'.format(name))
                Tournaments[name] = t
    print('Tournaments: {0}'.format(tournaments))
    print('Finished in {0} seconds'.format(time.time()-start_time))

    with open("tournaments.txt", "w") as text:
        for tourney in Tournaments:
            print(Tournaments[tourney].phase_groups_url, file=text)
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


