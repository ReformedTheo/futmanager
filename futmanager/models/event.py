
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
from futmanager.controllers.team_controller import get_team_by_id

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
        
        home_team = get_team_by_id(game.home_id)
        away_team = get_team_by_id(game.away_id)
        
        events: List[Event] = []
        idx = 0
        teams = [home_team, away_team]

        # gols do time da casa
        for _ in range(game.home_goals):
            m = goal_minutes[idx]; idx += 1
            scorer = random.choice(home_team.roster.attack_players)
            assist = random.choice([p for p in home_team.roster.players if p != scorer] + [None])
            events.append(cls(m, EventType.GOAL, scorer, home_team, assist))

        for _ in range(1,91):
            if _ not in goal_minutes and random.randint(1,10) % 2 != 0:
                m = _
                other_events = [EventType.DEFENSE, EventType.FOUL, EventType.YELLOW_CARD]
                event_type = random.choice(other_events)
                team = random.choice(teams)

                if event_type == EventType.DEFENSE:
                    player = team.roster.goalkeeper
                else: player = random.choice(team.roster.players)
                events.append(cls(_, event_type, player, team))
                

        # gols do visitante
        for _ in range(game.away_goals):
            m = goal_minutes[idx]; idx += 1
            scorer = random.choice(away_team.roster.attack_players)
            assist = random.choice([p for p in away_team.roster.players if p != scorer] + [None])
            events.append(cls(m, EventType.GOAL, scorer, away_team, assist))

        # ordena por minuto
        events.sort(key=lambda e: e.minute)
        return events
