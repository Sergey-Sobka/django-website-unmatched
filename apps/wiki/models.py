from django.db import models
from django.urls import reverse

from .services import create_unique_slug


class GameSet(models.Model):
    name = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    release_year = models.IntegerField()

    description = models.TextField()

    bgg_link = models.URLField(
        blank=True
    )

    cover_image = models.ImageField(
        upload_to='gamesets/',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_unique_slug(
                GameSet,
                self.name
            )

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'wiki:game-set-detail',
            kwargs={
                'slug': self.slug
            }
        )

    def __str__(self):
        return self.name


class Character(models.Model):

    class AttackTypes(models.TextChoices):
        MELEE = 'melee', 'Melee'
        RANGED = 'ranged', 'Ranged'

    game_set = models.ForeignKey(
        GameSet,
        on_delete=models.CASCADE,
        related_name='characters'
    )

    name = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    subtitle = models.CharField(
        max_length=255,
        blank=True
    )

    description = models.TextField()

    movement = models.IntegerField(default=2)

    special = models.TextField(
        blank=True
    )

    quote = models.TextField(
        blank=True
    )

    health = models.IntegerField()

    attack_type = models.CharField(
        max_length=20,
        choices=AttackTypes.choices
    )

    image = models.ImageField(
        upload_to='characters/',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_unique_slug(
                Character,
                self.name
            )

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'wiki:character-detail',
            kwargs={
                'slug': self.slug
            }
        )

    def __str__(self):
        return self.name


class Sidekick(models.Model):
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='sidekicks'
    )

    name = models.CharField(max_length=255)

    description = models.TextField(
        blank=True
    )

    count = models.IntegerField(default=1)

    health = models.IntegerField()

    image = models.ImageField(
        upload_to='sidekicks/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Card(models.Model):

    class CardTypes(models.TextChoices):
        ATTACK = 'attack', 'Attack'
        DEFENSE = 'defense', 'Defense'
        VERSATILE = 'versatile', 'Versatile'
        SCHEME = 'scheme', 'Scheme'

    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='cards'
    )

    name = models.CharField(max_length=255)

    card_type = models.CharField(
        max_length=20,
        choices=CardTypes.choices
    )

    quantity = models.IntegerField(default=1)

    value = models.IntegerField(
        null=True,
        blank=True
    )

    boost = models.IntegerField(
        null=True,
        blank=True
    )

    text = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to='cards/',
        null=True,
        blank=True
    )

    source_image_url = models.URLField(
        blank=True
    )

    def __str__(self):
        return self.name


class Map(models.Model):
    game_set = models.ForeignKey(
        GameSet,
        on_delete=models.CASCADE,
        related_name='maps'
    )

    name = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    description = models.TextField()

    players_count = models.IntegerField(default=2)

    spaces_count = models.IntegerField(
        null=True,
        blank=True
    )

    zone_count = models.IntegerField(
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to='maps/',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_unique_slug(
                Map,
                self.name
            )

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'wiki:map-detail',
            kwargs={
                'slug': self.slug
            }
        )

    def __str__(self):
        return self.name
