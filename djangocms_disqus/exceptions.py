# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class DisqusAPIError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
