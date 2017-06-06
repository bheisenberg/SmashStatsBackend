import json
import codecs
import urllib.parse
import urllib.request
import time
import sqlite3
import time
import Elo
import os

db = os.path.expanduser('~/documents/smashstats/db/melee.sqlite')
conn = sqlite3.connect(db)
cur = conn.cursor()

Tournaments = []
TournamentSets = []

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
    def __init__(self, tournament_id, tournament_name, tournament_date):
        self.tournament_id = tournament_id
        self.tournament_name = tournament_name
        self.tournament_date = tournament_date

def create_tables():
    cur.executescript('''
    DROP TABLE IF EXISTS Player;
    DROP TABLE IF EXISTS TournamentSet;
    DROP TABLE IF EXISTS Tournament;

    CREATE TABLE Player (
        player_id VARCHAR(20) NOT NULL PRIMARY KEY UNIQUE,
        tag VARCHAR(20),
        elo INTEGER,
        prefix VARCHAR(20),
        state VARCHAR(20),
        country VARCHAR(20),
        twitter_handle VARCHAR(20),
        twitch_stream VARCHAR(20)
    );

    CREATE TABLE TournamentSet (
        set_id INTEGER PRIMARY KEY AUTOINCREMENT,
        entrant_1_id VARCHAR(20),
        entrant_1_score VARCHAR(20),
        entrant_2_id VARCHAR(20),
        entrant_2_score VARCHAR(20),
        winner_id VARCHAR(20),
        loser_id VARCHAR(20),
        tournament_id INTEGER,
        FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id)
        FOREIGN KEY (entrant_1_id) REFERENCES Player(player_id)
        FOREIGN KEY (entrant_2_id) REFERENCES Player(player_id)
    );

    CREATE TABLE Tournament (
        tournament_id INTEGER PRIMARY KEY,
        tournament_name VARCHAR(20),
        tournament_date DATE
    )''')

def winner(x, y):
    if x > y:
        return x
    elif y > x:
        return y
    else:
        return None

def loser(x, y):
    if x < y:
        return x
    elif y < x:
        return y
    else:
        return None

def populate_players():
    print("Loading players...")
    with open('text/playerdict.txt', 'r', encoding='utf-8') as playerdict:
        for line in playerdict:
            split_line = line.split()
            if len(split_line) > 1:
                player_id = split_line[0]
                print(player_id)
                tag = split_line[1]
                prefix = split_line[2]
                #twitter_handle = split_line[3]
                #twitch_stream = split_line[4]
                state = split_line[3]
                country = split_line[4]
                cur.execute(''' INSERT INTO Player (player_id, tag, elo, prefix, state, country)
                VALUES ( ?, ?, ?, ?, ?, ? )''', (player_id, tag, 0, prefix, state, country))
    print("Insertion successful")
    conn.commit()

def populate_tournaments():
    print("Loading tournaments...")
    with open('text/tournaments.txt', 'r', encoding='utf-8') as tournaments:
        for line in tournaments:
            tournament_name = line.split()[1]
            tournament_date = line.split()[2]
            tournament_id = line.split()[3]
            tournament = Tournament(tournament_id, tournament_name, tournament_date)
            Tournaments.append(tournament)
            cur.execute(''' INSERT INTO Tournament (tournament_id, tournament_name, tournament_date)
                VALUES (?, ?, datetime(?, 'unixepoch', 'localtime'))''', (tournament.tournament_id, tournament.tournament_name, tournament.tournament_date))
    print("Insertion successful")
    conn.commit()

def populate_sets():
    print("Loading sets...")
    with open('text/sets.txt', 'r', encoding='utf-8') as sets:
        for line in sets:
            if len(line.split()) > 3:
                entrant_1_id = line.split()[0]
                entrant_1_score = line.split()[1]
                entrant_2_id = line.split()[2]
                entrant_2_score = line.split()[3]
                tournament_id = line.split()[4]
                tournament_set = TournamentSet(entrant_1_id, entrant_1_score, entrant_2_id, entrant_2_score, tournament_id)
                TournamentSets.append(tournament_set)
                cur.execute(''' INSERT INTO TournamentSet (entrant_1_id, entrant_1_score, entrant_2_id, entrant_2_score, winner_id, loser_id, tournament_id)
                VALUES ( ?, ?, ?, ?, ?, ?, ? )''', (tournament_set.entrant_1_id, tournament_set.entrant_1_score, tournament_set.entrant_2_id, tournament_set.entrant_2_score, tournament_set.winner, tournament_set.loser, tournament_set.tournament_id))
    conn.commit()

def update_player_elo():
    print('Updating players...')
    sets = cur.execute('''SELECT s.winner_id, s.loser_id, t.tournament_date FROM TournamentSet s, Tournament t WHERE s.tournament_id = t.tournament_id ''').fetchall()
    sets.sort(key=lambda x: x[2])
    eloCalculator = Elo.Elo(sets)
    players = eloCalculator.Calculate_Elo()
    for player_id in players.keys():
        #print(player_id)
        cur.execute('UPDATE Player SET elo = {0} WHERE player_id = {1}'.format(players[player_id].elo, player_id))
    conn.commit()

print("Insertion successful")
create_tables()
populate_players()
populate_tournaments()
populate_sets()
update_player_elo()


