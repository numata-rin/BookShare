"""
プロジェクト用ルーティングファイル。URLをパターンマッチングして処理経路を制御する役割を担い、
「URLディスパッチャー」とも呼ばれる。（ファイル名は"URLconf"とも記述される）
一般的にはアプリケーションごとにそれぞれのディレクトリ別途urls.pyを作成して処理を移譲する。

Djangoはurlspatternsというリストを順番にチェックしてpath関数の第1引数とURLをパターンマッチングしている。
パターンが一致すればpath関数の第2引数の処理を行う。
URLとのパターンマッチングは、ホスト名のあとの部分をチェックして、第2引数にあるinclude関数がある場合は、
include関数の引数に指定しているアプリのurls.pyに処理を移譲している。
"""


from django.contrib import admin
from django.contrib.staticfiles.urls import static
# 設定ディレクトリのurls.pyから各アプリのurls.pyに処理を渡す命令を書くためのincludeをimport
from django.urls import path, include

from . import settings_common, settings_dev

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bookshare.urls')),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(
  settings_common.MEDIA_URL,
  document_root = settings_dev.MEDIA_ROOT
)
