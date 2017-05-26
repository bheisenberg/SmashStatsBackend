import sqlite3
import os
import pyodbc

db = os.path.expanduser("~/Desktop/melee.sqlite")

def populate(tournaments, players, sets):
    #conn = sqlite3.connect(db)
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 13 for SQL Server};'
        r'SERVER=WHITEKNIGHT;'
        r'DATABASE=meleedb;'
        r'Trusted_Connection=yes'
    )
    cursor = conn.cursor()
    create_tables(cursor)
    for player in players:
        cursor.execute(''' INSERT INTO Player (player_id, tag, elo, prefix, state, country)
                    VALUES ( ?, ?, ?, ?, ?, ? )''', (player.pid, player.tag, 0, player.prefix, player.state, player.country))
    for tournament in tournaments.values():
        cursor.execute(''' INSERT INTO Tournament (tournament_id, tournament_name, tournament_date)
            VALUES (?, ?, dateadd(?, [unixtime], '1970-01-01'))''',
                    (tournament.tid, tournament.name, tournament.date))
    for tournament_set in sets:
        cursor.execute(''' INSERT INTO TournamentSet (entrant_1_id, entrant_1_score, entrant_2_id, entrant_2_score, winner_id, loser_id, tournament_id, url)
        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)''', (
        tournament_set.entrant_1_id, tournament_set.entrant_1_score, tournament_set.entrant_2_id,
        tournament_set.entrant_2_score, tournament_set.winner, tournament_set.loser, tournament_set.tid, tournament_set.url))
    conn.commit()
    conn.close()


def create_tables(cursor):
    cursor.execute('''
    DROP TABLE IF EXISTS Player;
    DROP TABLE IF EXISTS TournamentSet;
    DROP TABLE IF EXISTS Tournament;

    CREATE TABLE Player (
        player_id VARCHAR(100) NOT NULL PRIMARY KEY,
        tag VARCHAR(100),
        elo INT,
        prefix VARCHAR(100),
        state VARCHAR(100),
        country VARCHAR(100)
    );

    CREATE TABLE Tournament (
        tournament_id INTEGER PRIMARY KEY,
        tournament_name VARCHAR(20),
        tournament_date DATE
    );

    CREATE TABLE TournamentSet (
        set_id INTEGER IDENTITY(1,1) PRIMARY KEY,
        entrant_1_id VARCHAR(20) FOREIGN KEY REFERENCES Player(player_id),
        entrant_1_score VARCHAR(20),
        entrant_2_id VARCHAR(20) FOREIGN KEY REFERENCES Player(player_id),
        entrant_2_score VARCHAR(20),
        winner_id VARCHAR(20),
        loser_id VARCHAR(20),
        tournament_id INTEGER FOREIGN KEY REFERENCES Tournament(tournament_id),
        url VARCHAR(200),
    )


    ''')
