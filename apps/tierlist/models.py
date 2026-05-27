from django.conf import settings
from django.db import models

from apps.wiki.models import Character


class TierListEntry(models.Model):

    class Modes(models.TextChoices):
        ONE_VS_ONE = '1v1', '1 vs 1'
        TWO_VS_TWO = '2v2', '2 vs 2'

    class Tiers(models.TextChoices):
        S = 'S', 'S'
        A = 'A', 'A'
        B = 'B', 'B'
        C = 'C', 'C'
        D = 'D', 'D'

    mode = models.CharField(
        max_length=10,
        choices=Modes.choices
    )

    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='tier_entries'
    )

    tier = models.CharField(
        max_length=1,
        choices=Tiers.choices
    )

    notes = models.TextField(
        blank=True
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            'mode',
            'character',
        )

    def __str__(self):
        return f'{self.character} - {self.mode} - {self.tier}'
