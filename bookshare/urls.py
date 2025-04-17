"""ファイルの概要

アプリのurls.pyではURLとビューとのマッピングを行う。このurls.pyは開発者が作成する。
path関数の第1関数では設定ファイルのurls.pyでマッチング判断したURL以降の部分のURLがマッチング対象となる。
第2引数ではマッピングされるビューを記述して、第3引数ではキーワード引数を設定して逆引きするときに使う。

"""

from django.urls import path

from . import views

app_name = 'bookshare'
urlpatterns = [
  path('', views.IndexView.as_view(), name="index"),
  path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
  path('book-list/', views.BookListView.as_view(), name="book_list"),
  path('book-detail/<int:pk>/', views.BookDetailView.as_view(), name="book_detail"),
  path('book-create/', views.BookCreateView.as_view(), name="book_create"),
  path('book-update/<int:pk>/', views.BookUpdateView.as_view(), name="book_update"),
  path('book-delete/<int:pk>/', views.BookDeleteView.as_view(), name="book_delete"),
]

"""補足・個人用メモ

・as_view()メソッドを使う理由
Djangoのpath()関数は基本的に関数を受け取る仕組みであり、クラスベースビューはクラスそのものだからそのまま引数に渡しても扱えない。
as_view()メソッドはクラスを関数に変換する役割を持っているので、as_view()メソッドを使ってクラスを関数に変換している。


"""