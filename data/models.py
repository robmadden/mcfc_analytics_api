from django.db import models, connection

class Players(models.Model):
    _db = 'mcfc_analytics'

    id = models.AutoField(primary_key=True)
    player_surname = models.CharField(max_length=30, null=True, blank=True)
    player_forename = models.CharField(max_length=30, null=True, blank=True)
    team = models.CharField(max_length=50, null=True, blank=True)
    player_id = models.IntegerField(max_length=11)

    def get_teams(self):
        """
        Fetch all the teams and their corresponding IDs

        @returns [ (team_id, team_name), (team_id, team_name), ... ]
        """

        sql = "select team_id, team from players group by team_id;"
        cursor = connection.cursor()
        cursor.execute(sql)
        teams = cursor.fetchall()
        cursor.close()
        return teams

    def get_players_on_team(self, team_id):
        """
        Get all players on a team given a team ID

        @returns [ (player_id, player_surname, player_forname), ... ]
        """
        sql = 'select player_id, player_surname, player_forename, team from players where team_id=%s group by player_id, team_id;'
        cursor = connection.cursor()
        cursor.execute(sql, team_id)
        players = cursor.fetchall()
        cursor.close()
        return players