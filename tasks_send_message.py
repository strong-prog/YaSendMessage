from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ex
import telebot
import time
import datetime


def input_account(brow, name, password, num):
    button = WebDriverWait(brow, 5).until(
         ex.presence_of_element_located((By.CSS_SELECTOR, '.Button2')))
    button.click()

    name_field = WebDriverWait(brow, 5).until(
         ex.presence_of_element_located((By.NAME, 'login')))
    name_field.send_keys(name)

    pass_field = WebDriverWait(brow, 5).until(
         ex.presence_of_element_located((By.NAME, 'passwd')))
    pass_field.send_keys(password)

    button_sign_in = WebDriverWait(brow, 5).until(
         ex.presence_of_element_located((By.CSS_SELECTOR, '.passport-Button-Text')))
    button_sign_in.click()
    time.sleep(1)

    number_field = WebDriverWait(brow, 5).until(
         ex.presence_of_element_located((By.CSS_SELECTOR, '.passport-Input-Controller')))
    number_field.send_keys(num)

    button_sign_in2 = WebDriverWait(brow, 5).until(
         ex.presence_of_element_located((By.CSS_SELECTOR, '.passport-Button-Text')))
    button_sign_in2.click()
    print('Авторизация успешна.')


def send_message(pay):
    token = '...'
    bot = telebot.TeleBot(token)
    chat_id = '-805805357'
    text = f'Задание принято на {pay}р. Приступай к работе.'
    bot.send_message(chat_id, text)
    

def get_task(brow):
    try:
        get_snippets = WebDriverWait(brow, 2).until(
             ex.presence_of_all_elements_located((By.CSS_SELECTOR, '.snippet__side.snippet__side_right')))
    except TimeoutException:
        return False

    dict_snippets = {}
    if get_snippets:
        for snippet in get_snippets:
            payment = int(float(snippet.find_element(By.CSS_SELECTOR, '.informer-field__value').text.replace(',', '.')))
            if payment >= 100:
                dict_snippets[payment] = snippet
        if dict_snippets:
            max_key = max(dict_snippets.keys())
            button = dict_snippets[max_key].find_element(By.CSS_SELECTOR, '.snippet__take-btn')
            button.click()
            print('Задача принята.')
            send_message(max_key)
            print('Сообщение отправлено.')
            return True
        else:
            return False
    else:
        return False


def time_t():
    today = datetime.datetime.today()
    return today.strftime("%H:%M:%S")


user_name = '...'
user_pass = '...'
user_num = '...'

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
browser = webdriver.Firefox(options=options)
browser.get('https://.../tasks')
print(f'Браузер запущен. {time_t()}')

try:
    input_account(browser, user_name, user_pass, user_num)
    while True:
        if get_task(browser):
            break
        else:
            print('Подходящих заданий нет.')
            print(f'Обновление задач. {time_t()}')
            browser.refresh()

finally:
    browser.quit()
    print(f'Браузер закрыт. {time_t()}')
