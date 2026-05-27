from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Character, GameSet, Map


def game_set_list():
    return GameSet.objects.order_by('release_year', 'name')


def game_set_get_by_slug(slug):
    return get_object_or_404(
        GameSet.objects.prefetch_related(
            'characters',
            'maps',
        ),
        slug=slug
    )


def map_list(game_set=''):
    maps = Map.objects.select_related(
        'game_set'
    ).order_by('name')

    if game_set:
        maps = maps.filter(
            game_set_id=game_set
        )

    return maps


def map_get_by_slug(slug):
    return get_object_or_404(
        Map.objects.select_related('game_set'),
        slug=slug
    )


def character_list(search='', attack_type='', game_set=''):
    characters = Character.objects.select_related(
        'game_set'
    ).order_by('name')

    if search:
        characters = characters.filter(
            Q(name__icontains=search)
            | Q(subtitle__icontains=search)
            | Q(description__icontains=search)
        )

    if attack_type:
        characters = characters.filter(
            attack_type=attack_type
        )

    if game_set:
        characters = characters.filter(
            game_set_id=game_set
        )

    return characters


def character_get_by_slug(slug):
    return get_object_or_404(
        Character.objects.select_related(
            'game_set'
        ).prefetch_related(
            'sidekicks',
            'cards',
        ),
        slug=slug
    )
