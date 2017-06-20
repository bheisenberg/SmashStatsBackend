import pymysql

def update_player_elo():
    conn = pymysql.connect(user='root', password='', database='smashstats')
    cursor = conn.cursor()
    print('Calculating elo...')
    query = cursor.execute(
        '''SELECT s.winner_id, s.loser_id, t.tournament_date FROM Sets s, Tournaments t WHERE s.tournament_id = t.id ORDER BY t.tournament_date ASC''')
    sets = [item for item in cursor.fetchall()]
    print(len(sets))
    sets.sort(key=lambda x: x[2])
    elo = Elo(sets)
    players = elo.Calculate_Elo()
    for player_id in players.keys():
        #print(player_id)
        cursor.execute('UPDATE Players SET elo = {0} WHERE id = {1}'.format(players[player_id].elo, player_id))
    conn.commit()
    conn.close()
    print('Elo calculation complete.')


class Tournament:
    def __init__(self, tournament_id):
        self.tournament_id = tournament_id
        self.sets = None

class Player:
    def __init__(self):
        self.elo = 1000
        self.games = 0
        self.k = 40
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


    def Save_Record(self, record):
        player = 'Armada'
        with open('text/record.txt', 'w', encoding='utf-8') as record_file:
            for line in record:
                if(player in line):
                    print(line)
                    record_file.write(line)
                    record_file.write('\n')

    def Calculate_Elo(self):
        num=0
        players = {}
        record = []
        for set in self.sets:
            if (set[0] is not None and set[1] is not None) and (set[0] != 'None' and set[1] != 'None'):
                winner_id = set[0]
                loser_id = set[1]
                winner = Player() if not (winner_id in players) else players[winner_id]
                loser = Player() if not (loser_id in players) else players[loser_id]

                #dif = abs(winner.elo - loser.elo)
                ea = self.e_a(winner.elo, loser.elo)
                eb = 1-ea
                win_elo = int(winner.calculate_k() * eb)
                loss_elo = int(loser.calculate_k() * eb)
                #print(winner.k/c)
                winner.elo += win_elo
                loser.elo -= loss_elo
                winner.games += 1
                loser.games += 1
                players[winner_id] = winner
                players[loser_id] = loser
                #print(winner_id)
                #print(loser_id)
                #record.append('{0} gained {1} elo from {2}. Now has {3} after {4} games. K is now {5}'.format(winner_id, win_elo, loser_id, winner.elo, winner.games, winner.calculate_k()))
                #record.append('{0} lost {1} elo from {2}. Now has {3} after {4} games. K is now {5}'.format(loser_id, loss_elo, winner_id, loser.elo, loser.games, winner.calculate_k()))
                #print('{0} gained {1} elo from {2}. Now has {3} after {4} games. K is now {5}'.format(winner_id, win_elo, loser_id, winner.elo, winner.games, winner.calculate_k()))
                #print('{0} lost {1} elo from {2}. Now has {3} after {4} games. K is now {5}'.format(loser_id, loss_elo, winner_id, loser.elo, loser.games, winner.calculate_k()))
                #num += 1
        self.Save_Record(record)
        return players
