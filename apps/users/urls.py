from django.urls import path

from .views import (
    ProfileUpdateView,
    ProfileView,
    ReferralInviteCreateView,
    ReferralInviteListView,
    referral_accept_view,
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
        referral_accept_view,
        name='referral-accept'
    ),
]
