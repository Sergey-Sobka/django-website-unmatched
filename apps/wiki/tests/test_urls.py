from django.test import SimpleTestCase
from django.urls import resolve, reverse

from apps.wiki.views import (
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


class WikiUrlTests(SimpleTestCase):

    def test_game_set_urls_resolve(self):
        self.assertEqual(
            resolve(reverse('wiki:game-set-list')).func.view_class,
            GameSetListView
        )
        self.assertEqual(
            resolve(reverse('wiki:game-set-detail', kwargs={'slug': 'set'})).func.view_class,
            GameSetDetailView
        )
        self.assertEqual(
            resolve(reverse('wiki:game-set-update', kwargs={'slug': 'set'})).func.view_class,
            GameSetUpdateView
        )

    def test_map_urls_resolve(self):
        self.assertEqual(
            resolve(reverse('wiki:map-list')).func.view_class,
            MapListView
        )
        self.assertEqual(
            resolve(reverse('wiki:map-detail', kwargs={'slug': 'map'})).func.view_class,
            MapDetailView
        )
        self.assertEqual(
            resolve(reverse('wiki:map-update', kwargs={'slug': 'map'})).func.view_class,
            MapUpdateView
        )

    def test_character_urls_resolve(self):
        self.assertEqual(
            resolve(reverse('wiki:character-list')).func.view_class,
            CharacterListView
        )
        self.assertEqual(
            resolve(reverse('wiki:character-detail', kwargs={'slug': 'hero'})).func.view_class,
            CharacterDetailView
        )
        self.assertEqual(
            resolve(reverse('wiki:character-update', kwargs={'slug': 'hero'})).func.view_class,
            CharacterUpdateView
        )

    def test_card_update_url_resolves(self):
        self.assertEqual(
            resolve(reverse('wiki:card-update', kwargs={'pk': 1})).func.view_class,
            CardUpdateView
        )
