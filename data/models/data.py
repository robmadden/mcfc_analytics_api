from db_helpers import run_multirow_query, run_singlerow_query

class Data():
    """
    A class to wrap the Players model.
    """

    def get_teams(self):
        """
        Fetch all the teams and their corresponding IDs

        :rtype: a list of tuples
        :returns: [ (team_id, team_name), (team_id, team_name), ... ]
        """

        sql = "SELECT DISTINCT team_id, team FROM players ORDER BY team;"
        return run_multirow_query(sql)

    def get_players(self):
        """
        Fetch all the players in the league and their corresponding IDs

        :rtype: a list of tuples
        :returns: [ (player_id, player, team) ]
        """
        sql = """SELECT distinct player_id, player_surname, player_forename, team_id, team
                 FROM players
                 ORDER BY team_id, player_surname;"""

        return run_multirow_query(sql)