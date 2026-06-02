from django.conf import settings
from django.db import models

from apps.wiki.models import Character, Map


class MatchRecord(models.Model):

    class Modes(models.TextChoices):
        ONE_VS_ONE = '1v1', '1 vs 1'
        TWO_VS_TWO = '2v2', '2 vs 2'

    class Winners(models.TextChoices):
        TEAM_ONE = 'team_one', 'Team One'
        TEAM_TWO = 'team_two', 'Team Two'

    mode = models.CharField(
        max_length=10,
        choices=Modes.choices,
        default=Modes.ONE_VS_ONE
    )

    map = models.ForeignKey(
        Map,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    team_one_player = models.CharField(max_length=100)

    team_one_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='team_one_matches'
    )

    team_one_partner = models.ForeignKey(
        Character,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_one_partner_matches'
    )

    team_two_player = models.CharField(max_length=100)

    team_two_character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='team_two_matches'
    )

    team_two_partner = models.ForeignKey(
        Character,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_two_partner_matches'
    )

    winner = models.CharField(
        max_length=20,
        choices=Winners.choices
    )

    notes = models.TextField(
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    played_at = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.team_one_character} vs {self.team_two_character}'
