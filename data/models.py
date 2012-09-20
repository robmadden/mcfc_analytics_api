from django.db import models, connection

class Data(models.Model):
    _db = 'mcfc_analytics'

    id = models.AutoField(primary_key=True)
    player_surname = models.CharField(max_length=30, null=True, blank=True)
    player_forename = models.CharField(max_length=30, null=True, blank=True)
    team = models.CharField(max_length=50, null=True, blank=True)
    player_id = models.IntegerField(max_length=11)

    def _run_query(self, query, params=None):
        """
        Run a generic query and return the results
        """
        cursor = connection.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_teams(self):
        """
        Fetch all the teams and their corresponding IDs

        :rtype: a list of tuples
        :returns: [ (team_id, team_name), (team_id, team_name), ... ]
        """

        sql = "select distinct team_id, team from players order by team;"
        return self._run_query(sql)

    def get_players(self):
        """
        Fetch all the players in the league and their corresponding IDs

        :rtype: a list of tuples
        :returns: [ (player_id, player, team) ]
        """
        sql = "select distinct player_id, player_surname, player_forename, team_id, team from players order by team_id, player_surname;"
        return self._run_query(sql)

    def get_players_on_team(self, team_id):
        """
        Get all players on a team given a team ID

        :returns: [ (player_id, player_surname, player_forname), ... ]
        """
        sql = 'select player_id, player_surname, player_forename, team from players where team_id=%s group by player_id, team_id;'
        return self._run_query(sql, team_id)

    def get_team_fixtures(self, team_id):
        """
        Get all fixtures for a given team

        :returns: ( (date, team, team_id, opposition, opposition_id, venue), ... )
        """

        sql = 'select date, team_id, team, opposition_id, opposition, venue from players where team_id=%s group by team_id, opposition_id;'
        return self._run_query(sql, team_id)