"""Encapsulates all serialiser instances."""

from rest_framework import fields as rest_field
from rest_framework import relations
from rest_framework import serializers

import collections


class ErrorSerializer(serializers.Serializer):
    """Representation of any errors."""
    error_code = serializers.IntegerField()
    error_message = serializers.CharField(max_length=200)


class LatLongSerializer(serializers.Serializer):
    """Instance of this class serialies the latitude, longitude and errors"""
    latitude = serializers.DecimalField(max_digits=8, decimal_places=5)
    longitude = serializers.DecimalField(max_digits=8, decimal_places=5)
    errors = ErrorSerializer(required=False, many=True)

    def to_representation(self, instance):
        """Removes empty data structures."""
        ret = collections.OrderedDict()
        readable_fields = self._readable_fields

        for field in readable_fields:
            try:
                attribute = field.get_attribute(instance)
            except rest_field.SkipField:
                continue

            if attribute in [None, '', [], {}, ()]:
                continue
            check_for_none = attribute.pk if isinstance(
                attribute, relations.PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret
