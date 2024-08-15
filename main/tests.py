from django.test import TestCase, Client
from django.urls import reverse
from .models import LinkMapping

class TestModels(TestCase):
    def setUp(self):
        self.originalUrl = 'https://www.assetcare.nl'
        self.shortcode = 'asc123'

    def test_model_LinkMapping(self):
        link_map = LinkMapping.objects.create(
            originalUrl = self.originalUrl,
            shortcode = self.shortcode
        )

        self.assertTrue(isinstance(link_map, LinkMapping))

class TestViews(TestCase):
    def setUp(self):
        self.url = 'https://www.assetcare.nl'
        self.shortcode = 'asc123'
        self.client = Client()
        self.index_url = reverse('index')
        self.shorten_url = reverse('shorten_post')
        self.shortcode_request = reverse('handle_shortcode_request')
    
    def test_index(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')

    def test_shorten_request_POST(self):
        response = self.client.post(self.shorten_url, {'url': self.url, 'shortcode': self.shortcode})

        self.assertEqual(response.status_code, 201)

    def test_shorten_request_invalid_code_POST(self):
        response1 = self.client.post(self.shorten_url, {'url': self.url, 'shortcode': '12345'})
        response2 = self.client.post(self.shorten_url, {'url': 'https://www.job1.nl', 'shortcode': '1234567'})
        response3 = self.client.post(self.shorten_url, {'url': 'https://www.job2.nl', 'shortcode': '12345#'})

        self.assertEqual(response1.status_code, 412)
        self.assertEqual(response2.status_code, 412)
        self.assertEqual(response3.status_code, 412)
        

    def test_url_not_present_POST(self):
        response = self.client.post(self.shorten_url, {'url': '', 'shortcode': self.shortcode})

        self.assertEqual(response.status_code, 400)

    def test_shortcode_already_used_POST(self):
        response1 = self.client.post(self.shorten_url, {'url': self.url, 'shortcode': self.shortcode})
        response2 = self.client.post(self.shorten_url, {'url': self.url, 'shortcode': self.shortcode})
        response3 = self.client.post(self.shorten_url, {'url': 'https://www.google.com', 'shortcode': self.shortcode})

        self.assertEqual(response2.status_code, 409)
        self.assertEqual(response3.status_code, 409)

    def test_no_shortcode_provided_POST(self):
        response = self.client.post(self.shorten_url, {'url': self.url, 'shortcode': ''})

        self.assertEqual(response.status_code, 201)
        print(f'type content: {type(response.content.decode("utf-8"))}')
        print(f'content: {response.content.decode("utf-8")}')
        self.assertRegex(response.content.decode("utf-8"), r'shortcode: [\w]{6} ')

    def test_redirect_GET(self):
        LinkMapping.objects.create(originalUrl=self.url, shortcode=self.shortcode)
        response_correct = self.client.get(self.shortcode_request, {'shortcode': self.shortcode, 'request_type': 'redirect'})
        response_incorrect = self.client.get(self.shortcode_request, {'shortcode': '123456', 'request_type': 'redirect'})

        self.assertEqual(response_correct.status_code, 302)
        self.assertEqual(response_correct.url, self.url)
        self.assertEqual(response_incorrect.status_code, 404)

    def test_stats_GET(self):
        LinkMapping.objects.create(originalUrl=self.url, shortcode=self.shortcode)
        response_correct = self.client.get(self.shortcode_request, {'shortcode': self.shortcode, 'request_type': 'stats'})
        response_incorrect = self.client.get(self.shortcode_request, {'shortcode': '123456', 'request_type': 'stats'})

        self.assertEqual(response_correct.status_code, 200)
        self.assertEqual(response_incorrect.status_code, 404)

    def test_redirect_stats_update(self):
        response_create = self.client.post(self.shorten_url, {'url': self.url, 'shortcode': self.shortcode})
        response_redirect_1 = self.client.get(self.shortcode_request, {'shortcode': self.shortcode, 'request_type': 'redirect'})
        redirect_count_1 = LinkMapping.objects.get(shortcode=self.shortcode).redirectCount
        response_redirect_2 = self.client.get(self.shortcode_request, {'shortcode': self.shortcode, 'request_type': 'redirect'})
        redirect_count_2 = LinkMapping.objects.get(shortcode=self.shortcode).redirectCount
        response_redirect_3 = self.client.get(reverse('redirect_from_url', args=[self.shortcode]))
        redirect_count_3 = LinkMapping.objects.get(shortcode=self.shortcode).redirectCount

        self.assertEqual(redirect_count_2 - redirect_count_1, 1)
        self.assertEqual(redirect_count_3 - redirect_count_2, 1)