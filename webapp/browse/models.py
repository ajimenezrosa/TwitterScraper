from django.db import models


class Users(models.Model):
    username = models.TextField(blank=True, primary_key=True)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    locations = models.TextField(blank=True, null=True)
    personality = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
