import melee_data
import load_tournaments

container = melee_data.TableContainer()
tournament_loader = load_tournaments.TournamentLoader(container)
tournament_loader.load_tournaments()


