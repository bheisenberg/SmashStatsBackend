import pymysql
import melee
import populate_db

db = 'test'

wrecken = melee.Player(132087, 'WreckenFro', '''Wrecken's''', '', 'United_States')
shameless = melee.Player(69, 'Shameless🌊', '/Ô\\\\', 'NJ', 'United_States')
tygo = melee.Player(42, r'Tygo🔥 \"The Kid\"', 'WASD', 'NJ', 'United_States')
shameless_entrant = melee.Entrant(69, 3)
tygo_entrant = melee.Entrant(42, 2)
test_tournament = melee.Tournament(1234, 'Alcoholocaust', '1496340191', 'http://api.smash.gg/tournament/Alcoholocaust')
test_tournament_set = melee.TournamentSet(shameless_entrant, tygo_entrant, 1234, 'http://api.smash.gg/tournament/Alcoholocaust')

players = [shameless, tygo, wrecken]
tournaments = [test_tournament]
sets = [test_tournament_set]

populate_db.populate(db, tournaments, players, sets)