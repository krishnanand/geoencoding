from django.conf.urls import url
from encoding import viewset
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = format_suffix_patterns([
    url(r'^encoding/lat_long/$',
        viewset.GeocodingViewSet.as_view({'get': 'get_lat_long'}),
        name='lat_long'),
])
