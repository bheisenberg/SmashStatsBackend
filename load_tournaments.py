import json
import codecs
import urllib.parse
import urllib.request
import time
import string_operations
import melee
import gg

base_url = 'https://api.smash.gg/public/tournaments/schedule?expand[]&page=1&per_page=100'

class TournamentLoader:
    def __init__(self, container):
        self.container = container
        self.pages = 2

    def melee_slug(self, tournament):
        tid = str(tournament['id'])
        #num_events = tournament['mutations']['cardData'][tid]['eventData']['count']
        #print(num_events)
        top_events = tournament['mutations']['cardData'][tid]['eventData']['topEvents']
        num_events = len(top_events)
        #print(top_events)
        for x in range(0, num_events):
            #print(top_events[x]['name'])
            if top_events[x]['name'] == "Melee Singles":
                return top_events[x]['slug']

    def tournament_complete(self, tournament):
        tid = str(tournament['id'])
        return bool(tournament['mutations']['cardData'][tid]['hasRegistrationEnded'])

    def valid_tournament (self, tournament):
        return self.melee_slug(tournament) is not None and self.tournament_complete(tournament)

    def get_urls(self, pages):
        x = 1
        urls = []
        while (x < pages):
            url = 'https://api.smash.gg/public/tournaments/schedule?expand[]&page={0}&per_page={1}'.format(x, 100)
            urls.append(url)
            x += 1
        return urls

    def load_tournaments(self):
        print('loading tournaments')
        start_time = time.time()
        pages = gg.Connection(base_url).pages
        connection = gg.Async_Connection(self.get_urls(pages))
        tournaments = connection.data_list
        for tournament in tournaments:
            if (self.valid_tournament(tournament)):
                name = format(tournament['name'])
                tid = str(tournament['id'])
                slug = self.melee_slug(tournament)
                date = tournament['startAt']
                tournament = melee.Tournament(name, date, tid, gg.phase(slug), gg.entrants(slug))
                self.container.Tournaments[tid] = tournament
                print('{0} added to tournaments'.format(name))
        '''while (x < self.pages):
            url = 'https://api.smash.gg/public/tournaments/schedule?expand[]&page={0}&per_page={1}'.format(x, per_page)
            connection = gg.Connection(url)
            self.pages = connection.pages
            tournaments = gg.tournaments(connection.data)
            for tournament in tournaments:
                if(self.valid_tournament(tournament)):
                    name = format(tournament['name'])
                    tid = str(tournament['id'])
                    slug = self.melee_slug(tournament)
                    date = tournament['startAt']
                    tournament = melee.Tournament(name, date, tid, gg.phase(slug), gg.entrants(slug))
                    self.container.Tournaments[tid] = tournament
                    #print('{0} added to tournaments'.format(name))
            x += 1'''
        #print('Tournaments: {0}'.format(tournaments))
        #print('Finished in {0} seconds'.format(time.time()-start_time))