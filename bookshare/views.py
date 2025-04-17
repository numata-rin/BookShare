"""
ビューは、ルーティングからリクエスト情報を受け取ってレスポンス情報を作り出す役割を持つ。
Djangoはリクエスト情報とレスポンス情報をオブジェクトとして扱っており、そのオブジェクト内には
methodやログイン中のユーザー情報など様々なものが格納されている。

またビューはレスポンス情報を作り出すために必要に応じて様々なコンポーネントに
様々なリクエストを送る。
"""
import logging

from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404

from .models import BookShare
from .forms import InquiryForm, BookCreateForm

logger = logging.getLogger(__name__)

class OnlyYouMixin(UserPassesTestMixin):
  raise_exception = True

  def test_func(self):
    # URLに埋め込まれた主キーから本データを一件取得。取得できなかった場合は404エラー
    book = get_object_or_404(BookShare, pk=self.kwargs['pk'])
    return self.request.user == book.user

class IndexView(generic.TemplateView):
  template_name = "index.html"

class InquiryView(generic.FormView):
  template_name = "inquiry.html"
  form_class = InquiryForm
  #処理に問題がなかったときにreverse_lazy関数で逆引きして指定したＵＲＬにリダイレクトする。(success_urlはクラス変数)
  success_url = reverse_lazy('bookshare:inquiry')

  def form_valid(self, form):
    form.send_email()
    messages.success(self.request, 'メッセージを送信しました。')
    logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
    return super().form_valid(form)
  
class BookListView(LoginRequiredMixin, generic.ListView):
  model = BookShare
  template_name = 'book_list.html'
  paginate_by = 2

  def get_queryset(self):
    books = BookShare.objects.filter(user=self.request.user).order_by('-created_at')
    return books
  
class BookDetailView(LoginRequiredMixin, OnlyYouMixin, generic.DetailView):
  model = BookShare
  template_name = 'book_detail.html'
  pk_url_kwarg = 'pk'

class BookCreateView(LoginRequiredMixin, generic.CreateView):
  model = BookShare
  template_name = 'book_create.html'
  form_class = BookCreateForm
  success_url = reverse_lazy('bookshare:book_list')

  def form_valid(self, form):
    book = form.save(commit=False)
    book.user = self.request.user
    book.save()
    messages.success(self.request, '日記を作成しました。')
    return super().form_valid(form)
  
  def form_invalid(self, form):
    messages.error(self.request, "日記の作成に失敗しました。")
    return super().form_invalid(form)
  
class BookUpdateView(LoginRequiredMixin, OnlyYouMixin, generic.UpdateView):
  model = BookShare
  template_name = 'book_update.html'
  form_class = BookCreateForm

  def get_success_url(self):
    return reverse_lazy('bookshare:book_detail', kwargs={'pk': self.kwargs['pk']})
  
  def form_valid(self, form):
    messages.success(self.request, '本情報を更新しました。')
    return super().form_valid(form)
  
  def form_invalid(self, form):
    messages.error(self.request, "本情報の更新に失敗しました。")
    return super().form_invalid(form)

class BookDeleteView(LoginRequiredMixin, OnlyYouMixin, generic.DeleteView):
  model = BookShare
  template_name = 'book_delete.html'
  success_url = reverse_lazy('bookshare:book_list')

  def delete(self, request, *args, **kwargs):
    messages.success(self.request, "本情報を削除しました。")
    return super().delete(request, *args, **kwargs)

"""補足・個人用メモ

・form_classをオーバーライドする理由
フォームとビューを紐づけるため

・form_validメソッドについて
form_validメソッドは親クラスで定義されているメソッドで、フォームバリデーションに問題が
なかったら実行されるメソッド。これをオーバーライドして独自処理を追加出来る。
form_validメソッドでは「form」という名前の引数にformオブジェクトが格納されており、
フォームバリデーションを通ったユーザー入力値を取り出すことが出来る。

"""