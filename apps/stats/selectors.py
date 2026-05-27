from collections import defaultdict

from apps.wiki.models import Character

from .models import MatchRecord


def match_list():
    return MatchRecord.objects.select_related(
        'team_one_character',
        'team_one_partner',
        'team_two_character',
        'team_two_partner',
        'map',
        'created_by',
    ).order_by('-played_at', '-created_at')


def character_stats(mode=''):
    stats = defaultdict(
        lambda: {
            'wins': 0,
            'losses': 0,
            'games': 0,
        }
    )

    matches = MatchRecord.objects.all()

    if mode:
        matches = matches.filter(mode=mode)

    for match in matches:
        team_one = [
            match.team_one_character_id,
            match.team_one_partner_id,
        ]
        team_two = [
            match.team_two_character_id,
            match.team_two_partner_id,
        ]

        for character_id in filter(None, team_one):
            stats[character_id]['games'] += 1
            stats[character_id]['wins' if match.winner == MatchRecord.Winners.TEAM_ONE else 'losses'] += 1

        for character_id in filter(None, team_two):
            stats[character_id]['games'] += 1
            stats[character_id]['wins' if match.winner == MatchRecord.Winners.TEAM_TWO else 'losses'] += 1

    characters = Character.objects.filter(
        id__in=stats.keys()
    ).order_by('name')

    result = []

    for character in characters:
        row = stats[character.id]
        games = row['games']
        winrate = round(row['wins'] / games * 100, 1) if games else 0
        result.append(
            {
                'character': character,
                'wins': row['wins'],
                'losses': row['losses'],
                'games': games,
                'winrate': winrate,
            }
        )

    return sorted(
        result,
        key=lambda item: item['winrate'],
        reverse=True
    )
