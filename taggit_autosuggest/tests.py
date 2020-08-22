import json

from django.shortcuts import reverse
from django.test import TestCase, override_settings

from taggit.models import Tag


class TaggitAutoSuggestTests(TestCase):

    def setUp(self):
        Tag.objects.create(name='test 1')
        Tag.objects.create(name='test 2')
        Tag.objects.create(name='not found 3')

    def test_default_view(self):

        base_url = reverse('taggit_autosuggest-list', args=['taggit.Tag'])

        resp = self.client.get('{}?q=test'.format(base_url))
        self.assertEqual(2, len(json.loads(resp.content)))

        resp = self.client.get('{}?q=rock'.format(base_url))
        self.assertEqual(0, len(json.loads(resp.content)))

        resp = self.client.get('{}?q=t'.format(base_url))
        self.assertEqual(3, len(json.loads(resp.content)))

        resp = self.client.get('{}'.format(base_url))
        self.assertEqual(0, len(json.loads(resp.content)))

    def test_default_view_with_invalid_model(self):

        base_url = reverse('taggit_autosuggest-list', args=['people.Person'])

        with self.assertRaises(LookupError):
            self.client.get('{}?q=test'.format(base_url))

    @override_settings(
        TAGGIT_AUTOSUGGEST_MAX_SUGGESTIONS=1,
    )
    def test_max_suggestions(self):

        base_url = reverse('taggit_autosuggest-list', args=['taggit.Tag'])

        resp = self.client.get('{}?q=test'.format(base_url))
        self.assertEqual(1, len(json.loads(resp.content)))

        resp = self.client.get('{}?q=t'.format(base_url))
        self.assertEqual(1, len(json.loads(resp.content)))

    def test_limit(self):

        base_url = reverse('taggit_autosuggest-list', args=['taggit.Tag'])

        resp = self.client.get('{}?q=test&limit=1'.format(base_url))
        self.assertEqual(1, len(json.loads(resp.content)))

        resp = self.client.get('{}?q=t&limit=2'.format(base_url))
        self.assertEqual(2, len(json.loads(resp.content)))

        resp = self.client.get('{}?q=t&limit=1'.format(base_url))
        self.assertEqual(1, len(json.loads(resp.content)))

    @override_settings(
        TAGGIT_AUTOSUGGEST_MODELS=['test.Test']
    )
    def test_tag_models_invalid_selection(self):

        base_url = reverse('taggit_autosuggest-list', args=['taggit.Tag'])

        with self.assertRaises(LookupError):
            self.client.get('{}?q=test'.format(base_url))
