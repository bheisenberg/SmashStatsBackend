import grequests
import melee


def format_string(string):
    if string is not None: return string.replace(' ', '_')


def has_entrants(entrant_data):
    return 'entrants' in entrant_data['entities']


def get_entrants(entrant_data):
    return entrant_data['entities']['entrants']

def parse_entrant(r, **kwargs):
    entrants_dict = {}
    # print('loading entrants... from {0} phases'.format(len(self.phases)))
    # entrant_pages = self.get_entrant_pages()
    print(r.url)
    print(r)
    entrant_page = r.json()
    entities = entrant_page['entities']
    if 'entrants' in entities:
        entrants = entities['entrants']
        players = entities['player']
        for entrant, player in zip(entrants, players):
            entrant_id = entrant['id']
            player_id = player['id']
            tag = format_string(player['gamerTag'])
            prefix = format_string(player['prefix'])
            state = player['state']
            country = format_string(player['country'])
            melee_player = melee.Player(player_id, tag, prefix, state, country)
            print(melee_player.to_string())
            players[entrant_id] = melee_player


def load_players():
    sites = []
    urls = ['https://api.smash.gg/phase_group/241620?expand[]=entrants']
    for u in urls:
        rs = grequests.get(u, hooks=dict(response=parse_entrant))
        sites.append(rs)
    grequests.map(sites)

load_players()
