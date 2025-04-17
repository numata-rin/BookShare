"""
フォームは、フォーム画面で入力された値をフォームオブジェクトに変換および保持するコンポーネントである。
また、入力値のバリデーションまで担う。

フォーム定義を記述するのは forms.py というファイルになるが、このファイルは自動作成されないため
開発者側で作成する必要がある。作成する場所はDjangoアプリケーションディレクトリ直下になる。

フォーム定義は、forms.py に django.forms.Form クラスまたは django.forms.ModelForm クラスを継承して行う。
前者のFormクラスはどのようなフォームにも使えるが、後者のModelFormクラスのほうはモデルのフィールドとフォーム画面のフィールドが同じような場合に
使えることが出来る。モデルのフィールド定義を流用する分、Formクラスよりも簡潔に記述できる。
さらにモデルの各フィールドに設定した制約（ユニーク制約など）についてもデフォルトでバリデーションしてくれて便利なので
積極的に使いたい。本アプリケーションでは両方使う。

"""

import os

from django import forms
from django.core.mail import EmailMessage

from .models import BookShare
"""
django.forms.Formクラスを継承したフォーム定義では、以下のInquiryFormクラスのように
フィールドクラスを1個ずつ定義する必要がある。
"""
#汎用的に使えるdjango.forms.Formクラスを継承したInquiryFormクラスを作り、その中に4つのフォームフィールドを定義している。
class InquiryForm(forms.Form):
  name = forms.CharField(label="お名前", max_length=30)
  email = forms.EmailField(label="メールアドレス")
  title = forms.CharField(label="タイトル", max_length=30)

  """
  フォームのフィールドクラスにはウィジェットがデフォルトで設定されている。
  ウィジェットとはフィールドクラスに設定されているフィールドのタイプ（テキストフィールドなど）や
  画面のデザインをまとめたものである。このウィジェットは変えることができ、以下では CharField のウィジェット
  をテキストエリアに変えている。
  """
  message = forms.CharField(label="メッセージ", widget=forms.Textarea)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['name'].widget.attrs['class'] = 'form-control'
    self.fields['name'].widget.attrs['placeholder'] = 'お名前をここに入力してください。'

    self.fields['email'].widget.attrs['class'] = 'form-control'
    self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力してください。'

    self.fields['title'].widget.attrs['class'] = 'form-control'
    self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力してください。'

    self.fields['message'].widget.attrs['class'] = 'form-control'
    self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください。'

  #メール送信処理を行うメソッド。メール送信処理に関係しているので、引数にはformオブジェクトが渡されることを想定している。
  #引数のselfに対してcleaned_dataメソッドなどを行ってビューの時と同様にフォームバリデーションを通ったユーザー入力値を取得。
  
  def send_email(self):
    name = self.cleaned_data['name']
    email = self.cleaned_data['email']
    title = self.cleaned_data['title']
    message = self.cleaned_data['message']

    subject = 'お問い合わせ {}'.format(title)
    message = '送信者名: {0}\nメールアドレス: {1}\nメッセージ:\n{2}'.format(name, email, message)
    from_email = os.environ.get('FROM_EMAIL')
    to_list = [os.environ.get('FROM_EMAIL')]
    cc_list = [email]

    message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
    message.send()

class BookCreateForm(forms.ModelForm):
  
  class Meta:
    model = BookShare
    fields = ('title', 'content', 'photo1', 'photo2', 'photo3',)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'


"""
class DiaryCreateForm(forms.ModelForm):

  class Meta:
    model = BookShare
    fields = ('title', 'content', 'photo1', 'photo2', 'photo3')

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'
"""