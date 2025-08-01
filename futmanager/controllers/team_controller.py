from futmanager.models.team import Team
from futmanager.services.load_teams import LoadTeams


def get_team_by_id(id: int) -> Team:        
         teams = LoadTeams()
         teams_list = teams.load()
         for team in teams_list:
               if team.id == id:
                    return team
         raise ValueError(f"Time com id={id} não encontrado em")
