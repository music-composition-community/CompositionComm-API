# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.test import TestCase

from spotify.api import spotify_request


class TestRun(TestCase):

    def test_search_for_artist(self):
        artists = spotify_request.get_artist('0oSGxfWSnnOXhD2fKuz2Gy')
        print(artists)
        artists = spotify_request.get_artist('0oSGxfWSnnOXhD2fKuz2Gy', extension='related-artists')
        print(artists)
