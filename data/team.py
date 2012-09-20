from db_helpers import run_multirow_query

class Team():
    def __init__(self, team_id):
        self.team_id = team_id
        
    def get_players_on_team(self):
        """
        Get all players on a team given a team ID

        :param team_id: A numeric team id.
        :type team_id: int

        :returns: [ (player_id, player_surname, player_forname), ... ]
        """
        sql = """SELECT player_id, player_surname, player_forename, team
                 FROM players WHERE team_id=%s GROUP BY player_id, team_id;"""

        return run_multirow_query(sql, self.team_id)

    def get_team_fixtures(self, team_id):
        """
        Get all fixtures for a given team

        :param team_id: A numeric team id.
        :type team_id: int

        :returns: ( (date, team, team_id, opposition, opposition_id, venue), ... )
        """

        sql = """SELECT date, team_id, team, opposition_id, opposition, venue
                 FROM players WHERE team_id=%s GROUP BY team_id, opposition_id;"""

        return run_multirow_query(sql, self.team_id)