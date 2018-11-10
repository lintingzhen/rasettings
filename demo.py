#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Create Date: 2018-11-10 19:04
# Author: Airlam

from demo_default_conf import define_default_settings
from rasettings import settings, parse_command_line, parse_config_file


def main():
    # 加载默认配置
    define_default_settings()

    # 读取命令行配置
    parse_command_line()

    # 读取实际配置
    parse_config_file('demo_prod.yaml')

    print settings.mysql
    # 输出：
    # RASettings: {'host': '127.0.0.1', 'auth': {'user': 'xxx'}}

    print settings.mysql.auth
    # 输出：
    # RASettings: {'user': 'xxx'}

    print settings.mysql.auth.user
    # 输出：
    # xxx

    settings.mysql = {"auth": {"user": "yyy"}}
    print settings.get_setting("mysql.auth")
    # 输出：
    # {'user': 'zzz'}

    settings.mysql = {"auth.user": "zzz"}
    print settings.get_setting("mysql.auth")
    # 输出：
    # {'user': 'zzz'}

    print settings.mysql.auth.to_dict()
    # 输出：
    # {'user': 'zzz'}


if __name__ == '__main__':
    main()
