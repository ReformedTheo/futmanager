# futmanager/models/match.py
from __future__ import annotations #pra evitar imports circulares
from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING

from .team import Team

if TYPE_CHECKING:
    from .event import Event

@dataclass
class Match:
    home: Team
    away: Team
    home_goals: int = 0
    away_goals: int = 0
    #evita import circulares
    events: List["Event"] = field(default_factory=list)
