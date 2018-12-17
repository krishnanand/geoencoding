"""Encapsulates all the models used to represent the state."""


class Error(object):
    """Encapsulates the error messages to be returned"""
    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message

    def __repr__(self):
        return '{}[{}]'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return (self.error_code == other.error_code and
                self.error_message == other.error_message)


class LatitudeLongitude(object):
    """Encapsulates the latitude and longitude information."""
    def __init__(self, latitude=None, longitude=None):
        self.latitude = latitude
        self.longitude = longitude
        self.errors = []

    def add_error(self, error_code, error_message):
        self.errors.append(Error(error_code, error_message))

    def is_valid(self):
        return not self.errors

    def __repr__(self):
        return '{}[{}]'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return (self.latitude == other.latitude and
                self.longitude == other.longitude and
                self.errors == other.errors)
