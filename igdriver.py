import json
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import bnh
import config

# undetected = False
undetected = True

if undetected:
    import undetected_chromedriver as uc
    driver = uc.Chrome()
else:
    from selenium import webdriver
    driver = webdriver.Chrome()
driver.implicitly_wait(10)

url = 'https://www.instagram.com/direct/inbox/'


def login():
    time.sleep(2)
    username_input = driver.find_element(By.CSS_SELECTOR, '#loginForm input[name="username"]')
    password_input = driver.find_element(By.CSS_SELECTOR, '#loginForm input[name="password"]')
    login_button = driver.find_element(By.CSS_SELECTOR, '#loginForm button[type="submit"]')

    username_input.send_keys(config.username)
    time.sleep(1)
    password_input.send_keys(config.password)
    time.sleep(1)
    login_button.click()
    time.sleep(2)


def add_cookies():
    try:
        with open('cookies.json') as f:
            cookies = json.load(f)
    except FileNotFoundError:
        login()
        cookies = driver.get_cookies()
        with open('cookies.json', 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=4)
        driver.get(url)

    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(2)


def send_msg(msg):
    time.sleep(1)
    textbox = driver.find_element(By.CSS_SELECTOR, 'div[role="textbox"]')
    msg_lines = msg.split('\n')
    for idx, line in enumerate(msg_lines):
        if line:
            textbox.send_keys(line)
        if idx != len(msg_lines) - 1:
            textbox.send_keys(Keys.SHIFT, Keys.ENTER)
    textbox.send_keys(Keys.ENTER)
    time.sleep(1)


def run():
    driver.get(url)
    add_cookies()

    try:
        notif_button = driver.find_element(By.CSS_SELECTOR, 'div[role="dialog"] button._a9--._ap36._a9_1')
        notif_button.click()
        time.sleep(2)
    except NoSuchElementException:
        pass

    while True:
        try:
            chat_buttons = driver.find_elements(By.CSS_SELECTOR, 'div[aria-label="Chats"] div.x13dflua.x19991ni > div[role="button"]')
            random.shuffle(chat_buttons)

            for cb in chat_buttons:
                msg = cb.find_element(
                    By.CSS_SELECTOR, 'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1.xmix8c7.xh8yej3 > span:first-child > span'
                ).text
                if msg[:5] == 'You: ':
                    continue

                print(msg)
                ret_msg = bnh.get_ret(msg)
                print(ret_msg)
                cb.click()
                send_msg(ret_msg)
                time.sleep(0.2)

            time.sleep(0.2)

        except KeyboardInterrupt:
            break


if __name__=='__main__':
    run()
