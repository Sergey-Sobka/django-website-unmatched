from django.urls import path

from .views import (
    ProfileUpdateView,
    ProfileView,
    ReferralInviteCreateView,
    ReferralInviteListView,
    ReferralAcceptView,
)


app_name = 'users'

urlpatterns = [
    path(
        'profile/',
        ProfileView.as_view(),
        name='profile'
    ),
    path(
        'profile/edit/',
        ProfileUpdateView.as_view(),
        name='profile-edit'
    ),
    path(
        'invites/',
        ReferralInviteListView.as_view(),
        name='referral-invite-list'
    ),
    path(
        'invites/create/',
        ReferralInviteCreateView.as_view(),
        name='referral-invite-create'
    ),
    path(
        'invites/<str:code>/',
        ReferralAcceptView.as_view(),
        name='referral-accept'
    ),
]
