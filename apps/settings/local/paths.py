# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os


__all__ = ('BASE_DIR', 'PROJECT_DIR', )


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
