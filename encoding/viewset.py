"""Encapsulates all viewsets configured to handle incoming http requests."""

from rest_framework import viewsets
from rest_framework import response
from rest_framework import status

from encoding import constants
from encoding import http_helper as helper
from encoding import serializers


class GeocodingViewSet(viewsets.GenericViewSet):
    """Returns the encoding latitude and longitude for a query parameter."""
    serializer_class = serializers.LatLongSerializer

    def get_queryset(self):
        """Query set is not required."""
        return None

    def get_lat_long(self, request, *args, **kwargs):
        lat_long = None
        if 'address' not in request.query_params:
            lat_long = helper.create_error(400, constants.MISSING_QUERY_PARAM)
        else:
            lat_long = helper.fetch_geocoding_information(
                **request.query_params)
        serialized_data = self.get_serializer_class()(lat_long)
        return response.Response(
                serialized_data.data,
                (status.HTTP_200_OK
                 if lat_long.is_valid() else status.HTTP_400_BAD_REQUEST))
