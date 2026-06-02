from django.urls import path

from .views import (
    CharacterStatsView,
    MatchRecordCreateView,
    MatchRecordListView,
)


app_name = 'stats'

urlpatterns = [
    path(
        '',
        CharacterStatsView.as_view(),
        name='character-stats'
    ),
    path(
        'matches/',
        MatchRecordListView.as_view(),
        name='match-list'
    ),
    path(
        'matches/add/',
        MatchRecordCreateView.as_view(),
        name='match-create'
    ),
]
