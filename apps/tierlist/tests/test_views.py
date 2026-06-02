from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from apps.tierlist.models import TierListEntry
from apps.users.models import User
from apps.wiki.models import Character, GameSet


class TierListViewTests(TestCase):

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
        self.entry = TierListEntry.objects.create(
            mode=TierListEntry.Modes.ONE_VS_ONE,
            character=self.character,
            tier=TierListEntry.Tiers.S,
        )

    def login_editor(self):
        user = User.objects.create_user(
            username='editor',
            email='editor@example.com',
            password='testpass123',
        )
        permissions = Permission.objects.filter(
            content_type__app_label='tierlist',
            codename__in=[
                'add_tierlistentry',
                'change_tierlistentry',
            ]
        )
        user.user_permissions.set(permissions)
        self.client.force_login(user)

        return user

    def test_tier_list_page(self):
        response = self.client.get(reverse('tierlist:tier-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Hero')

    def test_create_page_requires_login(self):
        response = self.client.get(reverse('tierlist:tier-entry-create'))

        self.assertEqual(response.status_code, 302)

    def test_editor_with_permission_can_open_create_page(self):
        self.login_editor()

        response = self.client.get(reverse('tierlist:tier-entry-create'))

        self.assertEqual(response.status_code, 200)

    def test_editor_with_permission_can_open_update_page(self):
        self.login_editor()

        response = self.client.get(
            reverse('tierlist:tier-entry-update', kwargs={'pk': self.entry.id})
        )

        self.assertEqual(response.status_code, 200)
