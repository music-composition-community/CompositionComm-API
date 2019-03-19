# -*- coding: utf-8 -*-
from __future__ import absolute_import


__all__ = ('DATABASES', )


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    },
}
