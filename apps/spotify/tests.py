# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.test import TestCase


class TestRun(TestCase):
    def test_get_music(self):
        client = docker.from_env()
        print client

