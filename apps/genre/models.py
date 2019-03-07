# -*- coding: utf-8 -*-
from __future__ import absolute_import


from django.db import models


class Genre(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'genre'

    def __str__(self):
        return "<Genre %s>" % self.slug
