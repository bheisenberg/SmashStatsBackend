import load_players
import melee

test_phase = melee.Phase(9379, 100)
phases = [test_phase]
players = load_players.Player_Loader(phases).load_players()

for player in players.player_list:
    print(player.tag)