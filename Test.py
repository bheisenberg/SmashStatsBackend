import grequests
import melee


def format_string(self, string):
    if string is not None: return string.replace(' ', '_')


def has_entrants(entrant_data):
    return 'entrants' in entrant_data['entities']


def get_entrants(entrant_data):
    return entrant_data['entities']['entrants']

def parse_entrant(r, **kwargs):
    print(r.url)

    entrant_page = r.json()
    entities = entrant_page['entities']
    if 'entrants' in entities:
        print('has entrants')
        entrants = entities['entrants']
        players = entities['player']
        for entrant, player in zip(entrants, players):
            entrant_id = entrant['id']
            player_id = player['id']
            tag = format_string(player['gamerTag'])
            prefix = format_string(player['prefix'])
            state = player['state']
            country = format_string(player['country'])
            player = melee.Player(player_id, tag, prefix, state, country)
            players[entrant_id] = player
            print(player.to_string())

def load_players():
    sites = []
    urls = ['http://api.smash.gg/phase_group/117894?expand[]=entrants']
    for u in urls:
        rs = grequests.get(u, hooks=dict(response=parse_entrant))
        sites.append(rs)
    grequests.map(sites)

load_players()
