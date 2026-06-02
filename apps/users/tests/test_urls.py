from django.test import SimpleTestCase
from django.urls import resolve, reverse

from apps.users.views import (
    ProfileUpdateView,
    ProfileView,
    ReferralAcceptView,
    ReferralInviteCreateView,
    ReferralInviteListView,
)


class UserUrlTests(SimpleTestCase):

    def test_profile_urls_resolve(self):
        self.assertEqual(
            resolve(reverse('users:profile')).func.view_class,
            ProfileView
        )
        self.assertEqual(
            resolve(reverse('users:profile-edit')).func.view_class,
            ProfileUpdateView
        )

    def test_referral_urls_resolve(self):
        self.assertEqual(
            resolve(reverse('users:referral-invite-list')).func.view_class,
            ReferralInviteListView
        )
        self.assertEqual(
            resolve(reverse('users:referral-invite-create')).func.view_class,
            ReferralInviteCreateView
        )
        self.assertEqual(
            resolve(reverse('users:referral-accept', kwargs={'code': 'ABC'})).func.view_class,
            ReferralAcceptView
        )
