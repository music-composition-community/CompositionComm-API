# -*- coding: utf-8 -*-
from __future__ import absolute_import

import base64
from oauthlib.oauth2 import BackendApplicationClient
import os
import requests
import six

from django.conf import settings

from lib.utils import default_singleton

from spotify.exceptions import (SpotifyApiException, SpotifyApiNotFound,
    SpotifyApiClientException, SpotifyApiServerException)
from spotify.data_models import SpotifyTracks, SpotifyArtist


class SpotifyEndpointsMixin(object):

    @classmethod
    def _get_from_settings(cls, *args):
        params = []
        for arg in args:
            if not getattr(settings, arg, None):
                raise SpotifyApiException("%s not in settings." % arg)
            params.append(getattr(settings, arg))
        return default_singleton(params)

    @classmethod
    def path_join(cls, *args):
        """
        Convenience method.
        Joins components of paths to server_url where they don't all necessarily
        have to be non-null values.
        """
        path_params = [cls.server_url()]
        path_params.extend([arg for arg in args if arg is not None])
        return os.path.join(*tuple(path_params))

    @classmethod
    def server_url(cls):
        return cls._get_from_settings('SPOTIFY_API_URL')

    @classmethod
    def auth_endpoint(cls):
        """
        Endpoint for authenticating user accounts with OAUTH2.  Not currently
        using.
        """
        return os.path.join(cls.spotify_api_endpoint(), 'authorize')

    @classmethod
    def token_endpoint(cls):
        return cls._get_from_settings('SPOTIFY_TOKEN_URL')

    @classmethod
    def artists_endpoint(cls, id=None, extension=None):
        return cls.path_join('artists', id, extension)


class SpotifyAuth(BackendApplicationClient, SpotifyEndpointsMixin):
    """
    TODO:
    -----
    Build in expired token/refresh token capability.
    Shamelessly stolen from https://github.com/plamere/spotipy
    """
    proxies = None
    payload = {'grant_type': 'client_credentials'}

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def _get_auth_headers(self):
        client = self.client_id + ':' + self.client_secret
        auth_header = base64.b64encode(six.text_type(client).encode('ascii'))
        return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

    def get_token_info(self):

        response = requests.post(
            self.token_endpoint(),
            data=self.payload,
            headers=self._get_auth_headers(),
            verify=True,
            proxies=self.proxies
        )

        if response.status_code != 200:
            raise SpotifyApiException(response.reason)
        return response.json()

    def get_token(self):
        info = self.get_token_info()
        return info['access_token']

    def __call__(self, req):
        req.headers['Authorization'] = "Bearer %s" % self.get_token()
        return req


class spotify_request(SpotifyEndpointsMixin):

    @classmethod
    def auth(cls):
        client_id, client_secret = cls._get_from_settings(
            'SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET')
        return SpotifyAuth(client_id, client_secret)

    @classmethod
    def _format_response(cls, response, data_class):
        """
        TODO:
        -----
        Might want to build in KeyError exceptions here and ValueError exceptions
        for the response.json() portion.
        """
        data = response.json()
        if "%ss" % data_class.type not in data:
            return data_class.from_dict(data)

        results = data["%ss" % data_class.type]
        if len(results) == 0:
            raise SpotifyApiNotFound(data_class.type)
        return [data_class.from_dict(result) for result in results]

    @classmethod
    def _handle_response(cls, response, data_class):
        try:
            response.raise_for_status()
        except requests.RequestException:
            if response.status_code >= 400 and response.status_code < 500:
                raise SpotifyApiClientException(response.reason)
            else:
                raise SpotifyApiServerException(response.status_code)
        else:
            return cls._format_response(response, data_class)

    @classmethod
    def get(cls, endpoint, data_class, **params):
        auth = cls.auth()
        resp = requests.get(endpoint, params=params, auth=auth)
        return cls._handle_response(resp, data_class)

    @classmethod
    def get_artist(cls, id, extension=None):
        """
        Endpoints for retrieving information about one or more artists from the
        Spotify catalog.

        extension:
            (1) albums
            (2) top-tracks
            (3) related-artists
        """
        endpoint = cls.artists_endpoint(id=id, extension=extension)
        return cls.get(endpoint, SpotifyArtist)

    @classmethod
    def get_artists(cls, ids):
        endpoint = cls.artists_endpoint()
        return cls.get(endpoint, SpotifyArtist, ids=ids)


# class spotipy_request(SpotifyEndpointsMixin):

#     @classmethod
#     def _handle_results(cls, results, data_class, key=None):
#         results = results[key or "%ss" % data_class.type]['items']
#         if len(results) == 0:
#             raise SpotifyApiNotFound(data_class.type)
#         return [data_class.from_dict(result) for result in results]

#     @classmethod
#     def _handle_result(cls, results, data_class, key=None):
#         results = results[key or "%ss" % data_class.type]['items']
#         if len(results) == 0:
#             raise SpotifyApiNotFound(data_class.type)
#         return data_class.from_dict(results[0])

#     @classmethod
#     def search(cls, query, data_class, key=None, limit=20):
#         results = cls.request().search(
#             q='%s:%s' % (data_class.type, query),
#             limit=limit,
#             type=data_class.type,
#         )

#         if limit != 1:
#             return cls._handle_results(results, data_class, key=key)
#         return cls._handle_result(results, data_class, key=key)

#     @classmethod
#     def search_for_artist(cls, query):
#         """
#         The only way to retrieve information for a concrete artist is to request
#         the artist by ID, URL or URI.  If we want to reference the artist by
#         name, than we need to perform a more general search.

#         Since we have to perform these queries by searching, we are going to make
#         sure that the lowercase version of the searched name equals the lowercase
#         version of the first result, since we have to assume the first result
#         is the correct one.
#         """
#         artist = cls.search(query, SpotifyArtist, limit=1)
#         if artist.name.lower() != query.lower():
#             raise SpotifyApiNotFound(SpotifyArtist.type)
#         return artist

#     @classmethod
#     def get_artist(cls, id):
#         result = cls.request().artist(id)
#         return from_dict(data_class=SpotifyArtist, data=result)

#     @classmethod
#     def get_top_tracks(cls, artist_id=None, artist_name=None, artist=None, country='US'):
#         """
#         Get Spotify catalog information about an artist’s top 10 tracks by country.
#         """
#         artist_id = artist.id if artist else artist_id
#         if not artist_id and artist_name:
#             artist = cls.search_for_artist(artist_name)
#             artist_id = artist.id
#         else:
#             raise SpotifyApiException(
#                 "Must provide `artist_id`, `artist_name` or `artist`.")

#         results = cls.request().artist_top_tracks(artist_id, country=country)
#         return cls._handle_results(results, SpotifyTracks)
