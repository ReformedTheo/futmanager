from itertools import permutations
from datetime import datetime, timedelta
from typing import List, Tuple

from futmanager.models.board            import Board
from futmanager.models.match            import Match
from futmanager.models.team             import Team
from futmanager.services.load_teams     import LoadTeams
from futmanager.services.simulate_match import SimulateMatch

def _schedule_rounds(teams: List[Team]) -> List[List[Tuple[Team, Team]]]:
    # 1) gera e ordena todos os jogos de ida e volta de uma vez
    pool = sorted(
        [(h, a) for h, a in permutations(teams, 2)],
        key=lambda ha: (ha[0].id, ha[1].id)
    )

    rounds: List[List[Tuple[Team, Team]]] = []

    # 2) enquanto houver jogos, monta cada rodada garantindo
    #    que nenhum time joga duas vezes na mesma rodada
    while pool:
        this_round: List[Tuple[Team, Team]] = []
        used_ids = set()

        for h, a in pool:
            if h.id not in used_ids and a.id not in used_ids:
                this_round.append((h, a))
                used_ids.add(h.id)
                used_ids.add(a.id)

        # 3) remove esses jogos do pool
        for match in this_round:
            pool.remove(match)

        rounds.append(this_round)

    return rounds


def run_camp() -> List[Match]:
    teams: List[Team] = LoadTeams().load()
    sim     = SimulateMatch()
    board   = Board(team_ids=[t.id for t in teams], board_id=2)

    rounds  = _schedule_rounds(teams)
    start_dt = datetime(2025, 1, 1)
    match_id = 1
    all_games: List[Match] = []

    for rd, matchups in enumerate(rounds, start=1):
        match_day = start_dt + timedelta(days=rd - 1)
        print(f"{rd}ª RODADA ({match_day.date()})")

        for home, away in matchups:
            game = Match(
                match_id = match_id,
                home_id  = home.id,
                away_id  = away.id,
                match_day= match_day
            )
            sim.simulate(game)
            board.matches.append(game)
            all_games.append(game)
            match_id += 1

        board.print_table()
        print()

    return all_games
