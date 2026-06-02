from datetime import date

from django.test import TestCase

from apps.stats.models import MatchRecord
from apps.wiki.models import Character, GameSet


class MatchRecordModelTests(TestCase):

    def test_match_record_string(self):
        game_set = GameSet.objects.create(
            name='Test Set',
            release_year=2024,
            description='Test description',
        )
        hero_one = Character.objects.create(
            game_set=game_set,
            name='Hero One',
            description='Hero one description',
            health=10,
            attack_type=Character.AttackTypes.MELEE,
        )
        hero_two = Character.objects.create(
            game_set=game_set,
            name='Hero Two',
            description='Hero two description',
            health=12,
            attack_type=Character.AttackTypes.RANGED,
        )
        match = MatchRecord.objects.create(
            team_one_player='Player One',
            team_one_character=hero_one,
            team_two_player='Player Two',
            team_two_character=hero_two,
            winner=MatchRecord.Winners.TEAM_ONE,
            played_at=date.today(),
        )

        self.assertEqual(str(match), 'Hero One vs Hero Two')
