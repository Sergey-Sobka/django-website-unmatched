from django.test import TestCase
from django.urls import reverse

from apps.wiki.models import Card, Character, GameSet, Map, Sidekick


class WikiModelTests(TestCase):

    def setUp(self):
        self.game_set = GameSet.objects.create(
            name='Test Set',
            release_year=2024,
            description='Test description',
        )
        self.character = Character.objects.create(
            game_set=self.game_set,
            name='Test Hero',
            description='Test hero description',
            health=10,
            attack_type=Character.AttackTypes.MELEE,
        )
        self.map = Map.objects.create(
            game_set=self.game_set,
            name='Test Map',
            description='Test map description',
        )

    def test_game_set_fields(self):
        self.assertEqual(str(self.game_set), 'Test Set')
        self.assertEqual(self.game_set.slug, 'test-set')
        self.assertEqual(
            self.game_set.get_absolute_url(),
            reverse('wiki:game-set-detail', kwargs={'slug': self.game_set.slug})
        )

    def test_character_fields(self):
        self.assertEqual(str(self.character), 'Test Hero')
        self.assertEqual(self.character.slug, 'test-hero')
        self.assertEqual(
            self.character.get_absolute_url(),
            reverse('wiki:character-detail', kwargs={'slug': self.character.slug})
        )

    def test_map_fields(self):
        self.assertEqual(str(self.map), 'Test Map')
        self.assertEqual(self.map.slug, 'test-map')
        self.assertEqual(
            self.map.get_absolute_url(),
            reverse('wiki:map-detail', kwargs={'slug': self.map.slug})
        )

    def test_sidekick_string(self):
        sidekick = Sidekick.objects.create(
            character=self.character,
            name='Helper',
            health=3,
        )

        self.assertEqual(str(sidekick), 'Helper')

    def test_card_string(self):
        card = Card.objects.create(
            character=self.character,
            name='Test Card',
            card_type=Card.CardTypes.ATTACK,
            quantity=1,
        )

        self.assertEqual(str(card), 'Test Card')

    def test_duplicate_slug_gets_number(self):
        second_character = Character.objects.create(
            game_set=self.game_set,
            name='Test Hero',
            description='Second hero',
            health=12,
            attack_type=Character.AttackTypes.RANGED,
        )

        self.assertEqual(second_character.slug, 'test-hero-1')
