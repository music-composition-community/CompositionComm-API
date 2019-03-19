# -*- coding: utf-8 -*-
from __future__ import absolute_import


__all__ = ('DATABASES', )


DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}
