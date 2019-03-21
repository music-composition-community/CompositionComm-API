# -*- coding: utf-8 -*-
from __future__ import absolute_import

from dacite import from_dict
from dataclasses import dataclass
from typing import List, Optional

from django.utils.text import slugify

from song.models import Song


__all__ = ('SpotifyTracks', 'SpotifyTrack', )


@dataclass
class CompDataClass:

    @classmethod
    def from_dict(cls, data):
        return from_dict(data_class=cls, data=data)


@dataclass
class SpotifyImage(CompDataClass):
    url: str
    width: int
    height: int

    def __repr__(self):
        return f'Spotify Image: {self.url}'

    def __str__(self):
        return f'Spotify Image: {self.url}'


@dataclass
class SpotifyItem(CompDataClass):
    id: str
    name: str
    uri: str
    href: str
    external_urls: dict


@dataclass
class SpotifyArtist(SpotifyItem):

    type: str = 'artist'

    def __repr__(self):
        return f'Spotify Artist: {self.name}'

    def __str__(self):
        return f'Spotify Artist: {self.name}'


@dataclass
class SpotifyAlbum(SpotifyItem):

    release_date: str
    release_date_precision: str

    artists: List[SpotifyArtist]
    images: List[SpotifyImage]
    available_markets: List[str]

    album_type: str = 'album'
    type: str = 'album'
    total_tracks: int = 0

    def __repr__(self):
        return f'Spotify Album: {self.name}, {self.artists[0].name}'

    def __str__(self):
        return f'Spotify Album: {self.name}, {self.artists[0].name}'


@dataclass
class SpotifyTrack(SpotifyItem):

    preview_url: Optional[str]
    external_ids: dict

    album: SpotifyAlbum
    artists: List[SpotifyArtist]
    available_markets: List[str]

    type: str = 'track'
    track_number: int = 0
    disc_number: int = 0
    explicit: bool = False
    duration_ms: int = 0
    is_local: bool = False
    popularity: int = 0

    class Meta:
        model_fields = ()

    def create_models(self):
        song = Song(
            title=self.name,
            duration_ms=self.duration_ms,
            slug=slugify(self.name)
        )
        song.save()

    def __repr__(self):
        return f'Spotify Track: {self.name}'

    def __str__(self):
        return f'Spotify Track: {self.name}'


@dataclass
class SpotifyTracks(CompDataClass):
    items: List[SpotifyTrack]

    def create_models(self):
        for item in self.items:
            item.create_models()

    @property
    def count(self):
        return len(self.items)

    def __repr__(self):
        return f'Spotify Tracks: {self.count}'

    def __str__(self):
        return f'Spotify Tracks: {self.count}'
