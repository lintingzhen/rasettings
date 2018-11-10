random access settings
任意访问配置类，读取yaml格式配置定义默认配置，并可在后期加载当前环境用到的具体配置。

## feature list
- 读取yaml配置，设置默认配置
- 读取yaml配置，设置当前配置，配置项为默认配置项子集，且受默认配置的值类型约束
- 通过用'.'连接的相邻多级key字符串读写配置
- 读取命令行修改一级配置
- 暂不支持列表
- 暂不支持修改默认配置

## demo
```
# file: demo_default_conf.py，存放默认配置，并初始化
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
```

```
# file: demo_prod.yaml，存放实际配置
mysql.auth.user: xxx
```

```
# file: demo.py，示例程序
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
```

