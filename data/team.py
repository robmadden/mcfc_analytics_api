from db_helpers import run_multirow_query, run_singlerow_query

class Team():
    def __init__(self, team_id):
        self.team_id = team_id
        
    def get_players_on_team(self):
        """
        Get all players on a team given a team ID

        :returns: [ (player_id, player_surname, player_forname), ... ]
        """
        sql = """SELECT player_id, player_surname, player_forename, team
                 FROM players WHERE team_id=%s GROUP BY player_id, team_id;"""

        return run_multirow_query(sql, self.team_id)

    def get_match_result(self, opposition_id, date):
        sql = """SELECT SUM(goals) as goals_scored, SUM(goals_conceded) as goals_conceded
                 FROM players WHERE team_id=%s AND opposition_id=%s AND date=%s GROUP BY date;"""

        (goals_scored, goals_conceded) = run_singlerow_query(sql, (self.team_id, opposition_id, date))

        if goals_scored > goals_conceded:
            return "win"
        elif goals_scored == goals_conceded:
            return "tie"
        else:
            return "loss"

    def get_season_results(self):
        """
        Get all fixtures for a given team
        
        :returns: ( (date, team, team_id, opposition, opposition_id, venue, formation), ... )
        """

        sql = """SELECT DISTINCT date, team_id, team, opposition_id, opposition, venue, team_formation
                 FROM players WHERE team_id=%s ORDER BY DATE;"""

        results = run_multirow_query(sql, self.team_id)
        results_with_results = []
        for r in results:
            r_with_result = {
                'date': r[0],
                'team_id': r[1],
                'team': r[2],
                'opposition_id': r[3],
                'opposition': r[4],
                'venue': r[5],
                'formation': r[6],
                'result': self.get_match_result(r[3], r[0])
            }
            
            results_with_results.append(r_with_result)

        return results_with_results