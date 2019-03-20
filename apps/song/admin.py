# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib import admin

from song.models import Song

admin.site.register(Song)
