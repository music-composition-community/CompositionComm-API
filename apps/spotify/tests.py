# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.test import TestCase

from spotify.api import spotify_request


class TestRun(TestCase):
    def test_get_music(self):
        results = spotify_request.search(q='weezer', limit=20)
        results.create_models()
