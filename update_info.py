import melee
import db_connector

duplicates = {'Swift~': 'Swiftbass', 'swift~': 'Swiftbass'}

def update():
    global duplicates
    connection = db_connector.connection()
    cursor = connection.cursor()

    for player in duplicates:
        print('Replacing all instances of player {0} with {1}'.format(player, duplicates[player]))
        cursor.execute('SELECT id FROM Players WHERE tag = %s', (player))
        if (len(cursor.fetchall()) > 0):
            old_id = cursor.fetchone()[0]
            cursor.execute('SELECT id FROM Players WHERE tag = %s', (duplicates[player]))
            new_id = cursor.fetchone()[0]
            print('old id = {0}'.format(old_id))
            print('new id = {0}'.format(new_id))
            cursor.execute('UPDATE Sets SET winner_id = %s WHERE winner_id = %s', (new_id, old_id))
            cursor.execute('UPDATE Sets SET loser_id = %s WHERE loser_id = %s', (new_id, old_id))
            cursor.execute('DELETE FROM Players WHERE id = %s', (old_id))
        else:
            print('no duplicates found for {0}'.format(player))

    print('Duplicates replaced successfully')
    connection.commit()
    connection.close()
