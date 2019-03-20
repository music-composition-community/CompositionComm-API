# -*- coding: utf-8 -*-
from __future__ import absolute_import

from collections import Iterable


__all__ = ('default_singleton', 'ensure_iterable', )


def default_singleton(array, map_to=None):
    if isinstance(array, Iterable) and len(array) == 1:
        return array[0]
    if map_to:
        return map_to(array)
    return array


def ensure_iterable(array, map_to=tuple):
    if isinstance(array, Iterable):
        return array
    return map_to(array)
