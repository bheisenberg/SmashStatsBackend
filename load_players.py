import smash_gg_connector
import melee

class Player_Loader():
    def __init__(self, tournaments):
        self.tournaments = tournaments
        self.players = {}

    def get_entrant_pages(self):
        entrant_pages = []
        for tournament in self.tournaments:
            for entrant_page in self.tournaments[tournament].entrants:
                entrant_pages.append(entrant_page)
        return entrant_pages

    def get_player_urls(self):
        urls = []
        for player in self.players.values():
            urls.append('https://api.smash.gg/player/{0}'.format(player))
        return urls

    def format_string(self, string):
        if string is not None: return string.replace(' ', '_')

    def get_players(self, player_data):
        if 'entrants' in player_data['entities']:
            for entrant in player_data['entities']['entrants']:
                if entrant['id'] not in self.players:
                    entrant_id = (entrant['id'])
                    participant = entrant['participantIds'][0]
                    try:
                        if type(entrant['playerIds']) == dict:
                            player = entrant['playerIds'][str(participant)]
                            self.players[entrant_id] = player
                        else:
                            player = entrant['playerIds'][0]
                            self.players[entrant_id] = player

                    except:
                        print("Player could not be loaded")

    def load_players(self):
        print('loading players...')
        connection = smash_gg_connector.Async_Connection(self.get_entrant_pages())
        entrant_data = connection.data_list
        for entrant_page in entrant_data:
            self.get_players(entrant_page)
        return self.create_players()

    def create_players(self):
        print("Creating players...")
        connection = smash_gg_connector.Async_Connection(self.get_player_urls())
        player_data = connection.data_list
        for player in player_data:
            if(player is not None):
                player_entity = player['entities']['player']
                player_id = player_entity['id']
                tag = self.format_string(player_entity['gamerTag'])
                prefix = self.format_string(player_entity['prefix'])
                state = player_entity['state']
                country = self.format_string(player_entity['country'])
                player = melee.Player(player_id, tag, prefix, state, country)
                self.players[player_id] = player
                print(player.to_string())
        return self.players