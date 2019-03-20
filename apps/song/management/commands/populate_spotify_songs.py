from __future__ import absolute_import

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from spotify.api import spotify_request


class Command(BaseCommand):

    def handle(self, **options):
        tracks = spotify_request.search(q='weezer', limit=20)
        tracks.create_models()
