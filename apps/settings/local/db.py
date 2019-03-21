# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
from .paths import PROJECT_DIR


__all__ = ('DATABASES', )


MYSQL_CONFIG = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'comp_community',
    'USER': 'root',
    'PASSWORD': '',
    'HOST': 'localhost',
    'PORT': '3306',
}

SQLITE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'comp_community.db',
    # 'NAME': os.path.join(PROJECT_DIR, 'comp_community.db'),
}

# MySQL is being a pain in the ass working with Pytohn3.7, it is having trouble
# finding the mysql_config file, which is in /usr/local/.  For now, we are just
# going to use sqlite.db until we decide to go with PostGreSQL or MySQL.
DATABASES = {
    'default': SQLITE
}
