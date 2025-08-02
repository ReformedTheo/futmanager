# futmanager/models/match.py
from __future__ import annotations #pra evitar imports circulares
from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING
from datetime import datetime



if TYPE_CHECKING:
    from .event import Event

@dataclass
class Match():
    match_id: int
    home_id: int
    away_id: int
    board_id: int = 0
    home_goals: int = 0
    away_goals: int = 0
    match_day: datetime = field(default_factory=datetime.now)
    events: List["Event"] = field(default_factory=list)
    winner: int = 0
    

    def __post_init__(self):
        if self.home_id == self.away_id:
            raise ValueError("home_id e away_id não podem ser iguais")
