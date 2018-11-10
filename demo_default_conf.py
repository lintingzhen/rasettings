#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Create Date: 2018-11-10 19:03
# Author: Airlam

import yaml

default_settings = """
mysql:
    host: 127.0.0.1
    auth:
        user: admin
"""


def define_default_settings():
    from rasettings import define_default
    define_default(yaml.load(default_settings))
