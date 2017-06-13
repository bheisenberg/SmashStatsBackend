import os
import pymysql
import melee

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
            """INSERT INTO Players (id, tag, elo, prefix, state, country) VALUES ({0}, "{1}", {2}, "{3}", '{4}', '{5}')""".format(
                player.pid, player.tag, 0, player.prefix, player.state, player.country))
    for tournament in tournaments:
        print(tournament.to_string())
        cursor.execute(
            """INSERT INTO Tournaments (id, tournament_name, tournament_date) VALUES ({0}, '{1}', FROM_UNIXTIME({2}, '%y-%m-%d'))""".format(
                tournament.tid, tournament.name, tournament.date))
    for tournament_set in sets:
        print(tournament_set.to_string())
        cursor.execute(
            """INSERT INTO Sets (winner_id, winner_score, loser_id, loser_score, tournament_id, url) VALUES ( {0}, {1}, {2}, {3}, {4}, '{5}' )""".format(
                tournament_set.winner.id, tournament_set.winner.score, tournament_set.loser.id, tournament_set.loser.score, tournament_set.tid,
                tournament_set.url))
    conn.commit()
    conn.close()


def create_tables(cursor):
    print('creating tables')
    cursor.execute('''
    DROP TABLE IF EXISTS Sets;
    DROP TABLE IF EXISTS Players;
    DROP TABLE IF EXISTS Tournaments;

    CREATE TABLE Tournaments (
        id INTEGER PRIMARY KEY,
        tournament_name VARCHAR(200),
        tournament_date DATE
    );

    CREATE TABLE Players (
        id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        tag VARCHAR(500),
        elo INTEGER,
        prefix VARCHAR(500),
        state VARCHAR(500),
        country VARCHAR(500)
    );

    CREATE TABLE Sets (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        winner_id INTEGER,
        winner_score INTEGER,
        loser_id INTEGER,
        loser_score INTEGER,
        tournament_id INTEGER,
        url VARCHAR(200),
        FOREIGN KEY (tournament_id) REFERENCES Tournaments(id),
        FOREIGN KEY (winner_id) REFERENCES Players(id),
        FOREIGN KEY (loser_id) REFERENCES Players(id)
    );
    ''')



