from django.test import SimpleTestCase
from django.urls import reverse

from .catalog import load_catalog


class ApiDocsPagesTests(SimpleTestCase):

    def test_home(self):
        response = self.client.get(reverse('apidocs:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jardinagem')

    def test_getting_started(self):
        response = self.client.get(reverse('apidocs:getting_started'))
        self.assertEqual(response.status_code, 200)

    def test_every_section(self):
        for platform in load_catalog():
            url = reverse('apidocs:platform', args=[platform['slug']])
            self.assertEqual(self.client.get(url).status_code, 200)
            for section in platform['sections']:
                url = reverse('apidocs:section', args=[platform['slug'], section['slug']])
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_unknown_section(self):
        url = reverse('apidocs:section', args=['jardinagem', 'nao-existe'])
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_catalog_has_no_credentials(self):
        text = str(load_catalog())
        self.assertNotIn('127.0.0.1', text)
        self.assertNotIn('TESte', text)
