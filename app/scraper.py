import datetime
import os
import time
import requests
from datetime import datetime as dt
import locale
import re
import streamlit as st


# locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--remote-debugging-port=9222")


def get_all_books(driver):
    username = "210442158"
    password = "43h?jMEU"

    # opacトップページへ遷移
    url = "https://opac.meijo-u.ac.jp/?page_id=0"
    driver.get(url)
    driver.implicitly_wait(60)  # 追加

    driver.find_element(By.ID, "opacSideAsk_39466").click()
    time.sleep(2)

    # 現在のウィンドウのハンドルを取得
    current_window_handle = driver.current_window_handle

    opac_login(username, password, driver)

    driver.find_element(By.XPATH, '//*[@id="popup"]/table/tr[2]/td[1]/input').click()

    # 全てのタブのハンドルを取得
    all_window_handles = driver.window_handles

    # 現在のタブと異なるハンドルを見つける
    new_window_handle = None
    for handle in all_window_handles:
        if handle != current_window_handle:
            new_window_handle = handle
            break

    # 新しいタブに切り替える
    driver.switch_to.window(new_window_handle)

    str = driver.find_element(
        By.XPATH, "/html/body/div/div/div/div[1]/form/div/div[3]/div[2]/p"
    ).text

    if re.search(r"借りている資料\s*0冊", str):
        print("冊数は0冊です。")
    else:
        books = []
        driver.find_element(
            By.XPATH, "/html/body/div/div/div/div[1]/form/div/div[3]/div[2]/div/button").click()

        contents = driver.find_elements(By.XPATH, "/html/body/div/div/div/div[1]/form[1]/div/div[3]")
        for content in contents:
            name = content.find_element(By.XPATH, "/html/body/div/div/div/div[1]/form[1]/div/div[3]/table/tbody/tr[2]/td[8]/a",).text
            books.append(name)

    return books


def opac_login(username, password, driver):

    # ユーザーネームとパスワードを定義
    username_value = username
    password_value = password

    # ユーザーネームを入力
    username = driver.find_element(By.ID, "idToken1")
    username.send_keys(username_value)

    # パスワードを入力
    password = driver.find_element(By.ID, "idToken2")
    password.send_keys(password_value)

    # ログインボタンをクリック
    driver.find_element(By.ID, "loginButton_0").click()
    driver.implicitly_wait(60)  # 追加


# 入力フィールドにフォーカスを当ててから、値をDELETE
def clear_input(element):
    element.click()
    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.DELETE)


# ユーザID、パスワードを設定
# username = (os.environ.get("SBI_USER"),)
# password = os.environ.get("SBI_PASS")

username = "210442158"
password = "43h?jMEU"

# print("ログイン処理を開始します。")
# driver = sbi_login(username, password)
driver = webdriver.Chrome(options=options)
driver.set_window_size(950, 800)
print("データの取得を開始します。")
books = get_all_books(driver)
# driver.quit()

print("データの内容を表示します。")
print(books)


# headers = {
#     "Content_Type": "application/json",
#     "Authorization": "Bearer "
#     + "3CqE6LNR8wAZelOAWoHEzCIR/s2Ygky8h3mfWnDkU016/sgStrpPsU9lfCO115MTea3K1cuIanM6DDvSHvFsnvgPN1Y8F+oeElG+CG+E0fRkAKOtyhZhwZ46cU2l7OJP03d51vuBxmhlPwtyEUZcPwdB04t89/1O/w1cDnyilFU=",
# }


# def SendMsg(text, uid):
#     res = requests.post(
#         "https://api.line.me/v2/bot/message/push",
#         headers=headers,
#         json={"to": uid, "messages": [{"type": "text", "text": text}]},
#     ).json()


# str = sbi_dividend_data

# if __name__ == "__main__":
#     SendMsg(str, "Uc97709b4b5baaafa68fb054916ec63de")
