# -*- coding: utf-8 -*-
from __future__ import absolute_import


__all__ = ('DATABASES', )


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'comp_community',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    },
}
