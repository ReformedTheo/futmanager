# futmanager/interfaces/cli.py

from futmanager.models.team import Team
from futmanager.models.player import Player
from futmanager.models.match import Match
from futmanager.services.simulate_match import SimulateMatch

def run():
    t1 = Team("Cruzeiro", cruzeiro_players)
    t2 = Team("Patético Mineiro", atletico_players)
    game = Match(t1, t2)
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
    Player("Everson", 85, "GOL"),
    Player("Natanael", 82, "ZAG"),
    Player("Lyanco", 30, "ZAG"),
    Player("Junior Alonso", 82, "ZAG"),
    Player("Caio Paulista", 80, "LAT"),
    Player("Gabriel Menino", 84, "VOL"),
    Player("Igor Gomes", 83, "MEI"),
    Player("Gustavo Scarpa", 84, "MEI"),
    Player("Dudu", 7, "ATA"),
    Player("Rony", 85, "ATA"),
    Player("Hulk", 24, "ATA")
]
