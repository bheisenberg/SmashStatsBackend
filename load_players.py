#Created by Brian Eisenberg 4/25/2017
import smash_gg_connector
import melee

class Player_Loader():
    def __init__(self, tournaments):
        self.tournaments = tournaments
        self.players = {}

    def get_entrant_pages(self):
        entrant_pages = []
        with open('text/entrant_pages.txt', 'w', encoding='utf-8') as text:
            for tournament in self.tournaments.values():
                for entrant_page in tournament.entrant_pages:
                    text.write('{0}\n'.format(entrant_page))
                    entrant_pages.append(entrant_page)
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

    def create_entrants_dict(self):
        entrants = {}
        print('loading entrants...')
        entrant_pages = self.get_entrant_pages()
        connection = smash_gg_connector.Async_Connection(entrant_pages)
        entrant_data = connection.data_list
        for entrant_page in entrant_data:
            if self.has_entrants(entrant_page):
                for entrant in self.get_entrants(entrant_page):
                    entrant_id = entrant['id']
                    if entrant_id not in entrants.keys():
                        participant = entrant['participantIds'][0]
                        try:
                            player = entrant['playerIds'][str(participant)] if type(entrant['playerIds']) == dict else entrant['playerIds'][0]
                            entrants[entrant_id] = player
                        except:
                            print("Player could not be loaded")
        return self.create_players(entrants)

    def create_players(self, entrants):
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
        return self.players