from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from ..models import BookShare

class LoggedInTestCase(TestCase):
  """各テストクラスで共通の事前準備仮処理をオーバーライドした独自TestCaseクラス"""

  def setUp(self):
    """テストメソッド実行前の事前設定"""

    # テストユーザーのパスワード
    self.password = 'jagaimo1013'

    # 各インスタンスメソッドで使うテスト用ユーザーを生成し
    # インスタンス変数に格納しておく
    self.test_user = get_user_model().objects.create_user(
      username='postgres',
      email='test@gmail.com',
      password=self.password
    )

    # テスト用ユーザーでログインする
    self.client.login(email=self.test_user.email, password=self.password)

class TestBookCreateView(LoggedInTestCase):
  """BookCreateView用のテストクラス"""

  def test_create_book_success(self):
    """本作成処理が成功することを検証する"""

    # Postパラメータ
    params = {'title': 'テストタイトル',
              'content': '本文',
              'photo1': '',
              'photo2': '',
              'photo3': ''
              }
    
    # 新規本情報作成処理(Post)を実行
    response = self.client.post(reverse_lazy('bookshare:book_create'), params)

    # 本一覧ページへのリダイレクトを検証
    self.assertRedirects(response, reverse_lazy('bookshare:book_list'))

    # 本データがデータベースに登録されたかを検証
    self.assertEqual(BookShare.objects.filter(title='テストタイトル').count(), 1)

  def test_create_book_failure(self):
    """新規本情報作成処理が失敗することを検証する"""

    # 新規本作成処理(Post)を実行
    response = self.client.post(reverse_lazy('bookshare:book_create'))

    # 必須フォームフィールドが未入力によりエラーになることを検証
    self.assertFormError(response, 'form', 'title', 'このフィールドは必須です。')

class TestBookUpdateView(LoggedInTestCase):
  """BookUpdateView用のテストクラス"""

  def test_update_book_success(self):
    """本編集処理が成功することを検証する"""

    # テスト用本データの作成
    book = BookShare.objects.create(user=self.test_user, title='タイトル編集前')

    # Postパラメータ
    params = {'title': 'タイトル編集後'}

    # 本編集処理(Post)を実行
    response = self.client.post(reverse_lazy('bookshare:book_update', kwargs={'pk': book.pk}), params)

    # 本詳細ページへのリダイレクトを検証
    self.assertRedirects(response, reverse_lazy('bookshare:book_detail', kwargs={'pk': book.pk}))

    # 本データが編集されたかを検証
    self.assertEqual(BookShare.objects.get(pk=book.pk).title, 'タイトル編集後')

  def test_update_book_failure(self):
    """本編集処理が失敗することを検証する"""

    # 本情報編集処理(Post)を実行
    response = self.client.post(reverse_lazy('bookshare:book_update', kwargs={'pk': 999}))

    # 存在しない本データを編集しようとしてエラーになることを検証
    self.assertEqual(response.status_code, 404)

class TestBookDeleteView(LoggedInTestCase):
  """BookDeleteView用のテストクラス"""

  def test_delete_book_success(self):
    """本情報削除処理が成功することを検証する"""

    # テスト用本データの作成
    book = BookShare.objects.create(user=self.test_user, title='タイトル')

    # 本削除処理(Post)を実行
    response = self.client.post(reverse_lazy('bookshare:book_delete', kwargs={'pk': book.pk}))

    # 本一覧ページへのリダイレクトを検証
    self.assertRedirects(response, reverse_lazy('bookshare:book_list'))

    # 本データが削除されたかを検証
    self.assertEqual(BookShare.objects.filter(pk=book.pk).count(), 0)

  def test_delete_book_failure(self):
    """本情報削除が失敗することを検証する"""

    # 本削除処理(Post)を実行
    response = self.client.post(reverse_lazy('bookshare:book_delete', kwargs={'pk': 999}))