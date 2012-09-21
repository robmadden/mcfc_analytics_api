from django.db import models

class Players(models.Model):
    _db = 'mcfc_analytics'

    id = models.AutoField(primary_key=True)
    player_surname = models.CharField(max_length=30, null=True, blank=True)
    player_forename = models.CharField(max_length=30, null=True, blank=True)
    team = models.CharField(max_length=50, null=True, blank=True)
    player_id = models.IntegerField(max_length=11)