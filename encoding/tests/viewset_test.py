from rest_framework import test

from django import urls

import vcr


class ViewSetTest(test.APITestCase):

    def setUp(self):
        self.lat_long_url = urls.reverse('lat_long')

    def test_get_lat_long__missing_query_parameter(self):
        response = self.client.get(self.lat_long_url)
        assert response.json() == (
            {'errors': [{'error_code': 400,
             'error_message': "'Address' query parameter is missing"}]})

    @vcr.use_cassette('encoding/tests/test_data/vcr_cassettes/viewset_response')
    def test_get_lat_long__success(self):
        response = self.client.get(
            '{}?address=1600+Amphitheatre+Parkway+Mountain+View'.format(
                self.lat_long_url))
        assert response.json() == {
             'latitude': '37.42619',
             'longitude': '-122.07615'
        }
