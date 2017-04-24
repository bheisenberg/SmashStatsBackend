import sqlite3

class Tournament:
    def __init__(self, tournament_id):
        self.tournament_id = tournament_id
        self.sets = None

class Player:
    def __init__(self):
        self.elo = 1000
        self.games = 0
        self.k = self.calculate_k()
        self.master = False

    def calculate_k(self):
        if self.games < 30:
            return 40
        elif self.games >= 30 and self.elo < 2400:
            return 20
        elif self.elo >= 2400 or self.master:
            self.master = True
            return 10

class Elo:
    def __init__(self, sets):
        self.sets = sets
        print('starting elo')

    def e_a (self, win_elo, loss_elo):
        return 1 / (1 + pow (10, (loss_elo - win_elo) / 400))

    def Player_Dict(self):
        player_dict = {}
        with open("playerdict.txt", 'r', encoding='utf-8') as text:
            for line in text:
                splitline = str.split(line)
                pid = splitline[0]
                name = splitline[1]
                player_dict[pid] = name
                print("{0} {1}".format(pid, name))
        return player_dict


    def Calculate_Elo(self):
        print('Calculating elo...')
        num=0
        player_dict = self.Player_Dict()
        players = {}
        for set in self.sets:
            if (set[0] is not None and set[1] is not None) and (set[0] != 'None' and set[1] != 'None'):
                winner_id = set[0]
                loser_id = set[1]
                winner = Player() if not (winner_id in players) else players[winner_id]
                loser = Player() if not (loser_id in players) else players[loser_id]

                #dif = abs(winner.elo - loser.elo)
                ea = self.e_a(winner.elo, loser.elo)
                eb = 1-ea
                win_elo = winner.calculate_k() * eb
                loss_elo = loser.calculate_k() * eb
                #print(winner.k/c)
                winner.elo += win_elo
                loser.elo -= loss_elo
                winner.games += 1
                loser.games += 1
                players[winner_id] = winner
                players[loser_id] = loser
                #print(winner_id)
                #print(loser_id)
                if(winner_id == '13740' or loser_id == '13740'):
                    print('{0} gained {1} elo. Now has {2} after {3} games. K is now {4}'.format(player_dict[winner_id], win_elo, winner.elo, winner.games, winner.calculate_k()))
                    print('{0} lost {1} elo. Now has {2} after {3} games. K is now {4}'.format(player_dict[loser_id], loss_elo, loser.elo, loser.games, winner.calculate_k()))
                num += 1
        return players



