from django.test import TestCase
from django.urls import reverse


class CoreViewTests(TestCase):

    def test_home_page(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Unmatched Wiki')
