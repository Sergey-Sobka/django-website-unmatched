from django.test import TestCase

from apps.users.models import ReferralInvite, User


class UserModelTests(TestCase):

    def test_user_string(self):
        user = User.objects.create_user(
            username='john',
            email='john@example.com',
            password='testpass123',
        )

        self.assertEqual(str(user), 'john')

    def test_profile_created_for_user(self):
        user = User.objects.create_user(
            username='john',
            email='john@example.com',
            password='testpass123',
        )

        self.assertEqual(user.profile.user, user)

    def test_referral_invite_fields(self):
        invite = ReferralInvite.objects.create(
            email='editor@example.com',
            role=ReferralInvite.InviteRoles.EDITOR,
        )

        self.assertTrue(invite.code)
        self.assertEqual(str(invite), 'editor@example.com - editor')

    def test_referral_invite_use(self):
        user = User.objects.create_user(
            username='editor',
            email='editor@example.com',
            password='testpass123',
        )
        invite = ReferralInvite.objects.create(
            email='editor@example.com',
            role=ReferralInvite.InviteRoles.EDITOR,
        )

        invite.use(user)

        self.assertEqual(invite.accepted_by, user)
        self.assertEqual(invite.status, ReferralInvite.Status.USED)
        self.assertIsNotNone(invite.used_at)
