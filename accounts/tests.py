from django.test import LiveServerTestCase
from django.urls import reverse_lazy
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login(self):
    self.selenium.get(self.live_server_url + str(reverse_lazy('account_login')))

    username_input = self.selenium.find_element(By.NAME, "login")
    username_input.send_keys('test@gmail.com')

    password_input = self.selenium.find_element(By.NAME, "password")
    password_input.send_keys('test12345')

    # ログインボタンの取得
    button = self.selenium.find_element(By.CSS_SELECTOR, 'form button[type="submit"]')

    # スクロールして要素を画面内に入れる
    self.selenium.execute_script("arguments[0].scrollIntoView(true);", button)

    # 要素がクリック可能になるまで待つ
    WebDriverWait(self.selenium, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'form button[type="submit"]')))

    # クリック
    button.click()

    # 遷移後の検証
    WebDriverWait(self.selenium, 10).until(EC.title_is('本一覧 | Book Share'))
    self.assertEqual('本一覧 | Book Share', self.selenium.title)
