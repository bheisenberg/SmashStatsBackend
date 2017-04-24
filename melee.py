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
    def __init__(self, name, phase_groups_slug, entrants_slug, date, tid):
        self.tid = tid
        self.name = name
        self.date = date
        self.phase_groups_url = '{0}{1}'.format(gg.api, phase_groups_slug)
        self.entrants_url = '{0}{1}'.format(gg.api, entrants_slug)


