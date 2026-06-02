from django.urls import path

from .views import (
    CardUpdateView,
    CharacterDetailView,
    CharacterListView,
    CharacterUpdateView,
    GameSetDetailView,
    GameSetListView,
    GameSetUpdateView,
    MapDetailView,
    MapListView,
    MapUpdateView,
)


app_name = 'wiki'

urlpatterns = [
    path(
        'sets/',
        GameSetListView.as_view(),
        name='game-set-list'
    ),
    path(
        'sets/<slug:slug>/',
        GameSetDetailView.as_view(),
        name='game-set-detail'
    ),
    path(
        'sets/<slug:slug>/edit/',
        GameSetUpdateView.as_view(),
        name='game-set-update'
    ),
    path(
        'maps/',
        MapListView.as_view(),
        name='map-list'
    ),
    path(
        'maps/<slug:slug>/',
        MapDetailView.as_view(),
        name='map-detail'
    ),
    path(
        'maps/<slug:slug>/edit/',
        MapUpdateView.as_view(),
        name='map-update'
    ),
    path(
        'characters/',
        CharacterListView.as_view(),
        name='character-list'
    ),
    path(
        'characters/<slug:slug>/',
        CharacterDetailView.as_view(),
        name='character-detail'
    ),
    path(
        'characters/<slug:slug>/edit/',
        CharacterUpdateView.as_view(),
        name='character-update'
    ),
    path(
        'cards/<int:pk>/edit/',
        CardUpdateView.as_view(),
        name='card-update'
    ),
]
