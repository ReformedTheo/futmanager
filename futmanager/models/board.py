from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
from futmanager.models.match import Match
from futmanager.models.team import Team
from futmanager.services.load_teams import LoadTeams

@dataclass
class StandingEntry:
    team:      Team
    played:    int = 0
    wins:      int = 0
    draws:     int = 0
    losses:    int = 0
    goals_for: int = 0
    goals_against: int = 0

    @property
    def goal_diff(self) -> int:
        return self.goals_for - self.goals_against

    @property
    def points(self) -> int:
        return self.wins * 3 + self.draws

@dataclass
class Board:
    team_ids:   List[int]
    matches:    List[Match]            = field(default_factory=list)
    created_at: datetime               = field(default_factory=datetime.now)
    board_id:   int = 0

    def compute_standings(self) -> List[StandingEntry]:
        # 1) carrega objetos Team
        teams: List[Team] = LoadTeams().load()
        # mapeia id → Team
        id2team: Dict[int, Team] = {t.id: t for t in teams if t.id in self.team_ids}

        # 2) inicializa tabela de classificação
        table: Dict[int, StandingEntry] = {
            team_id: StandingEntry(team=id2team[team_id])
            for team_id in self.team_ids
        }

        # 3) percorre cada partida e atualiza estatísticas
        for m in self.matches:
            home = table[m.home_id]
            away = table[m.away_id]

            home.played += 1
            away.played += 1

            # gols
            home.goals_for += m.home_goals
            home.goals_against += m.away_goals
            away.goals_for += m.away_goals
            away.goals_against += m.home_goals

            # resultado
            if m.home_goals > m.away_goals:
                home.wins  += 1
                away.losses += 1
            elif m.home_goals < m.away_goals:
                away.wins  += 1
                home.losses += 1
            else:
                # empate
                home.draws += 1
                away.draws += 1

        # 4) converte para lista e ordena por pontos, depois saldo de gols, depois gols pró
        standings = list(table.values())
        standings.sort(
            key=lambda e: (e.points, e.goal_diff, e.goals_for),
            reverse=True
        )
        return standings

    def print_table(self):
        """Exibe a tabela no console."""
        cols = f"{'Time':<20} {'J':>2} {'V':>2} {'E':>2} {'D':>2} {'GP':>3} {'GC':>3} {'SG':>3} {'P':>3}"
        print(cols)
        print("-" * len(cols))
        for e in self.compute_standings():
            print(f"{e.team.name:<20} "
                  f"{e.played:>2} "
                  f"{e.wins:>2} "
                  f"{e.draws:>2} "
                  f"{e.losses:>2} "
                  f"{e.goals_for:>3} "
                  f"{e.goals_against:>3} "
                  f"{e.goal_diff:>3} "
                  f"{e.points:>3}")
