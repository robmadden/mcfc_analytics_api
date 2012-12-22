from db_helpers import run_singlerow_query, run_multirow_query

class Player():
    def __init__(self, player_id):
        self.player_id = player_id

    def get_minutes_played(self):
        """
        Get the number of minutes a player played in a season

        :returns: ( player_id, player_surname, player_forename, minutes played)
        """

        sql = """SELECT player_id, player_surname, player_forename, SUM(time_played)
                 FROM players WHERE player_id=%s GROUP BY player_id;"""

        return run_singlerow_query(sql, self.player_id)

    ############################### DRIBBLING #################################

    def get_touches(self):
        """
        Get the number of times a player touched the ball over the course of a season

        :returns: ( player_id, player_surname, player_forename, touches)
        """

        sql = """SELECT player_id, player_surname, player_forename, SUM(touches)
                 FROM players WHERE player_id=%s GROUP BY player_id;"""

        return run_singlerow_query(sql, self.player_id)

    def get_dispossessions(self):
        """
        Get the number of times a player was dispossed over an entire season

        :returns: ( player_id, player_surname, player_forename, dispossesions)
        """

        sql = """SELECT player_id, player_surname, player_forename, SUM(dispossessed)
                 FROM players WHERE player_id=%s GROUP BY player_id;"""

        return run_singlerow_query(sql, self.player_id)

    def get_turnovers(self):
        """
        Get the number of turnovers for a given player over an entire season

        :returns: ( player_id, player_surname, player_forename, turnovers)
        """

        sql = """SELECT player_id, player_surname, player_forename, SUM(turnovers)
                 FROM players WHERE player_id=%s GROUP BY player_id;"""

        return run_singlerow_query(sql, self.player_id)

    ################################ PASSING ##################################

    def _run_passing_query(self, sql):
        """
        Helper function used by all passing calculating functions
        """

        results = run_singlerow_query(sql, self.player_id)
        percentage = results[3] / (results[3] + results[4])
        return results, percentage

    def get_minutes_played(self):
        """
        Get the number of successful, unsuccessful, and pass percentage for a given player over an entire season
        
        :returns: ( player_id, player_surname, player_forename, minutes_played)
        """

        sql = """SELECT player_id, player_surname, player_forename, SUM(time_played)
                 FROM players WHERE player_id=%s GROUP BY player_id;"""

        return run_multirow_query(sql, self.player_id)

    def get_passing_percentage(self):
        """
        Get the number of successful, unsuccessful, and pass percentage for a given player over an entire season

        :returns: ( player_id, player_surname, player_forename, successes, failures, percentage)
        """

        sql = """SELECT player_id, player_surname, player_forename, SUM(total_successful_passes_excl_crosses_corners),
                 SUM(total_unsuccessful_passes_excl_crosses_corners)
                 FROM players where player_id=%s GROUP BY player_id;"""

        return self._run_passing_query(sql)

    def get_passing_percentage_own_half(self):
        """
        Get the number of successful, unsuccessful, and pass percentage for a given player in their own half
        over an entire season

        :returns: ( player_id, player_surname, player_forename, successes, failures, percentage)
        """

        sql = """SELECT player_id, player_surname, player_forename, SUM(successful_passes_own_half),
                 SUM(unsuccessful_passes_own_half)
                 FROM players where player_id=%s GROUP BY player_id;"""

        return self._run_passing_query(sql)

    def get_passing_percentage_opposition_half(self):
        """
        Get the number of successful, unsuccessful, and pass percentage for a given player in the oppositions half
        over an entire season

        :returns: ( player_id, player_surname, player_forename, successes, failures, percentage)
        """

        sql = """SELECT player_id, player_surname, player_forename, SUM(successful_passes_opposition_half),
                 SUM(unsuccessful_passes_opposition_half)
                 FROM players where player_id=%s GROUP BY player_id;"""

        return self._run_passing_query(sql)

    def get_passing_percentage_defensive_third(self):
        """
        Get the number of successful, unsuccessful, and pass percentage for a given player in their defensive third
        over an entire season

        :returns: ( player_id, player_surname, player_forename, successes, failures, percentage)
        """

        sql = """SELECT player_id, player_surname, player_forename, SUM(successful_passes_defensive_third),
                 SUM(unsuccessful_passes_defensive_third)
                 FROM players where player_id=%s GROUP BY player_id;"""

        return self._run_passing_query(sql)

    def get_passing_percentage_middle_third(self):
        """
        Get the number of successful, unsuccessful, and pass percentage for a given player in the middle third
        over an entire season

        :returns: ( player_id, player_surname, player_forename, successes, failures, percentage)
        """

        sql = """SELECT player_id, player_surname, player_forename, SUM(successful_passes_middle_third),
                 SUM(unsuccessful_passes_middle_third)
                 FROM players where player_id=%s GROUP BY player_id;"""

        return self._run_passing_query(sql)

    def get_passing_percentage_final_third(self):
        """
        Get the number of successful, unsuccessful, and pass percentage for a given player in the final third
        over an entire season

        :returns: ( player_id, player_surname, player_forename, successes, failures, percentage)
        """

        sql = """SELECT player_id, player_surname, player_forename, SUM(successful_passes_final_third),
                 SUM(unsuccessful_passes_final_third)
                 FROM players where player_id=%s GROUP BY player_id;"""

        return self._run_passing_query(sql)

    def get_passing_percentage_short_passes(self):
        """
        Get the number of successful, unsuccessful, and pass percentage for a given player for short passes
        over an entire season

        :returns: ( player_id, player_surname, player_forename, successes, failures, percentage)
        """

        sql = """SELECT player_id, player_surname, player_forename, SUM(successful_short_passes),
                 SUM(unsuccessful_short_passes)
                 FROM players where player_id=%s GROUP BY player_id;"""

        return self._run_passing_query(sql)

    def get_passing_percentage_long_passes(self):
        """
        Get the number of successful, unsuccessful, and pass percentage for a given player for short passes
        over an entire season

        :returns: ( player_id, player_surname, player_forename, successes, failures, percentage)
        """

        sql = """SELECT player_id, player_surname, player_forename, SUM(successful_long_passes),
                 SUM(unsuccessful_long_passes)
                 FROM players where player_id=%s GROUP BY player_id;"""

        return self._run_passing_query(sql)