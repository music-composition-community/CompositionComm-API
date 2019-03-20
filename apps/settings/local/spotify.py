# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .secret_keys import SPOTIFY_CLIENT_SECRET

__all__ = ('SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT', )


SPOTIFY_CLIENT_ID = "30c8c44d821244958754abde5f12abe4"
SPOTIFY_REDIRECT_URI = "https://developer.spotify.com/documentation"

# TODO: DO NOT PUSH UP TO GIT UNTIL THIS IS ENCRYPTED
SPOTIFY_CLIENT = {
    'id': SPOTIFY_CLIENT_ID,
    'secret': SPOTIFY_CLIENT_SECRET,
}

SPOTIFY_API_URL = "https://api.spotify.com/v1"
