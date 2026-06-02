from django.test import SimpleTestCase
from django.urls import resolve, reverse

from apps.stats.views import (
    CharacterStatsView,
    MatchRecordCreateView,
    MatchRecordListView,
)


class StatsUrlTests(SimpleTestCase):

    def test_stats_urls_resolve(self):
        self.assertEqual(
            resolve(reverse('stats:character-stats')).func.view_class,
            CharacterStatsView
        )
        self.assertEqual(
            resolve(reverse('stats:match-list')).func.view_class,
            MatchRecordListView
        )
        self.assertEqual(
            resolve(reverse('stats:match-create')).func.view_class,
            MatchRecordCreateView
        )
