class Player:
    def __init__(self, name:str, player_overall: int, position: str):
        self.name = name
        self.player_overall = player_overall
        self.position = position

    def __repr__(self):
        return f"<Player {self.name} ({self.position})>"