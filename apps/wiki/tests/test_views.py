from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from apps.users.models import User
from apps.wiki.models import Card, Character, GameSet, Map, Sidekick


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

    def login_editor(self):
        user = User.objects.create_user(
            username='editor',
            email='editor@example.com',
            password='testpass123',
        )
        permissions = Permission.objects.filter(
            content_type__app_label='wiki',
            codename__in=[
                'change_gameset',
                'change_character',
                'change_map',
                'change_card',
            ]
        )
        user.user_permissions.set(permissions)
        self.client.force_login(user)

    def test_game_set_list_page(self):
        response = self.client.get(reverse('wiki:game-set-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Set')

    def test_character_list_page(self):
        response = self.client.get(reverse('wiki:character-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Hero')

    def test_character_detail_page(self):
        response = self.client.get(self.character.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Card')

    def test_map_list_page(self):
        response = self.client.get(reverse('wiki:map-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Map')

    def test_map_detail_page(self):
        response = self.client.get(self.map.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Map')

    def test_editor_with_permissions_can_open_edit_pages(self):
        self.login_editor()

        urls = [
            reverse('wiki:game-set-update', kwargs={'slug': self.game_set.slug}),
            reverse('wiki:character-update', kwargs={'slug': self.character.slug}),
            reverse('wiki:map-update', kwargs={'slug': self.map.slug}),
            reverse('wiki:card-update', kwargs={'pk': self.card.id}),
        ]

        for url in urls:
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
