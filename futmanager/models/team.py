from .player import Player
from typing import List

class Team:
    def __init__(self, name: str, players: list[Player]):
        self.name =  name
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

    @property
    def team_overall(self) -> float:
        return sum(p.player_overall for p in self.players) / len(self.players)
    
    @property
    def attack_overall(self) -> float:
        sum = 0
        for p in self.attack_players:
            sum = p.player_overall + sum
        return sum/len(self.attack_players)
    @property
    def defense_overall(self) -> float:
        sum = 0
        for p in self.defense_players:
            sum = p.player_overall + sum
        return sum/len(self.defense_players)
    
    