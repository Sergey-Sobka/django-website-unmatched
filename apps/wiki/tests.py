from django.test import TestCase

from apps.users.models import User

from .models import Card, Character, GameSet, Map, Sidekick


class WikiModelTests(TestCase):

    def test_character_slug_is_created(self):
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

        self.assertEqual(character.slug, 'test-hero')


class WikiViewTests(TestCase):

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
        Sidekick.objects.create(
            character=self.character,
            name='Helper',
            health=3,
        )
        self.card = Card.objects.create(
            character=self.character,
            name='Test Card',
            card_type=Card.CardTypes.ATTACK,
            quantity=1,
            value=3,
        )
        self.map = Map.objects.create(
            game_set=self.game_set,
            name='Test Map',
            description='Test map description',
        )

    def test_character_list_page(self):
        response = self.client.get('/characters/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Hero')

    def test_character_detail_page(self):
        response = self.client.get(self.character.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Card')

    def test_map_list_page(self):
        response = self.client.get('/maps/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Map')

    def test_editor_can_open_edit_pages(self):
        user = User.objects.create_user(
            username='editor',
            email='editor@example.com',
            password='testpass123',
            is_staff=True,
        )
        self.client.force_login(user)

        urls = [
            f'/sets/{self.game_set.slug}/edit/',
            f'/characters/{self.character.slug}/edit/',
            f'/maps/{self.map.slug}/edit/',
            f'/cards/{self.card.id}/edit/',
        ]

        for url in urls:
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
