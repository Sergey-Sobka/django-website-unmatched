from django.test import SimpleTestCase
from django.urls import resolve, reverse

from apps.core.views import HomePageView


class CoreUrlTests(SimpleTestCase):

    def test_home_url_resolves(self):
        resolver = resolve(reverse('home'))

        self.assertEqual(resolver.func.view_class, HomePageView)
