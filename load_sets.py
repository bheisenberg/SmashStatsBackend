import requests
import grequests
import melee

player_dict = {}
placements = []
phase_sets = []
sets = []
set_pages = {}

class Set_Container:
    def __init__(self, set_page, tid):
        self.set_page = set_page
        self.tid = tid

def get_set_page(phase_id):
    head = 'https://api.smash.gg/phase_group/'
    tail = '?expand[]=sets'
    return '{0}{1}{2}'.format(head, phase_id, tail)

def get_set_pages(phases):
    set_pages = {}
    for phase in phases:
        set_page = get_set_page(phase.phase_id)
        set_pages[set_page] = Set_Container(set_page, phase.tid)
    return set_pages

def exception_handler(request, exception):
        print(exception)

def load_sets (players, phases):
    print('populating sets')
    global sets
    global player_dict
    global set_pages
    player_dict = players
    set_pages = get_set_pages(phases)
    session = requests.Session()
    rs = (grequests.get(url.set_page, session=session) for url in set_pages.values())
    for r in grequests.imap(rs, exception_handler=exception_handler, size=200):
        parse_set_page(r)
    return sets

def update_sets (players, phases):
    print('populating sets')
    global sets
    global player_dict
    global set_pages
    player_dict = players
    set_pages = get_set_pages(phases)
    session = requests.Session()
    rs = (grequests.get(url.set_page, session=session) for url in set_pages.values())
    for r in grequests.imap(rs, exception_handler=exception_handler, size=200):
        parse_set_page(r)
    return [sets, placements]

def valid_set(set_obj):
    return set_obj['entrant1Id'] is not None and set_obj['entrant2Id'] is not None and set_obj['entrant1Score'] is not None and set_obj['entrant2Score'] is not None and (int(set_obj['entrant1Score']) > 1 or set_obj['entrant2Score'] > 1) and (set_obj['entrant1Score'] >= 0 and set_obj['entrant2Score'] >= 0)

def format_round(round_num):
    return -99 if round_num is None else round_num


def parse_set_page (r):
    global player_dict
    global sets
    global set_pages
    url = r.url
    print(url)
    set_data = r.json()
    entities = set_data['entities']
    if 'sets' in entities:
        phase_sets = entities['sets']
        for set_obj in phase_sets:
            if valid_set(set_obj):
                try:
                    winner_place = set_obj['wOverallPlacement']
                    loser_place = set_obj['lOverallPlacement']
                    entrant1_id = set_obj['entrant1Id']
                    entrant2_id = set_obj['entrant2Id']
                    entrant1_score = set_obj['entrant1Score']
                    entrant2_score = set_obj['entrant2Score']
                    round_text = set_obj['shortRoundText']
                    round_division = set_obj['roundDivision']
                    player_1_id = player_dict[entrant1_id].pid
                    player_2_id = player_dict[entrant2_id].pid
                    entrant_1 = melee.Entrant(player_1_id, entrant1_score)
                    entrant_2 = melee.Entrant(player_2_id, entrant2_score)
                    tid = set_pages[url].tid
                    new_set = melee.TournamentSet(entrant_1, entrant_2, round_division, round_text, tid, url)
                        #print(loser_placement.to_string())
                    #print(new_set.to_string())
                    sets.append(new_set)
                except:
                    print('Failed to load set, likely due to a missing player id')