"""Encapsulates all classes that handle geocoding responses."""

import requests

from encoding import api_keys
from encoding import constants
from encoding import models

_NO_DATA_FOUND = 'No Data Found'


def create_error(error_code, error_message):
    """Creates an error representation for the latitude and longitude object."""
    lat_long = models.LatitudeLongitude()
    lat_long.add_error(error_code, error_message)
    return lat_long


class BaseService(object):
    """Super class that exposes helper methods to make http requests."""

    def prepare_request(self, **kwargs):
        """Returns the request entity used to make the the requests."""
        raise NotImplementedError('Need to be implemented by the subclass')

    def process_payload(self, payload):
        """Returns the instances to be serialised to be serialised."""
        raise NotImplementedError('Need to be implemented by the subclass')

    def make_request(self, **kwargs):
        """Makes http request to geocoding services and process the payloads."""
        if 'address' not in kwargs:
            lat_long = models.LatitudeLongitude()
            lat_long.add_error(400, constants.MISSING_QUERY_PARAM)
            return lat_long
        r = self.prepare_request(**kwargs)
        return self.process_payload(r.json())


class HereEncodingService(BaseService):
    """Responsible for returning the latitude and longitude using Here APIs."""

    def prepare_request(self, **kwargs):
        url = 'https://geocoder.api.here.com/6.2/geocode.json'
        a_dict = {'app_id': api_keys.HERE_APP_ID,
                  'app_code': api_keys.HERE_APP_CODE}
        a_dict['searchtext'] = kwargs.pop('address')
        return requests.get(url, params=a_dict)

    def process_payload(self, json_object):
        """Returns the instance of the LatitudeLongitude instance."""
        response_object = json_object.get('Response', {})
        view_object_list = response_object.get('View', [])
        result_object_list = view_object_list[0].get('Result', [])
        location = result_object_list[0].get('Location', {})
        navigation_position_list = location.get('NavigationPosition', [])
        return models.LatitudeLongitude(
            navigation_position_list[0].get('Latitude'),
            navigation_position_list[0].get('Longitude'))


class GoogleMapGeocoding(BaseService):
    """Helper class to query Google Maps API."""

    def prepare_request(self, **kwargs):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        a_dict = {'key': api_keys.GOOGLE_APP_KEY}
        a_dict['address'] = kwargs.pop('address')
        return requests.get(url, params=a_dict)

    def process_payload(self, json_object):
        result_object_list = json_object.get('results', [])
        geometry = result_object_list[0].get('geometry', {})
        location = geometry.get('location', {})
        return models.LatitudeLongitude(
            location.get('lat'), location.get('lng'))


def fetch_geocoding_information(**kwargs):
    """Returns the geocoding information from either the geocoding services."""
    all_services = [GoogleMapGeocoding(), HereEncodingService()]
    lat_long = None
    for service in all_services:
        lat_long = service.make_request(**kwargs)
        if lat_long and not lat_long.errors:
            return lat_long
    lat_long = models.LatitudeLongitude()
    lat_long.add_error(400, _NO_DATA_FOUND)
    return lat_long
