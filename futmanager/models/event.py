
# futmanager/models/event.py
from __future__ import annotations
import random
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, TYPE_CHECKING

from .player import Player
from .team import Team

if TYPE_CHECKING:
    from .match import Match

class EventType(Enum):
    GOAL = "Goal"
    YELLOW_CARD = "Yellow Card"
    RED_CARD = "Red Card"
    SUBSTITUTION = "Substitution"
    FOUL = "Foul"
    DEFENSE = "Great defense"

@dataclass
class Event:
    minute: int
    type: EventType
    player: Player
    team: Team
    assist: Optional[Player] = None

    @classmethod
    def generate_events(cls, game: Match) -> List[Event]:
        total_goals = game.home_goals + game.away_goals
        # sorteia N minutos únicos de 1 a 90
        goal_minutes = random.sample(range(1, 91), total_goals)
        

        events: List[Event] = []
        idx = 0
        teams = [game.home, game.away]

        # gols do time da casa
        for _ in range(game.home_goals):
            m = goal_minutes[idx]; idx += 1
            scorer = random.choice(game.home.attack_players)
            assist = random.choice([p for p in game.home.players if p != scorer] + [None])
            events.append(cls(m, EventType.GOAL, scorer, game.home, assist))

        for _ in range(1,91):
            if _ not in goal_minutes and random.randint(1,10) % 2 != 0:
                m = _
                other_events = [EventType.DEFENSE, EventType.FOUL, EventType.YELLOW_CARD]
                event_type = random.choice(other_events)
                team = random.choice(teams)

                if event_type == EventType.DEFENSE:
                    player = team.goalkeeper
                else: player = random.choice(team.players)
                events.append(cls(_, event_type, player, team))
                

        # gols do visitante
        for _ in range(game.away_goals):
            m = goal_minutes[idx]; idx += 1
            scorer = random.choice(game.away.attack_players)
            assist = random.choice([p for p in game.away.players if p != scorer] + [None])
            events.append(cls(m, EventType.GOAL, scorer, game.away, assist))

        # ordena por minuto
        events.sort(key=lambda e: e.minute)
        return events
