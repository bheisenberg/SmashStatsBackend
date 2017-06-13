#Created by Brian Eisenberg 4/25/2017

class TournamentSet:
    def __init__(self, entrant_1, entrant_2, tid, url):
        self.__entrant_1 = entrant_1
        self.__entrant_2 = entrant_2
        self.winner = self.get_winner()
        self.loser = self.get_loser()
        self.tid = tid
        self.url = url


    def get_winner(self):
        return self.__entrant_1 if (self.__entrant_1.score > self.__entrant_2.score) else self.__entrant_2

    def get_loser(self):
        return self.__entrant_1 if (self.__entrant_1.score < self.__entrant_2.score) else self.__entrant_2

    def get_loser_score(self):
        return

    def to_string(self):
        return '{0} {1} {2} {3} {4}'.format(self.winner.id, self.winner.score, self.loser.id, self.loser.score, self.tid)

class Entrant:
    def __init__(self, id, score):
        self.id = id
        self.score = score


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

    def to_string(self):
        return '{0} {1} {2}'.format(self.tid, self.name, self.date)

class Player:
    def __init__(self, pid, tag, prefix, state, country):
        self.pid = pid
        self.tag = tag
        self.prefix = prefix
        self.state = state
        self.country = country

    def to_string(self):
        return '{0} {1} {2} {3} {4}'.format(self.pid, self.tag, self.prefix, self.state, self.country)



