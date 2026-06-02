from django.test import SimpleTestCase
from django.urls import resolve, reverse

from apps.tierlist.views import (
    TierListEntryCreateView,
    TierListEntryUpdateView,
    TierListView,
)


class TierListUrlTests(SimpleTestCase):

    def test_tier_list_urls_resolve(self):
        self.assertEqual(
            resolve(reverse('tierlist:tier-list')).func.view_class,
            TierListView
        )
        self.assertEqual(
            resolve(reverse('tierlist:tier-entry-create')).func.view_class,
            TierListEntryCreateView
        )
        self.assertEqual(
            resolve(reverse('tierlist:tier-entry-update', kwargs={'pk': 1})).func.view_class,
            TierListEntryUpdateView
        )
