#Created by Brian Eisenberg 4/25/2017
import smash_gg_connector
import melee
import grequests
import requests
import time
import pymysql

class Player_Container():
    def __init__(self, player_dict, player_list):
        self.player_dict = player_dict
        self.player_list = player_list


class Player_Loader():
    def __init__(self, phases):
        self.phases = phases
        self.player_dict = {}
        self.player_list = []
        self.placements = []

    def get_entrant_page(self, entrant_id):
        head = 'https://api.smash.gg/phase_group/'
        tail = '?expand[]=entrants'
        return '{0}{1}{2}'.format(head, entrant_id, tail)

    def get_entrant_pages(self):
        entrant_pages = []
        for phase_page in self.phases:
            entrant_pages.append(self.get_entrant_page(phase_page.phase_id))
        return entrant_pages

    def get_player_urls(self, entrants):
        urls = []
        with open('text/player_urls.txt', 'w', encoding='utf-8') as text:
            for player in entrants.values():
                text.write('https://api.smash.gg/player/{0}\n'.format(player))
                urls.append('https://api.smash.gg/player/{0}'.format(player))
        return urls

    def format_string(self, string):
        if string is not None:
            new_string = string
            if '"' in new_string or "'" in new_string:
                return new_string.replace('"', r'\"').replace("'", r"\'")
            else:
                return new_string.replace('\\', "\\\\")
        else:
            return ''

    def has_entrants(self, entrant_data):
        return 'entrants' in entrant_data['entities']

    def get_entrants(self, entrant_data):
        return entrant_data['entities']['entrants']

    def exception_handler(self, request, exception):
        print(exception)

    def get_player_id(self, participant_id, player_ids):
        if type(player_ids) is dict:
            return player_ids[participant_id]
        elif type(player_ids) is list and len(player_ids) > 0:
            return player_ids[0]
        else:
            return None

    def load_players(self):
        #TODO: Add support for placings using finalPlacement
        urls = self.get_entrant_pages()
        session = requests.Session()
        rs = (grequests.get(url, session=session) for url in urls)
        for r in grequests.imap(rs, exception_handler=self.exception_handler, size=200):
            self.parse_entrant_page(r)
            time.sleep(0.01)
        print(len(self.player_dict))
        return Player_Container(self.player_dict, dict((obj.pid, obj) for obj in self.player_list).values())

    def parse_entrant_page(self, r):
        print(r.url)
        entrant_page = r.json()
        entities = entrant_page['entities']
        if 'entrants' in entities:
            entrants = entities['entrants']
            players = entities['player']
            player_dict = {p['id']: p for p in players}
            for entrant in entrants:
                participant_id = str(entrant['participantIds'][0])
                player_ids = entrant['playerIds']
                player_id = self.get_player_id(participant_id, player_ids)
                if player_id is not None:
                    player = player_dict[player_id]
                    entrant_id = entrant['id']
                    tag = self.format_string(player['gamerTag'])
                    prefix = self.format_string(player['prefix'])
                    state = player['state']
                    country = self.format_string(player['country'])
                    melee_player = melee.Player(player_id, tag, prefix, state, country)
                    if not entrant_id in self.player_dict.keys():
                        self.player_dict[entrant_id] = melee_player
                        print(melee_player.to_string())
                    if not melee_player in self.player_list:
                        self.player_list.append(melee_player)
