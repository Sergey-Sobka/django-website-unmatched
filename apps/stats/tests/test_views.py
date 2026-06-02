from datetime import date

from django.test import TestCase
from django.urls import reverse

from apps.stats.models import MatchRecord
from apps.users.models import User
from apps.wiki.models import Character, GameSet, Map


class StatsViewTests(TestCase):

    def setUp(self):
        self.game_set = GameSet.objects.create(
            name='Test Set',
            release_year=2024,
            description='Test description',
        )
        self.hero_one = Character.objects.create(
            game_set=self.game_set,
            name='Hero One',
            description='Hero one description',
            health=10,
            attack_type=Character.AttackTypes.MELEE,
        )
        self.hero_two = Character.objects.create(
            game_set=self.game_set,
            name='Hero Two',
            description='Hero two description',
            health=12,
            attack_type=Character.AttackTypes.RANGED,
        )
        self.map = Map.objects.create(
            game_set=self.game_set,
            name='Test Map',
            description='Test map description',
        )
        self.match = MatchRecord.objects.create(
            map=self.map,
            team_one_player='Player One',
            team_one_character=self.hero_one,
            team_two_player='Player Two',
            team_two_character=self.hero_two,
            winner=MatchRecord.Winners.TEAM_ONE,
            played_at=date.today(),
        )

    def test_character_stats_page(self):
        response = self.client.get(reverse('stats:character-stats'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hero One')

    def test_match_list_page(self):
        response = self.client.get(reverse('stats:match-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hero One')

    def test_match_create_page_requires_login(self):
        response = self.client.get(reverse('stats:match-create'))

        self.assertEqual(response.status_code, 302)

    def test_logged_user_can_create_match(self):
        user = User.objects.create_user(
            username='john',
            email='john@example.com',
            password='testpass123',
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse('stats:match-create'),
            {
                'mode': MatchRecord.Modes.ONE_VS_ONE,
                'map': self.map.id,
                'team_one_player': 'Player One',
                'team_one_character': self.hero_one.id,
                'team_one_partner': '',
                'team_two_player': 'Player Two',
                'team_two_character': self.hero_two.id,
                'team_two_partner': '',
                'winner': MatchRecord.Winners.TEAM_TWO,
                'played_at': '2024-01-01',
                'notes': 'Test notes',
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            MatchRecord.objects.filter(winner=MatchRecord.Winners.TEAM_TWO).exists()
        )
