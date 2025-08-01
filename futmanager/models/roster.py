from .player import Player
from typing import List

class Roster:
     def __init__(self, players: List[Player], team_id: int):
         self.team_id = team_id
         self.players = players
        
     @property
     def attack_players(self) -> List[Player]:
        attack_players = []
        for player in self.players:
            if player.position in {"ATA", "MEI", "LAT"}:
                attack_players.append(player)
        return attack_players
    
     @property
     def defense_players(self) -> List[Player]:
        defense_players = []
        for player in self.players:
            if player.position in {"ZAG", "GOL", "VOL", "LAT"}:
                defense_players.append(player)
        return defense_players
    
     @property
     def goalkeeper(self) -> Player:
        for player in self.players:
            if player.position in {"GOL"}:
                goalkeeper = player
        return goalkeeper