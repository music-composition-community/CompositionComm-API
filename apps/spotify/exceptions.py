# -*- coding: utf-8 -*-
from __future__ import absolute_import


__all__ = ('SpotifyApiException', 'SpotifyApiNotFound')


class SpotifyException(Exception):
    pass


class SpotifyApiException(SpotifyException):
    pass


class SpotifyApiNotFound(SpotifyException):
    def __init__(self, param):
        self.message = "Did not find results for %s." % param

    def __str__(self):
        return self.message


class SpotifyApiClientException(SpotifyApiException):
    pass


class SpotifyApiServerException(SpotifyApiException):
    pass
