from django.test import TestCase

from apps.tierlist.models import TierListEntry
from apps.wiki.models import Character, GameSet


class TierListEntryModelTests(TestCase):

    def test_tier_list_entry_string(self):
        game_set = GameSet.objects.create(
            name='Test Set',
            release_year=2024,
            description='Test description',
        )
        character = Character.objects.create(
            game_set=game_set,
            name='Test Hero',
            description='Test hero description',
            health=10,
            attack_type=Character.AttackTypes.MELEE,
        )
        entry = TierListEntry.objects.create(
            mode=TierListEntry.Modes.ONE_VS_ONE,
            character=character,
            tier=TierListEntry.Tiers.S,
        )

        self.assertEqual(str(entry), 'Test Hero - 1v1 - S')
