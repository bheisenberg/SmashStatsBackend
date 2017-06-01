import pymysql
import melee

conn = pymysql.connect(user='root', password='', database='test')
cursor = conn.cursor()

cursor.execute('INSERT INTO TEST_TABLE VALUES(0)')
query = cursor.execute('SELECT * FROM TEST_TABLE')
data = cursor.fetchall()
cursor.execute('''
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
    url VARCHAR(200),
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

player = melee.Player(9999, 'Shameless', 'WASD', 'NJ', 'United States')
tournament = melee.Tournament(9999, 'Alcoholocaust', '1496340191', 'http://api.smash.gg/tournament/Alcoholocaust')
tournament_set = melee.TournamentSet()


cursor.execute(''' INSERT INTO Player (player_id, tag, elo, prefix, state, country)
                VALUES ( ?, ?, ?, ?, ?, ? )''',
                   (player.pid, player.tag, 0, player.prefix, player.state, player.country))

cursor.execute(''' INSERT INTO Tournament (tournament_id, tournament_name, tournament_date)
        VALUES (?, ?, FROM_UNIXTIME(?, '%y-%m-%d'))''',
                   (tournament.tid, tournament.name, tournament.date))

cursor.execute(''' INSERT INTO TournamentSet (entrant_1_id, entrant_1_score, entrant_2_id, entrant_2_score, winner_id, loser_id, tournament_id, url)
    VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)''', (
        tournament_set.entrant_1_id, tournament_set.entrant_1_score, tournament_set.entrant_2_id,
        tournament_set.entrant_2_score, tournament_set.winner, tournament_set.loser, tournament_set.tid,
        tournament_set.url))
conn.commit()
conn.close()


cursor.execute('''INSERT INTO Tournament VALUES(0, '0', FROM_UNIXTIME(1496330292, '%y-%m-%d'))''')
print(data)