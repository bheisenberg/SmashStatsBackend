import sqlite3

db = 'C:/users/Brian/Desktop/melee.sqlite'

def populate(tournaments, players):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    create_tables(cursor)
    for player in players:
        cursor.execute(''' INSERT OR IGNORE INTO Player (player_id, tag, elo, prefix, state, country)
                    VALUES ( ?, ?, ?, ?, ?, ? )''', (player.pid, player.tag, 0, player.prefix, player.state, player.country))
    for tournament in tournaments:
        cursor.execute(''' INSERT OR IGNORE INTO Tournament (tournament_id, tournament_name, tournament_date)
            VALUES (?, ?, datetime(?, 'unixepoch', 'localtime'))''',
                    (tournament.tid, tournament.name, tournament.date))
        for tournament_set in tournament.sets:
            cursor.execute(''' INSERT OR IGNORE INTO TournamentSet (entrant_1_id, entrant_1_score, entrant_2_id, entrant_2_score, winner_id, loser_id, tournament_id)
            VALUES ( ?, ?, ?, ?, ?, ?, ? )''', (
            tournament_set.entrant_1_id, tournament_set.entrant_1_score, tournament_set.entrant_2_id,
            tournament_set.entrant_2_score, tournament_set.winner, tournament_set.loser, tournament.tid))
    conn.commit()
    conn.close()


def create_tables(cursor):
    cursor.executescript('''
    DROP TABLE IF EXISTS Player;
    DROP TABLE IF EXISTS TournamentSet;
    DROP TABLE IF EXISTS Tournament;

    CREATE TABLE Player (
        player_id VARCHAR(20) NOT NULL PRIMARY KEY UNIQUE,
        tag VARCHAR(20),
        elo INTEGER,
        prefix VARCHAR(20),
        state VARCHAR(20),
        country VARCHAR(20)
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
    )
    ''')
