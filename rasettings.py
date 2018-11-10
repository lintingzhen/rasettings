#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Create Date: 2018-11-10 11:05
# Author: Airlam

import yaml
import argparse


class RASettings(object):
    """
    具体见README.MD
    """
    def __init__(self):
        super(RASettings, self).__init__()
        self.__dict__['_settings'] = {}

    def define(self, d):
        s = self._settings
        s.clear()
        for k, v in d.iteritems():
            if isinstance(v, dict):
                s[k] = _Option(RASettings().define(v), RASettings)
            else:
                s[k] = _Option(v, type(v))

        return self

    def __contains__(self, name):
        names = name.split('.')
        ss = self
        while names:
            name = names. pop(0)
            if not isinstance(ss, RASettings):
                return False
            if name not in ss._settings:
                return False

            ss = ss._settings[name].value

        return True

    def __repr__(self):
        return "RASettings: {}".format(self.to_dict())

    def set_dict(self, d):
        for k, v in d.iteritems():
            self.__setattr__(k, v)

    def to_dict(self):
        r = {}
        for k, v in self._settings.iteritems():
            if v.is_settings():
                r[k] = v.value.to_dict()
            else:
                r[k] = v.value
        return r

    def get_setting(self, name):
        names = name.split('.')
        ss = self
        while names:
            name = names.pop(0)
            if not name:
                raise Exception('exceptional key: {}'.format(name))

            if not isinstance(ss, RASettings):
                raise AttributeError('exceptional key: {}'.format(name))

            if name not in ss._settings:
                raise AttributeError('exceptional key: {}'.format(name))

            ss = ss._settings[name]
            if ss.is_settings():
                ss = ss.value

        if isinstance(ss, _Option):
            return ss.value
        else:  # Settings
            return ss.to_dict()

    def __getattr__(self, name):
        if name in self._settings:
            return self._settings[name].value
        raise AttributeError('exceptional key: {}'.format(name))

    def __setattr__(self, name, value):
        if isinstance(name, (str, unicode)):
            names = name.split('.')
        else:
            raise AttributeError('exceptional key: {}'.format(name))

        ss = self
        while names:
            name = names.pop(0)
            if not name:
                raise Exception('exceptional key: {}'.format(name))

            if not isinstance(ss, RASettings):
                raise AttributeError('exceptional key: {}'.format(name))

            if name not in ss._settings:
                raise AttributeError('exceptional key: {}'.format(name))

            ss = ss._settings[name]
            if ss.is_settings():
                ss = ss.value

        if isinstance(ss, RASettings):
            if isinstance(value, dict):
                ss.set_dict(value)
            else:
                raise AttributeError('exceptional value for key {}'.format(name))
        elif isinstance(ss, _Option):
            if isinstance(value, ss.type):
                ss.value = value
            else:
                raise AttributeError('exceptional value for key {}'.format(name))
        else:
            raise AttributeError('exceptional value for key {}'.format(name))

    def build_argument_parser(self, parser):
        for k, v in self._settings.iteritems():
            if v.is_settings():
                pass
            else:
                type_func = (lambda s: s.lower() not in ('false', 'f')) if v.type == bool else v.type
                parser.add_argument('--{}'.format(k), action='store', default=v.default, type=type_func)
        return parser


class _Option(object):

    def __init__(self, default, _type, value=None):
        super(_Option, self).__init__()
        self.default = default
        self.type = _type
        self.value = default if value is None else value

    def is_settings(self):
        return self.type == RASettings


settings = RASettings()


def define_default(d):
    settings.define(d)


def parse_command_line(args=None):
    """
    识别命令行中的参数，目前命令行中只能设置一级配置
    :param args:
    :return: None
    """
    parser = argparse.ArgumentParser()
    settings.build_argument_parser(parser)
    if args is None:
        import sys
        args = sys.argv[1:]

    conf = parser.parse_args(args)
    settings.set_dict(conf.__dict__)


def parse_config_file(path):
    with open(path, 'r') as f:
        c = yaml.load(f)
        settings.set_dict(c)
