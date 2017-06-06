import os
import pymysql

def populate(db_name, tournaments, players, sets):
    conn = pymysql.connect(user='root', password='', database=db_name)
    conn.set_charset('utf8mb4')
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8mb4;')
    cursor.execute('SET CHARACTER SET utf8mb4;')
    create_tables(cursor)
    conn.commit()
    for player in players:
        print(player.to_string())
        cursor.execute(
            """INSERT INTO Player (player_id, tag, elo, prefix, state, country) VALUES ({0}, "{1}", {2}, "{3}", '{4}', '{5}')""".format(
                player.pid, player.tag, 0, player.prefix, player.state, player.country))
    for tournament in tournaments:
        print(tournament.to_string())
        cursor.execute(
            """INSERT INTO Tournament (tournament_id, tournament_name, tournament_date) VALUES ({0}, '{1}', FROM_UNIXTIME({2}, '%y-%m-%d'))""".format(
                tournament.tid, tournament.name, tournament.date))
    for tournament_set in sets:
        print(tournament_set.to_string())
        cursor.execute(
            """INSERT INTO TournamentSet (entrant_1_id, entrant_1_score, entrant_2_id, entrant_2_score, winner_id, loser_id, tournament_id, url) VALUES ( {0}, {1}, {2}, {3}, {4}, {5}, {6}, '{7}')""".format(
                tournament_set.entrant_1_id, tournament_set.entrant_1_score, tournament_set.entrant_2_id,
                tournament_set.entrant_2_score, tournament_set.winner, tournament_set.loser, tournament_set.tid,
                tournament_set.url))
    conn.commit()
    conn.close()


def create_tables(cursor):
    print('creating tables')
    cursor.execute('''
    DROP TABLE IF EXISTS TournamentSet;
    DROP TABLE IF EXISTS Player;
    DROP TABLE IF EXISTS Tournament;

    CREATE TABLE Tournament (
        tournament_id INTEGER PRIMARY KEY,
        tournament_name VARCHAR(200),
        tournament_date DATE
    );

    CREATE TABLE Player (
        player_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        tag VARCHAR(500),
        elo INTEGER,
        prefix VARCHAR(500),
        state VARCHAR(500),
        country VARCHAR(500)
    );

    CREATE TABLE TournamentSet (
        set_id INTEGER PRIMARY KEY AUTO_INCREMENT,
        entrant_1_id INTEGER,
        entrant_1_score INTEGER,
        entrant_2_id INTEGER,
        entrant_2_score INTEGER,
        winner_id INTEGER,
        loser_id INTEGER,
        tournament_id INTEGER,
        url VARCHAR(200),
        FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id),
        FOREIGN KEY (entrant_1_id) REFERENCES Player(player_id),
        FOREIGN KEY (entrant_2_id) REFERENCES Player(player_id)
    );
    ''')



