from __future__ import division
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

        if int(goals_scored) > int(goals_conceded):
            return "win"
        elif int(goals_scored) == int(goals_conceded):
            return "tie"
        else:
            return "loss"

    def get_record(self):
        """
        Get season results for a team

        :returns: { 'wins': wins, 'losses': losses, 'ties': ties }
        """
        wins = losses = ties = 0
        results = self.get_season_results()

        for r in results:
            result = r.get('result')
            if result == 'win':
                wins += 1
            elif result == 'loss':
                losses += 1
            else:
                ties += 1

        return {
            'wins': wins,
            'losses': losses,
            'ties': ties
        }

    def get_season_results(self):
        """
        Get all fixtures for a given team
        
        :returns: ( (date, opposition, opposition_id, venue, formation), ... )
        """

        sql = """SELECT DISTINCT date, team_id, team, opposition_id, opposition, venue, team_formation
                 FROM players WHERE team_id=%s ORDER BY DATE;"""

        matches = run_multirow_query(sql, self.team_id)
        matches_with_results = []
        for m in matches:
            m_with_result = {
                'date': m[0],
                'opposition_id': m[3],
                'opposition': m[4],
                'venue': m[5],
                'formation': m[6],
                'result': self.get_match_result(m[3], m[0])
            }
            
            matches_with_results.append(m_with_result)

        return matches_with_results

    def get_winning_pct(self):
        """
        Compute the winning percentage for a team

        :returns: decimal win percentage
        """

        results = self.get_season_results()
        games_played = len(results)
        total_wins = 0

        for r in results:
            if r.get('result') == 'win':
                total_wins += 1
                
        return total_wins / games_played

    def get_winning_pct_with_formation(self, formation_id):
        """
        Compute the winning percentage for a team given a certain formation
        
        :returns: decimal win percentage
        """

        results = self.get_season_results()
        games_played = len(results)
        total_wins = 0
        
        for r in results:
            if int(r.get('formation')) == int(formation_id) and r.get('result') == 'win':
                total_wins += 1

        return total_wins / games_played