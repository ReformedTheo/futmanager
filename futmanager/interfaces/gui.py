import pygame
import sys
from pygame import Surface
from typing import List, Tuple, Optional, Any
from datetime import datetime, timedelta
from itertools import permutations

from futmanager.services.load_teams     import LoadTeams
from futmanager.services.simulate_match import SimulateMatch
from futmanager.models.team             import Team
from futmanager.models.match            import Match
from futmanager.models.board            import Board

BUTTON_COLOR    = (50, 150, 50)
BUTTON_HOVER    = (70, 170, 70)
TEXT_COLOR      = (255,255,255)
BG_PANEL        = (30, 30, 30)

def _schedule_rounds(teams: List[Team]) -> List[List[Tuple[Team, Team]]]:
    # gera ida e volta via permutations (já dá ambos sentidos)
    pool = sorted([(h,a) for h,a in permutations(teams,2)], key=lambda ha:(ha[0].id,ha[1].id))
    rounds = []
    while pool:
        this_round, used = [], set()
        for h,a in pool:
            if h.id not in used and a.id not in used:
                this_round.append((h,a))
                used |= {h.id,a.id}
        for m in this_round:
            pool.remove(m)
        rounds.append(this_round)
    return rounds

def run_gui():
    pygame.init()
    screen = pygame.display.set_mode((1100, 600))
    pygame.display.set_caption("Campeonato")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # carrega times e imagens
    teams = LoadTeams().load()
    team_images = {
        t.id: pygame.transform.scale(
            pygame.image.load(t.img_path), (40,40)
        )
        for t in teams
    }

    # calendário e estado
    rounds = _schedule_rounds(teams)
    total_rounds = len(rounds)
    current_round = 0
    board = Board([t.id for t in teams], board_id=1)

    # time selecionado (começa no 1º da lista)
    selected_idx = 0

    # simulação do jogo do time selecionado
    sim = SimulateMatch()
    simulation: Optional[Any] = None    # generator
    events_log: List[str] = []
    last_tick = 0

    # botão “Jogar Rodada”
    btn_rect = pygame.Rect(900, 520, 180, 50)

    running = True
    while running:
        now = pygame.time.get_ticks()
        mx,my = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

            # clique no botão
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button==1:
                if btn_rect.collidepoint(mx,my) and simulation is None:
                    # dispara simulação da próxima rodada
                    if current_round < total_rounds:
                        # simula TODOS os jogos da rodada
                        for h,a in rounds[current_round]:
                            m = Match(
                                match_id = current_round,
                                home_id  = h.id,
                                away_id  = a.id,
                                match_day= datetime(2025,1,1)+timedelta(days=current_round)
                            )
                            sim.simulate(m)
                            board.matches.append(m)
                        # prepara generator só para o jogo do time escolhido
                        h,a = next(filter(
                            lambda pa: pa[0].id==teams[selected_idx].id or pa[1].id==teams[selected_idx].id,
                            rounds[current_round]
                        ))
                        selected_match = Match(
                            match_id = current_round,
                            home_id  = h.id,
                            away_id  = a.id,
                            match_day= datetime(2025,1,1)+timedelta(days=current_round)
                        )
                        sim.simulate(selected_match)
                        simulation = _stepper(selected_match)
                        events_log.clear()
                        last_tick = now
                        current_round += 1

            # ciclo de teclas: esquerda/direita para mudar seleção
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_LEFT:
                    selected_idx = (selected_idx-1) % len(teams)
                elif ev.key==pygame.K_RIGHT:
                    selected_idx = (selected_idx+1) % len(teams)

        # avança o generator a cada 1s
        if simulation and now-last_tick>1000:
            last_tick = now
            try:
                minute,txt = next(simulation)
                events_log.append(txt)
            except StopIteration:
                simulation = None

        # -- desenho --

        screen.fill((0,0,0))
        # 1) painel de seleção de time
        for i,t in enumerate(teams):
            x = 10 + i*120
            clr = (200,200,50) if i==selected_idx else (100,100,100)
            pygame.draw.rect(screen, clr, (x,10,110,30))
            screen.blit(font.render(t.name, True, (0,0,0)), (x+5,15))

        # 2) botão Jogar Rodada
        hov = BUTTON_HOVER if btn_rect.collidepoint(mx,my) else BUTTON_COLOR
        pygame.draw.rect(screen, hov, btn_rect)
        screen.blit(font.render("Jogar Rodada", True, TEXT_COLOR), (btn_rect.x+20, btn_rect.y+15))

        # 3) tabela de classificação
        lines = ["Time          J  V  E  D  GP  GC  SG  P"]
        for e in board.compute_standings():
            pre = "> " if e.team.id==teams[selected_idx].id else "  "
            lines.append(pre + f"{e.team.name[:12]:12s} {e.played:2d} {e.wins:2d} {e.draws:2d} {e.losses:2d}"
                                 + f" {e.goals_for:2d} {e.goals_against:2d} {e.goal_diff:3d} {e.points:3d}")
        # desenha
        for i,line in enumerate(lines):
            screen.blit(font.render(line, True, TEXT_COLOR), (820, 60 + i*20))

        # 4) área de eventos (se tiver)
        pygame.draw.rect(screen, BG_PANEL, (10, 400, 780, 180))
        for i,txt in enumerate(events_log[-8:]):
            screen.blit(font.render(txt, True, TEXT_COLOR), (15, 405 + i*20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

def _stepper(game: Match):
    for minute in range(90):
        line = f"{minute}'"
        for e in game.events:
            if minute == e.minute:
                assist = f" (assist: {e.assist.name})" if e.assist else ""
                line += f" – {e.team.name}: {e.player.name} [{e.type.value}]{assist}"
                break
        yield minute, line
