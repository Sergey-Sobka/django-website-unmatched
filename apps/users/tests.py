from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import ReferralInvite


class ReferralInviteTests(TestCase):

    def test_editor_invite_creates_editor_user(self):
        User = get_user_model()
        staff = User.objects.create_user(
            username='staff',
            email='staff@example.com',
            password='test-pass-123',
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
