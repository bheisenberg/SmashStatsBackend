#Created by Brian Eisenberg 4/25/2017

class TournamentSet:
    def __init__(self, entrant_1_id, entrant_1_score, entrant_2_id, entrant_2_score, tid):
        self.entrant_1_id = entrant_1_id
        self.entrant_1_score = entrant_1_score
        self.entrant_2_id = entrant_2_id
        self.entrant_2_score = entrant_2_score
        self.winner = self.get_winner()
        self.loser = self.get_loser()
        self.tid = tid


    def get_winner(self):
        return self.entrant_1_id if (self.entrant_1_score > self.entrant_2_score) else self.entrant_2_id

    def get_loser(self):
        return self.entrant_1_id if (self.entrant_1_score < self.entrant_2_score) else self.entrant_2_id

    def to_string(self):
        return '{0} {1} {2} {3}'.format(self.entrant_1_id, self.entrant_1_score, self.entrant_2_id, self.entrant_2_score)


class Phase:
    def __init__(self, phase_id, tid):
        self.phase_id = phase_id
        self.tid = tid

class Tournament:
    def __init__(self, tid, name, date, phase_url):
        self.tid = tid
        self.name = name
        self.date = date
        self.phase_url = phase_url

class Player:
    def __init__(self, pid, tag, prefix, state, country):
        self.pid = pid
        self.tag = tag
        self.prefix = prefix
        self.state = state
        self.country = country

    def to_string(self):
        return '{0} {1} {2} {3} {4}'.format(self.pid, self.tag, self.prefix, self.state, self.country)



