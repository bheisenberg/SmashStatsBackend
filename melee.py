import gg

class TournamentSet:
    def __init__(self, entrant_1_id, entrant_1_score, entrant_2_id, entrant_2_score, tournament_id):
        self.entrant_1_id = entrant_1_id
        self.entrant_1_score = entrant_1_score
        self.entrant_2_id = entrant_2_id
        self.entrant_2_score = entrant_2_score
        self.winner = self.get_winner()
        self.loser = self.get_loser()
        self.tournament_id = tournament_id

    def get_winner(self):
        if self.entrant_1_score > self.entrant_2_score:
            return self.entrant_1_id
        elif self.entrant_2_score > self.entrant_1_score:
            return self.entrant_2_id
        else:
            return None

    def get_loser(self):
        if self.entrant_1_score < self.entrant_2_score:
            return self.entrant_1_id
        elif self.entrant_2_score < self.entrant_1_score:
            return self.entrant_2_id
        else:
            return None


class Tournament:
    def __init__(self, tid, name, date, phase_groups_url, entrants_url):
        self.tid = tid
        self.name = name
        self.date = date
        self.phase_groups_url = phase_groups_url
        self.entrants_url = entrants_url
        self.phase_groups = []
        self.entrants = []

class Player:
    def __init__(self, pid, tag, prefix, state, country):
        self.pid = pid
        self.tag = tag
        self.prefix = prefix
        self.state = state
        self.country = country

    def to_string(self):
        return '{0} {1} {2} {3} {4}'.format(self.pid, self.tag, self.prefix, self.state, self.country)



