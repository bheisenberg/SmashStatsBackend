import requests
import grequests
import melee

player_dict = {}
phase_sets = []
sets = []

class Set_page:
    def __init__(self, set_page, tid):
        self.set_page = set_page
        self.tid = tid


def get_set_page(set_id):
    head = 'https://api.smash.gg/phase_group/'
    tail = '?expand[]=sets'
    return '{0}{1}{2}'.format(head, set_id, tail)

def get_set_pages(phases):
    set_pages = []
    for phase in phases:
        set_pages.append(Set_page(get_set_page(phase.phase_id), phase.tid))
    return set_pages

def exception_handler(request, exception):
        print(exception)

def load_sets (players, phases):
    print('populating sets')
    global sets
    global  player_dict
    player_dict = players
    set_pages = get_set_pages(phases)
    session = requests.Session()
    rs = (grequests.get(url.set_page, session=session) for url in set_pages)
    for r, Set_page.tid in zip(grequests.imap(rs, exception_handler=exception_handler, size=200), set_pages):
        parse_set_page(r, Set_page.tid)
    return sets

def valid_set(set_obj):
    return set_obj['entrant1Id'] is not None and set_obj['entrant2Id'] is not None and set_obj['entrant1Score'] is not None and set_obj['entrant2Score'] is not None

def parse_set_page (r, tid):
    global player_dict
    global sets
    url = r.url
    print(url)
    set_data = r.json()
    entities = set_data['entities']
    if 'sets' in entities:
        phase_sets = entities['sets']
        for set_obj in phase_sets:
            if valid_set(set_obj):
                try:
                    entrant1 = player_dict[set_obj['entrant1Id']].pid
                    entrant2 = player_dict[set_obj['entrant2Id']].pid
                    entrant1_score = set_obj['entrant1Score']
                    entrant2_score = set_obj['entrant2Score']
                    new_set = melee.TournamentSet(entrant1, entrant1_score, entrant2, entrant2_score, tid)
                    print(new_set.to_string())
                    sets.append(new_set)
                except:
                    print('Failed to load set, likely due to a missing player id')