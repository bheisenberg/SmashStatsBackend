import requests
import grequests
import melee

tournament_list = []
player_dict = {}
tournament_dict = {}
tournaments_by_id = {}

def get_set_page(set_id):
    head = 'https://api.smash.gg/phase_group/'
    tail = '?expand[]=sets'
    return '{0}{1}{2}'.format(head, set_id, tail)

def get_set_pages(tournaments):
    set_pages = {}
    for tournament in tournaments:
        for phase_id in tournament.phase_ids:
            set_url = get_set_page(phase_id)
            set_pages[set_url] = tournament
    return set_pages

def tournaments_to_dict(tournaments):
    dict = {}
    for tournament in tournaments:
        dict[tournament.tid] = tournament

def exception_handler(request, exception):
        print(exception)

def load_sets (players, tournaments):
    print('populating sets')
    global tournament_dict
    global player_dict
    global tournaments_by_id
    player_dict = players
    tournament_dict = get_set_pages(tournaments)
    urls = tournament_dict.keys()
    session = requests.Session()
    rs = (grequests.get(url, session=session) for url in urls)
    for r in grequests.imap(rs, exception_handler=exception_handler, size=200):
        parse_set_page(r)
    return list(tournament_dict.values())

def valid_set(set_obj):
    return set_obj['entrant1Id'] is not None and set_obj['entrant2Id'] is not None and set_obj['entrant1Score'] is not None and set_obj['entrant2Score'] is not None

def parse_set_page (r):
    global tournament_dict
    global player_dict
    url = r.url
    print(url)
    set_data = r.json()
    entities = set_data['entities']
    if 'sets' in entities:
        sets = entities['sets']
        for set_obj in sets:
            if valid_set(set_obj):
                try:
                    entrant1 = player_dict[set_obj['entrant1Id']].pid
                    entrant2 = player_dict[set_obj['entrant2Id']].pid
                    entrant1_score = set_obj['entrant1Score']
                    entrant2_score = set_obj['entrant2Score']
                    new_set = melee.TournamentSet(entrant1, entrant1_score, entrant2, entrant2_score)
                    print(new_set.to_string())
                    if(new_set not in tournament_dict[r.url].sets):
                        tournament_dict[r.url].sets.append(new_set)
                except:
                    print('Failed to load set, likely due to a missing player id')

        '''for set_obj in sets:
            if (set_obj['entrant1Id']) is not None:
                entrant1 = player_dict[set_obj['entrant1Id']]
            else:
                entrant1 = None

            if (set_obj['entrant2Id']) is not None:
                entrant2 = player_dict[set_obj['entrant2Id']]
            else:
                entrant2 = None

            if (set_obj['entrant1Score']) is not None:
                entrant1_score = set_obj['entrant1Score']
            else:
                entrant1_score = None

            if (set_obj['entrant2Score']) is not None:
                entrant2_score = set_obj['entrant2Score']
            else:
                entrant2_score = None
            new_set = melee.TournamentSet(entrant1, entrant1_score, entrant2, entrant2_score)
            print(new_set.to_string())
            tournament_dict[r.url()].sets.append(new_set)'''
