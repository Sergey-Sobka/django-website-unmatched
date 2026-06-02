from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from apps.users.models import ReferralInvite, User


class UserViewTests(TestCase):

    def test_profile_page_requires_login(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 302)

    def test_profile_page_for_logged_user(self):
        user = User.objects.create_user(
            username='john',
            email='john@example.com',
            password='testpass123',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'john')

    def test_profile_update(self):
        user = User.objects.create_user(
            username='john',
            email='john@example.com',
            password='testpass123',
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse('users:profile-edit'),
            {
                'bio': 'Test bio',
            }
        )
        user.profile.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.profile.bio, 'Test bio')

    def test_referral_accept_sets_session(self):
        invite = ReferralInvite.objects.create(
            email='editor@example.com',
            role=ReferralInvite.InviteRoles.EDITOR,
        )

        response = self.client.get(
            reverse('users:referral-accept', kwargs={'code': invite.code})
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['invite_code'], invite.code)
        self.assertIn('/accounts/signup/', response['Location'])

    def test_referral_invite_list_with_permission(self):
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
        )
        permission = Permission.objects.get(codename='view_referralinvite')
        user.user_permissions.add(permission)
        self.client.force_login(user)
        ReferralInvite.objects.create(
            email='editor@example.com',
            role=ReferralInvite.InviteRoles.EDITOR,
            created_by=user,
        )

        response = self.client.get(reverse('users:referral-invite-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'editor@example.com')

    def test_referral_invite_create_with_permission(self):
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
        )
        permissions = Permission.objects.filter(
            content_type__app_label='users',
            codename__in=[
                'add_referralinvite',
                'view_referralinvite',
            ]
        )
        user.user_permissions.set(permissions)
        self.client.force_login(user)

        response = self.client.post(
            reverse('users:referral-invite-create'),
            {
                'email': 'editor@example.com',
                'role': ReferralInvite.InviteRoles.EDITOR,
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ReferralInvite.objects.filter(email='editor@example.com').exists()
        )

    def test_editor_invite_creates_editor_user(self):
        staff = User.objects.create_user(
            username='staff',
            email='staff@example.com',
            password='testpass123',
            is_staff=True,
        )
        invite = ReferralInvite.objects.create(
            email='editor@example.com',
            role=ReferralInvite.InviteRoles.EDITOR,
            created_by=staff,
        )

        response = self.client.post(
            f'/accounts/signup/?invite={invite.code}',
            {
                'username': 'editor',
                'email': 'editor@example.com',
                'password1': 'StrongPass12345',
                'password2': 'StrongPass12345',
            },
        )

        self.assertEqual(response.status_code, 302)

        editor = User.objects.get(username='editor')
        invite.refresh_from_db()

        self.assertEqual(editor.role, User.Roles.EDITOR)
        self.assertTrue(editor.is_staff)
        self.assertEqual(invite.status, ReferralInvite.Status.USED)
