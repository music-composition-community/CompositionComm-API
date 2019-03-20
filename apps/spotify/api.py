# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import requests

from django.conf import settings

from dacite import from_dict
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from lib.utils import default_singleton
from spotify.exceptions import SpotifyApiException
from spotify.data_models import SpotifyTracks


class spotify_endpoints(object):

    @classmethod
    def spotify_api_endpoint(cls):
        return cls._get_from_settings('SPOTIFY_API_URL')

    @classmethod
    def auth_endpoint(cls):
        return os.path.join(cls.spotify_api_endpoint(), 'authorize')


class spotify_request(spotify_endpoints):

    @classmethod
    def _get_from_settings(cls, *args):
        params = []
        for arg in args:
            if not getattr(settings, arg, None):
                raise SpotifyApiException("%s not in settings." % arg)
            params.append(getattr(settings, arg))
        return default_singleton(params)

    @classmethod
    def credentials(cls):
        client_id, client_secret = cls._get_from_settings(
            'SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET')

        return SpotifyClientCredentials(client_id, client_secret)

    @classmethod
    def get(cls, endpoint, **params):
        response = requests.get(endpoint, params=params)
        return cls._handle_response(response)

    @classmethod
    def get_token(cls):
        auth = cls.credentials()
        return auth.get_access_token()

    @classmethod
    def authorize(cls, endpoint, **params):
        endpoint = cls.auth_endpoint()
        client_id = cls._get_from_settings('SPOTIFY_CLIENT_ID')
        return cls.get(endpoint, client_id=client_id, response_type='token')

    @classmethod
    def _handle_response(cls, response):
        return response

    @classmethod
    def search(cls, **kwargs):
        token = cls.get_token()
        results = spotipy.Spotify(auth=token).search(q='weezer', limit=20)
        tracks = results['tracks']
        return from_dict(data_class=SpotifyTracks, data=tracks)
