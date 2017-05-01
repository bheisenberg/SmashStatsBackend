#Created by Brian Eisenberg 4/25/2017
import smash_gg_connector
import melee
import grequests
import requests

class Player_Container():
    def __init__(self, player_dict, player_list):
        self.player_dict = player_dict
        self.player_list = player_list


class Player_Loader():
    def __init__(self, tournaments):
        self.tournaments = tournaments
        self.players = {}
        self.player_list = []

    def get_entrant_page(self, entrant_id):
        head = 'https://api.smash.gg/phase_group/'
        tail = '?expand[]=entrants'
        return '{0}{1}{2}'.format(head, entrant_id, tail)

    def get_entrant_pages(self):
        entrant_pages = []
        for tournament in self.tournaments:
            for phase_id in tournament.phase_ids:
                entrant_pages.append(self.get_entrant_page(phase_id))
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

    def exception_handler(self, request, exception):
        print(exception)

    def load_players(self):
        urls = self.get_entrant_pages()
        session = requests.Session()
        rs = (grequests.get(url, session=session) for url in urls)
        for r in grequests.imap(rs, exception_handler=self.exception_handler, size=200):
            self.parse_entrant_page(r)
        print(len(self.players))
        return Player_Container(self.players, self.player_list)

    def parse_entrant_page(self, r):
        print(r.url)
        entrant_page = r.json()
        entities = entrant_page['entities']
        if 'entrants' in entities:
            #print('has entrants')
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
                if not melee_player in self.player_list:
                    self.player_list.append(melee_player)
                #print(melee_player.to_string())

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