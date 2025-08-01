
from .roster import Roster
import os
import unicodedata

class Team:
    def __init__(self, name: str, roster: Roster, id: int):
        self.name =  name
        self.roster = roster
        self.id = id
   
    @property
    def team_overall(self) -> float:
        return sum(p.player_overall for p in self.roster.players) / len(self.roster.players)
    
    @property
    def attack_overall(self) -> float:
        sum = 0
        for p in self.roster.attack_players:
            sum = p.player_overall + sum
        return sum/len(self.roster.attack_players)
    @property
    def defense_overall(self) -> float:
        sum = 0
        for p in self.roster.defense_players:
            sum = p.player_overall + sum
        return sum/len(self.roster.defense_players)
    
    @property
    def short_name(self) -> str:
        base = self.name.split()[0]
        # 2) normaliza e remove acentos
        no_accents = unicodedata.normalize("NFKD", base) \
                    .encode("ASCII", "ignore") \
                    .decode("ASCII")
        # 3) lowercase
        short_name = no_accents.lower()
        return short_name
    
    @property
    def img_path(self) -> str:
        filename = self.short_name
        return os.path.join("futmanager", "assets", f"{filename}.png")
    