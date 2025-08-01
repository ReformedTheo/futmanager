import pygame
import sys
from pygame import Surface
from futmanager.services.load_teams import LoadTeams
from futmanager.models.team import Team
from futmanager.models.match import Match
from futmanager.models.roster import Roster
from futmanager.services.simulate_match import SimulateMatch

def run_gui():
    pygame.init()

    team_loader = LoadTeams()
    teams = team_loader.load()

    home_image: Surface
    away_image: Surface
    home_roster: Roster
    away_roster: Roster

    

    for team in teams:
        if team.id == 61:
            home_roster = team.roster
            home_image = pygame.image.load(team.img_path)
        elif team.id == 24:
            away_roster = team.roster
            away_image = pygame.image.load(team.img_path)

    # --- Dimensões ---
    FIELD_W, FIELD_H = 800, 600
    LOG_W = 300
    WIN_W = FIELD_W + LOG_W
    WIN_H = FIELD_H

    screen = pygame.display.set_mode((WIN_W, WIN_H))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Simulação de Jogo")

    # --- Carrega imagens ---
    campo_img     = pygame.image.load("futmanager/assets/campo.png")

    campo_img    = pygame.transform.scale(campo_img, (FIELD_W, FIELD_H))
    home_image = pygame.transform.scale(home_image, (40, 40))
    away_image  = pygame.transform.scale(away_image, (40, 40))



    # --- Posições simples em linha ---
    def linspace(y, n, width):
        step = width // (n + 1)
        return [(step*(i+1), y) for i in range(n)]

    pos_cru = linspace(FIELD_H - 80, len(home_roster.players), FIELD_W)
    pos_pat = linspace(80,        len(away_roster.players), FIELD_W)

    # --- Time e partida ---
    t1_roster = Roster(home_roster.players, 61)
    t2_roster = Roster(away_roster.players, 24)
    t1 = Team("Cruzeiro", t1_roster, 61)
    t2 = Team("Patético Mineiro", t2_roster, 24)
    game = Match(t1.id, t2.id)
    simulator = SimulateMatch()

    # --- Fonte para o painel de eventos ---
    font = pygame.font.SysFont(None, 24)
    events_log = []           # armazena strings de eventos
    simulation = None         # será nosso gerador de passos
    last_tick_ms = 0          # para cronometrar 1s entre minutos

    running = True
    while running:
        now = pygame.time.get_ticks()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                # inicia/ reinicia simulação como gerador
                simulator.simulate(game)   # gera gols e eventos
                simulation = _stepper(game) 

                events_log.clear()
                last_tick_ms = now

        # --- Atualiza simulação a cada 1 segundo ---
        if simulation and now - last_tick_ms >= 1000:
            last_tick_ms = now
            try:
                minute, text = next(simulation)
                
                events_log.append(text)
            except StopIteration:
                simulation = None  # acabou

        # --- Desenha fundo e jogadores ---
        screen.blit(campo_img, (0, 0))
        for idx, _ in enumerate(home_roster.players):
            screen.blit(home_image, pos_cru[idx])
        for idx, _ in enumerate(away_roster.players):
            screen.blit(away_image, pos_pat[idx])

        # --- Desenha painel de eventos à direita ---
        panel_rect = pygame.Rect(FIELD_W, 0, LOG_W, WIN_H)
        pygame.draw.rect(screen, (20, 20, 20), panel_rect)

        # exibe as últimas N linhas que cabem
        line_h = font.get_linesize()
        max_lines = WIN_H // line_h
        for i, line in enumerate(events_log[-max_lines:]):
            txt_surf = font.render(line, True, (255, 255, 255))
            screen.blit(txt_surf, (FIELD_W + 10, 10 + i * line_h))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

def _stepper(game: Match):
    """
    Transforma sua simulate() num gerador de (minuto, texto),
    sem pausas, para ser sacado a cada tick de tempo.
    """
    # já gerou game.events dentro de simulate()
    for minute in range(90):
        line = f"{minute}'"
        for e in game.events:
            if minute == e.minute:
                assist = f" (assist: {e.assist.name})" if e.assist else ""
                line += f" – {e.team.name}: {e.player.name} [{e.type.value}]{assist}"
                break
        yield minute, line
