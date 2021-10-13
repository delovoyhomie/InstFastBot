    """
    Бот для инстаграма, который управляеся через бота в телеграме(InstFastBot)
    
    Функции: 
    📕Справка (/help): 
    📌  1) Пролайкать полностью аккаунт (/like_all_acc);  # /like_all_acc - кнопка в телеге, нажав на неё можно получить инструкцию по выполнению
    📌 2) Лайкнуть пост по ссылке (/like_post);           # /like_post - кнопка в телеге, нажав на неё можно получить инструкцию по выполнению
    📲 3) Скачать фото поста по ссылке (/save_photo);     # /save_photo - кнопка в телеге, нажав на неё можно получить инструкцию по выполнению
    📝 4) Подписаться на аккаунт (/subscribe)             # /subscribe - кнопка в телеге, нажав на неё можно получить инструкцию по выполнению
    ps также есть команда /start (при первом запуске бота инструкция) и /about
    
    Реализация:
    Бот управляется через телеграм-бота. На пк отправляются данные с телеги, затем через эмулятор действий в браузере(webdriver для chrome) бот заходит в свой аккаунт Instagram
    и выполняет действия, назначенные пользователем. 
    Т.е. бот по X-Patch ищет на странице нужны элементы и работает с ними.
    
    Выполнение:
    1) Пролайкать полностью аккаунт: 
    1.1 бот входит в свой акк
    1.2 пролистывает страницу нужного пользователя, собирая все ссылки на посты и записывает их в txt файл. Там они сортируются, чтобы не было повторений, и, в порядке очереди,
    ставит лайки по X-Patch(находит button(кнопку лайка) и кликает)
    
    2) Лайкнуть пост по ссылке:
    1.1 бот входит в свой акк
    1.2 открывает ссылку поста и ставит лайк
    
    3) Скачать фото поста по ссылке:
    1. Либо через библиотеку requests
    2. Либо вручную через html код(я это убрал из кода из-за ненадобности)
    
    4)Подписаться на аккаунт:
    1.1 бот входит в свой акк
    1.2 ищет кнопку подписки на странице пользователя по X-Patch и кликает на неё.
    
    
    
    """
import telebot
from telebot import types
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from token_bot import token
import time
import random
import requests
from selenium.common.exceptions import NoSuchElementException
bot = telebot.TeleBot(token)


def login(username, password):
    try:
        global browser
        browser = webdriver.Chrome('chromedriver')   # установка веб-драйвера хром
        browser.get('https://www.instagram.com')     # открытие ссылки
        time.sleep(6)                                # время для прогрузки страницы (секунды)
        username_input = browser.find_element_by_name('username')   # ищет на странице элемент с именем "username"
        username_input.clear()                       # очистка поля "username" (на всякий случай)
        username_input.send_keys(username)           # в поле "username" отправляются данные username из py-файла
        time.sleep(2)
        password_input = browser.find_element_by_name('password') # ищется элемент password
        password_input.clear()                       # очистка поля "пароль"
        password_input.send_keys(password)           # в поле "пароль" отправить пароль из py-файла
        password_input.send_keys(Keys.ENTER)         # нажатие кнопки "войти" (Enter)

        time.sleep(10)
        browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button').click() # ищет по xpath элемент на странице
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        time.sleep(2)
    except Exception as ex:
        print(ex)


def get_all_posts_urls(userpage):
    # ссылки на все посты
    browser.get('https://www.instagram.com/' + userpage + '/')
    posts_count = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text  # количество постов
    posts_count = int(posts_count)
    print('Кол-во постов:', posts_count)
    scroll_posts_count = int(posts_count // 12)  # количество прокруток страницы по 12 постов

    post_urls = []
    for i in range(0, scroll_posts_count):   # кол-во прокруток страницы
        hrefs = browser.find_elements_by_tag_name('a')
        hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')] # поиск постов по 'p' в ссылке

        for href in hrefs:
            post_urls.append(href) # в списке хранятся все ссылки

        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # прокрутка страницы по всей её длине (что-то около 12-16 постов)
        time.sleep(random.randrange(2, 4))
        print(f"Итерация #{i}")

    set_posts_urls = set(post_urls) # сортировка ссылок для избежания повторений ссылок
    set_posts_urls = list(set_posts_urls)

    with open(f'{userpage}_set.txt', 'w') as file:
        for i_post_url in set_posts_urls:
            file.write(i_post_url + '\n')


# накрутка лайков на весь аккаунт
def get_many_likes(userpage):
    login(username='', password='') #username - ник аккаунта бота, password - пароль аккаунта бота
    get_all_posts_urls(userpage=nickname)
    with open(f'{nickname}_set.txt', 'r') as file:
        urls_list = file.readlines()
        for i_post_url in urls_list:
            try:
                browser.get(i_post_url)
                time.sleep(2)

                like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
                browser.find_element_by_xpath(like_button).click()
                # time.sleep(random.randrange(80, 100))
                time.sleep(2)

                print(f"Лайк на пост: {i_post_url} успешно поставлен!")

            except Exception as ex:
                print(ex)
                browser.close()
                browser.quit()
    time.sleep(2)
    browser.close()
    browser.quit()

# поставка лайка на пост
def instbot_like_on_post():
    login(username='', password='') #username - ник аккаунта бота, password - пароль аккаунта бота
    browser.get(link_like_on_post)
    time.sleep(5)
    like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button" # храth кнопки лайка
    browser.find_element_by_xpath(like_button).click()
    time.sleep(2)
    browser.close()
    browser.quit()


#скачивание фото со страницы
def download_file_photo_acc(userpage):
    global post_id
    login(username='', password='') #username - ник аккаунта бота, password - пароль аккаунта бота
    userpage = nickname_download_photoo_acc
    browser.get(userpage)
    time.sleep(4)

    # img_src = "/html/body/div[6]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[2]"
    # img_src_url = browser.find_element_by_xpath(img_src).get_attribute("src")

    s = browser.find_element_by_class_name('FFVAD').get_attribute('src')
    r = requests.get(s, stream=True)

    post_id = userpage.split("/")[-2]
    with open(str(post_id) +".jpg", "wb") as img_file:
        img_file.write(r.content)
    browser.close()
    browser.quit()

# подписка
def follow(userpage):
    login(username='', password='') #username - ник аккаунта бота, password - пароль аккаунта бота
    browser.get('https://www.instagram.com/' + userpage + '/')
    browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button').click() #кнопка подписки

    browser.close()
    browser.quit()


# при написании команды /about, бот будет писать справку
@bot.message_handler(commands=['start']) # команда /start
def welcome(message):
    markdown = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Справка")
    markdown.add(item1)
    bot.send_message(message.chat.id, 'Добро пожаловать!\nНажми на плашку "Справка" снизу и увидишь результат',  reply_markup=markdown)

@bot.message_handler(commands=['help'])  # команда /help
def help(message):
    bot.send_message(message.chat.id, '🤖 Убедительная просьба!'
                                      '\n InstFastBot крашнется и не будет работать в случае, если Вы ему будете давать ему сразу несколько команд (2 и более). '
                                      '\n Спасибо за понимание!')

@bot.message_handler(commands=['subscribe'])  # команда /subscribe
def help(message):
    bot.send_message(message.chat.id, '🤖 InstFastBot может подписаться на любого человека из Instagram. '
                                      '\n Как пользоваться:'
                                      '\n  1. Зайдите в Instagram.'
                                      '\n  2. Выберите интересующий Вас аккаунт.'
                                      '\n  3. Запомните ник аккаунта (без @).'
                                      '\n  4. Отправьте нашему боту ник (без @)!'
                                      '\n \n ps если аккаунт закрытый - отправит запрос')


@bot.message_handler(commands=['like_all_acc'])
def help(message):
    bot.send_message(message.chat.id, '🤖 InstFastBot может пролайкать полностью аккаунт человека!'
                                      '\n Как пользоваться:'
                                      '\n  1. Зайдите в Instagram.'
                                      '\n  2. Выберите интересующий Вас аккаунт.'
                                      '\n  3. Запомните ник аккаунта (без @).'
                                      '\n  4. Отправьте нашему боту ник (без @)!'
                                      '\n \n ps если очень много постов - бот крашнется. увы, ноут не может потянуть на себе 5000 постов, как у скалы...')

@bot.message_handler(commands=['save_photo'])
def help(message):
    bot.send_message(message.chat.id, '🤖 InstFastBot может скачать фото в формате "jpg"!'
                                      '\n Как пользоваться:'
                                      '\n  1. Зайдите в Instagram.'
                                      '\n  2. Выберите интересующий Вас пост (фотографию).'
                                      '\n  3. Отправьте нашему боту ссылку на пост(фотографию)!'
                                      '\n \n ps видео бот пока что не умеет скачивать, потому что instagram стал умнее и шифрует ссылку с помощью "blog".\n если кто-то знает как расшифровать ссылку - пишите мне на почту slavik5yakimenko@gmail.com ')

@bot.message_handler(commands=['like_post'])
def help(message):
    bot.send_message(message.chat.id, '🤖 InstFastBot может лайкнуть пост по ссылке!'
                                      '\n Как пользоваться:'
                                      '\n  1. Зайдите в Instagram.'
                                      '\n  2. Выберите интересующий Вас пост.'
                                      '\n  3. Нажмите кнопку «Скопировать ссылку».'
                                      '\n  4. Отправьте нашему боту эту ссылку!')

@bot.message_handler(content_types = ['text'])
def add_message(message):

    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("1", callback_data='1')
    item2 = types.InlineKeyboardButton("2", callback_data='2')
    item3 = types.InlineKeyboardButton("3", callback_data='3')
    item4 = types.InlineKeyboardButton("4", callback_data='4')
    markup.add(item1, item2, item3, item4)

    if message.chat.type == 'private':
        if message.text == 'Справка':
            info = '📕Справка (/help): \n 📌 1) Пролайкать полностью аккаунт (/like_all_acc); \n 📌 2) Лайкнуть пост по ссылке (/like_post); \n \n📲 3) Скачать фото поста по ссылке (/save_photo); \n\n📝 4) Подписаться на аккаунт (/subscribe)'
            bot.send_message(message.chat.id, info, reply_markup=markup)

def nickname_reg_many_likes(message):
    global nickname
    nickname = message.text
    #bot.send_message(message.chat.id, 'Ник аккаунта: ' + nickname)
    bot.send_message(message.chat.id, 'Принято в работу.\nПо окончании загрузки бот отправит результат.')
    get_many_likes(userpage=nickname)
    bot.send_message(message.chat.id, 'Все лайки поставлены!')

def like_on_post(message):
    global link_like_on_post
    link_like_on_post = message.text
    #bot.send_message(message.chat.id, 'Ссылка на пост: ' + link_like_on_post)
    bot.send_message(message.chat.id, 'Принято в работу.\nПо окончании загрузки бот отправит результат.')
    instbot_like_on_post()
    bot.send_message(message.chat.id, 'Лайк поставлен!')

def nickname_download_photo_acc(message):
    global nickname_download_photoo_acc
    nickname_download_photoo_acc = message.text
    bot.send_message(message.chat.id, 'Принято в работу.\nПо окончании загрузки бот отправит результат.')
    # gif = open("loading.gif", 'rb')
    # loading = bot.send_animation(message.chat.id, gif)
    download_file_photo_acc(userpage=nickname_download_photoo_acc)
    bot.send_photo(message.chat.id, open(post_id + '.jpg', 'rb'))
    bot.send_document(message.chat.id, open(post_id + '.jpg', 'rb'))

def nickname_follow_def(message):
    global nickname_follow
    nickname_follow = message.text
    bot.send_message(message.chat.id, 'Принято в работу.\nПо окончании загрузки бот отправит результат.')
    follow(userpage=nickname_follow)
    bot.send_message(message.chat.id, 'Подписка на аккаунт'+ ' ' + nickname_follow + ' ' + 'выполнена!')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == '1':
        bot.send_message(call.message.chat.id, 'Выбран пункт 1 ✅\nНапишите ник аккаунта' )
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Будет выполнено ✅")  # показ уведомления
        bot.register_next_step_handler(call.message, nickname_reg_many_likes)
    elif call.data == '2':
        bot.send_message(call.message.chat.id, 'Выбран пункт 2 ✅\nНапишите ссылку поста, на который нужно поставить лайк')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Будет выполнено ✅")  # показ уведомления
        bot.register_next_step_handler(call.message, like_on_post)
    elif call.data == '3':
        bot.send_message(call.message.chat.id, 'Выбран пункт 3 ✅\nНапишите ссылку поста (фото), который нужно скачать')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Будет выполнено ✅")  # показ уведомления
        bot.register_next_step_handler(call.message, nickname_download_photo_acc)
    elif call.data == '4':
        bot.send_message(call.message.chat.id, 'Выбран пункт 4 ✅\nНапишите ник аккаунта, на который нужно подписаться')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Будет выполнено ✅")  # показ уведомления
        bot.register_next_step_handler(call.message, nickname_follow_def)

bot.polling(none_stop=True)   # бот будет работать беспрерывно