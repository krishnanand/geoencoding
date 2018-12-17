"""Unit test for http helper."""

from encoding import http_helper
from encoding import models
from django import test as django_test

import vcr


class HereEncodingServiceTest(django_test.TestCase):

    def setUp(self):
        self.here_encoding_service = http_helper.HereEncodingService()

    def tearDown(self):
        self.here_encoding_service = None

    @vcr.use_cassette('encoding/tests/test_data/vcr_cassettes/here_response')
    def test_make_request(self):
        latitude_longitude = self.here_encoding_service.make_request(
            address='1600+Amphitheatre+Parkway+Mountain+View')
        assert latitude_longitude == (
            models.LatitudeLongitude(latitude=37.42307, longitude=-122.08414))


class GoogleMapsServiceTest(django_test.TestCase):

    def setUp(self):
        self.google_maps_service = http_helper.GoogleMapGeocoding()

    def tearDown(self):
        self.google_maps_service = None

    @vcr.use_cassette('encoding/tests/test_data/vcr_cassettes/google_response')
    def test_make_request(self):
        latitude_longitude = self.google_maps_service.make_request(
            address='1600+Amphitheatre+Parkway+Mountain+View')
        assert latitude_longitude == (
            models.LatitudeLongitude(
                latitude=37.4261881, longitude=-122.0761534))


@vcr.use_cassette(
    'encoding/tests/test_data/vcr_cassettes/fetch_geocoding_response')
def test_fetch_geocoding_information__success():
    lat_long = http_helper.fetch_geocoding_information(
        address='1600+Amphitheatre+Parkway+Mountain+View')
    assert lat_long == (
        models.LatitudeLongitude(
            latitude=37.4261881, longitude=-122.0761534))


def test_fetch_geocoding_information__failure():
    lat_long_error = http_helper.fetch_geocoding_information()
    lat_long_expected = models.LatitudeLongitude()
    lat_long_expected.add_error(400, http_helper._NO_DATA_FOUND)
    assert lat_long_error == lat_long_expected
