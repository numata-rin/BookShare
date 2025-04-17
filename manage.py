# このファイルはDjangoプロジェクトにおいてとても重要なコマンドツールであり、プロジェクトの開発・管理を行うための
# エントリーポイントのような役割を持つファイルである。
# 具体的な役割としては、
#
#「Djangoの管理コマンドを実行する」
# =>runserverやmigrate, createsuperuserなどのコマンドをこのファイル経由で実行する。
# 
# 「設定ファイルを読みこむ」
# =>DJANGO_SETTINGS_MODULEを指定して、プロジェクトの設定(settings.py)を読み込む。
# 
# 「プロジェクトのルートとして動作する」
# =>コマンドを実行するときのカレントディレクトリ基準になるため、プロジェクトの起点として機能する。
# 
# 
# 
# 
# #

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
