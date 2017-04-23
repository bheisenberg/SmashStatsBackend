import sqlite3

class Tournament:
    def __init__(self, tournament_id):
        self.tournament_id = tournament_id
        self.sets = None

class Player:
    def __init__(self):
        self.elo = 1000
        self.games = 0
        self.k = 40

class Elo:
    def __init__(self, sets):
        self.elo = 1000
        self.games = 0
        self.k = 40
        self.sets = sets
        self.player_dict = {}
        self.tournaments = {}


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


    def Get_Elo(self):
        num=0
        players = self.Player_Dict()
        for set in self.sets:
            #print(set[1])
            if (set[0] is not None and set[1] is not None) and (set[0] != 'None' and set[1] != 'None'):
                winner_id = set[0]
                loser_id = set[1]
                winner = Player() if not (winner_id in players) else players[winner_id]
                loser = Player() if not (loser_id in players) else players[loser_id]

                #dif = abs(winner.elo - loser.elo)
                ea = self.e_a(winner.elo, loser.elo)
                eb = 1-ea
                win_elo = winner.k * eb
                loss_elo = loser.k * eb
                #print(winner.k/c)
                winner.elo += win_elo
                loser.elo -= loss_elo
                winner.games += 1
                loser.games += 1
                players[winner_id] = winner
                players[loser_id] = loser
                #print(winner_id)
                #print(loser_id)
                print('{0} gained {1} elo. Now has {2} after {3} games'.format(self.player_dict[winner_id], win_elo, winner.elo, winner.games))
                print('{0} lost {1} elo. Now has {2} after {3} games'.format(self.player_dict[loser_id], loss_elo, loser.elo, loser.games))
                num += 1
        return players



