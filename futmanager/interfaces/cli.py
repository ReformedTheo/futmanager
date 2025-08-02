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
    game = Match(home.id, away.id, 1, 1)
    SimulateMatch().simulate(game)