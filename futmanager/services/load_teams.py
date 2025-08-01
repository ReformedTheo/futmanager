from futmanager.models.team import Team
from futmanager.models.player import Player
from futmanager.models.roster import Roster
from typing import List
import json
import os


json_dir = "futmanager/store/teams"
class LoadTeams:    
    def load(self) -> List[Team]:
        teams: List[Team] = []
        for filename in os.listdir(json_dir):
                if not filename.lower().endswith(".json"):
                    continue
                path = os.path.join(json_dir, filename)
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)

                # Constrói objetos Player
                players = [
                    Player(p["name"], p["player_overall"], p["position"])
                    for p in data.get("players", [])
                ]

                roster = Roster(players, data["id"])
                team = Team(data["name"], roster, data["id"])
                teams.append(team)    
        return teams
    
    