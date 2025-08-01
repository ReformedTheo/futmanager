# futmanager/interfaces/cli.py

from futmanager.models.team import Team
from futmanager.models.player import Player
from futmanager.models.match import Match
from futmanager.models.roster import Roster
from futmanager.services.simulate_match import SimulateMatch
from futmanager.services.load_teams import LoadTeams
from random import sample
from typing import List

def run():
    team_load = LoadTeams()
    teams: List[Team] = team_load.load()
    home, away = sample(teams, 2)
    game = Match(home.id, away.id)
    SimulateMatch().simulate(game)



cruzeiro_players = [
    Player("Cássio", 88, "GOL"),
    Player("William", 86, "LAT"),
    Player("Fabrício Bruno", 87, "ZAG"),
    Player("Villalba", 85, "ZAG"),
    Player("Kaiki", 85, "LAT"),
    Player("Lucas Romero", 86, "VOL"),
    Player("Lucas Silva", 85, "VOL"),
    Player("Christian", 84, "MEI"),
    Player("Matheus Pereira", 92, "MEI"),
    Player("Wanderson", 84, "ATA"),
    Player("Kaio Jorge", 97, "ATA")
]

atletico_players = [
    Player("Everson", 24, "GOL"),
    Player("Natanael", 61, "ZAG"),
    Player("Lyanco", 24, "ZAG"),
    Player("Junior Alonso", 24, "ZAG"),
    Player("Caio Paulista", 61, "LAT"),
    Player("Gabriel Menino", 24, "VOL"),
    Player("Igor Gomes", 61, "MEI"),
    Player("Gustavo Scarpa", 24, "MEI"),
    Player("Dudu", 1, "ATA"),
    Player("Rony", 61, "ATA"),
    Player("Hulk", 24, "ATA")
]
