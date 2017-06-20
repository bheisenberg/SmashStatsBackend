import os
import pymysql
import db_connector
import melee

def populate(tournaments, players, sets):
    conn = db_connector.connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT id FROM Players''')
    pids = cursor.fetchall()
    for player in players:
        print(player.to_string())
        if(player.pid not in pids):
            cursor.execute(
                """INSERT INTO Players (id, tag, elo, prefix, state, country) VALUES ({0}, "{1}", {2}, "{3}", '{4}', '{5}')""".format(
                    player.pid, player.tag, 0, player.prefix, player.state, player.country))
        else:
            cursor.execute(
                """UPDATE Players SET tag = %s, prefix = %s, state = %s, country = %s WHERE id = %s""", (player.tag, player.prefix, player.state, player.country, player.pid))
    for tournament in tournaments:
        print(tournament.to_string())
        cursor.execute(
            """INSERT INTO Tournaments (id, tournament_name, tournament_date) VALUES ({0}, '{1}', FROM_UNIXTIME({2}, '%y-%m-%d'))""".format(
                tournament.tid, tournament.name, tournament.date))
    for tournament_set in sets:
        print(tournament_set.to_string())
        cursor.execute(
            """INSERT INTO Sets (winner_id, winner_score, loser_id, loser_score, round_division, round, tournament_id, url) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s )""", (
                tournament_set.winner.id, tournament_set.winner.score, tournament_set.loser.id, tournament_set.loser.score, tournament_set.round_division, tournament_set.round_text, tournament_set.tid,
                tournament_set.url))
    '''for placement in placements:
        print(placement.to_string())
        cursor.execute("""INSERT INTO Placements (player_id, placement, tournament_id) VALUES (%s, %s, %s)""", (placement.pid, placement.place, placement.tid))'''
    conn.commit()
    conn.close()



