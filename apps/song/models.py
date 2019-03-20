# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    duration_ms = models.IntegerField()

    class Meta:
        db_table = 'songs'

    def __str__(self):
        return "<Song %s>" % self.title
