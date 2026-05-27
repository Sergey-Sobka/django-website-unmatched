from django.urls import path

from .views import (
    TierListEntryCreateView,
    TierListEntryUpdateView,
    TierListView,
)


app_name = 'tierlist'

urlpatterns = [
    path(
        '',
        TierListView.as_view(),
        name='tier-list'
    ),
    path(
        'add/',
        TierListEntryCreateView.as_view(),
        name='tier-entry-create'
    ),
    path(
        '<int:pk>/edit/',
        TierListEntryUpdateView.as_view(),
        name='tier-entry-update'
    ),
]
