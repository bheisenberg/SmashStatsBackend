#Created by Brian Eisenberg 4/25/2017
import smash_gg_connector
import melee
import grequests

class Player_Loader():
    def __init__(self, phases):
        self.phases = phases
        self.players = {}

    def get_entrant_pages(self):
        entrant_pages = []
        #with open('text/entrant_pages.txt', 'w', encoding='utf-8') as text:
            #for tournament in self.tournaments.values():
                #for entrant_page in tournament.entrant_pages:
                    #text.write('{0}\n'.format(entrant_page))
                    #entrant_pages.append(entrant_page)
        #for phase in self.phases:


        return entrant_pages

    def get_player_urls(self, entrants):
        urls = []
        with open('text/player_urls.txt', 'w', encoding='utf-8') as text:
            for player in entrants.values():
                text.write('https://api.smash.gg/player/{0}\n'.format(player))
                urls.append('https://api.smash.gg/player/{0}'.format(player))
        return urls

    def format_string(self, string):
        if string is not None: return string.replace(' ', '_')

    def has_entrants(self, entrant_data):
        return 'entrants' in entrant_data['entities']

    def get_entrants(self, entrant_data):
        return entrant_data['entities']['entrants']

    def load_players(self):
        urls = self.phases
        rs = (grequests.get(url) for url in urls)
        response = grequests.map(rs)
        for item in response:
            if item is not None:
                entrant_page = item.json()
                entities = entrant_page['entities']
                if('entrants' in entities):
                    entrants = entities['entrants']
                    players = entities['player']
                    for entrant, player in zip(entrants, players):
                        entrant_id = entrant['id']
                        player_id = player['id']
                        tag = self.format_string(player['gamerTag'])
                        prefix = self.format_string(player['prefix'])
                        state = player['state']
                        country = self.format_string(player['country'])
                        melee_player = melee.Player(player_id, tag, prefix, state, country)
                        self.players[entrant_id] = melee_player
                        print(melee_player.to_string())
        print('Found {0} players'.format(len(self.players)))
        return self.players

    def parse_entrant_page(self, r, **kwargs):
        #entrants_dict = {}
        #print('loading entrants... from {0} phases'.format(len(self.phases)))
        #entrant_pages = self.get_entrant_pages()
        #print(r.url)
        #print(r.url)
        print(r)
        entrant_page = r.json()
        entities = entrant_page['entities']
        entrants = entities['entrants']
        players = entities['player']
        for entrant, player in zip(entrants, players):
            entrant_id = entrant['id']
            player_id = player['id']
            tag = self.format_string(player['gamerTag'])
            prefix = self.format_string(player['prefix'])
            state = player['state']
            country = self.format_string(player['country'])
            melee_player = melee.Player(player_id, tag, prefix, state, country)
            self.players[entrant_id] = melee_player
            print(melee_player.to_string())
        return self.players

'''def create_players(self, entrants):
    print("Creating players...")
    connection = smash_gg_connector.Async_Connection(self.get_player_urls(entrants))
    player_data = connection.data_list
    for player in player_data:
        player_entity = player['entities']['player']
        player_id = player_entity['id']
        tag = self.format_string(player_entity['gamerTag'])
        prefix = self.format_string(player_entity['prefix'])
        state = player_entity['state']
        country = self.format_string(player_entity['country'])
        player = melee.Player(player_id, tag, prefix, state, country)
        self.players[player_id] = player
    return self.players'''