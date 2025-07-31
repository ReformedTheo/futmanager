
import random
from futmanager.models.match import Match
from futmanager.models.event import Event
import time

class SimulateMatch:
    def __init__(self, variance: float = 0.35):
        self.variance = variance

    def simulate(self, game: Match) -> Match:
        def goals_expected(attack_overall, defense_overall):
            diff = attack_overall - defense_overall
            base = max(0.8, 1 + diff / 25)
            
            return max(0, random.gauss(base, self.variance))

        game.home_goals = round(goals_expected(game.home.attack_overall, game.away.defense_overall))
        game.away_goals = round(goals_expected(game.away.attack_overall, game.home.defense_overall))

        # Gera a lista de eventos (goals, etc)
        game.events = Event.generate_events(game)


        game_minute = 0
        for game_minute in range(90):
            line = f"{game_minute}'"

            for e in game.events:
                if game_minute == e.minute:
                    assist_txt = f" (assist: {e.assist.name})" if e.assist else ""
                    line += f" – {e.team.name}: {e.player.name} [{e.type.value}]{assist_txt}"
                    break

            print(line)
            time.sleep(1)
        print(f"FIM DE JOGO! \n{game.home.name} {game.home_goals} X {game.away_goals} {game.away.name}")
        return game
