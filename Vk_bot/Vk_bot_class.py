import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from configparser import ConfigParser
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sys
import time
from DB.data_changers import (
    open_session,
    update_user,
    get_favorites,
    set_favorite,
    get_likes,
    unset_like,
)
from DB.data_changers import (
    unset_blocklist,
    set_like,
    set_blocklist,
    set_dislike,
    unset_favorite,
    get_blocklist,
)

from vk.vk import VKConnector, VKUser

"""Открытие токина для бота"""


def open_a_token(file_name):
    config = ConfigParser()
    config.read(file_name)
    group_token = config["Vk_info"]["group_token"]
    return group_token


def get_db(file_name):
    """
    Берёт строчку для коннекта с БД
    """
    config = ConfigParser()
    config.read(file_name)
    dsn = config["Vk_info"]["DB_connect"]
    return dsn


def open_user_token(file_name):
    """Открытие токина для бота"""
    config = ConfigParser()
    config.read(file_name)
    user_token = config["Vk_info"]["user_token"]
    return user_token


class VkBot:

    """Подключение к боту"""

    def __init__(self, file_name: str, vk: VKConnector):
        self.vk_session = vk_api.VkApi(token=open_a_token(file_name))
        self.vk_api = self.vk_session.get_api()
        self.long_pool = VkLongPoll(self.vk_session)
        self.get_parametrs = {}
        self.__session = open_session(get_db(file_name))
        self.__vk = vk
        self.result_requests_vkontakte = []

    """Сообщение от бота: кому, сообщение, id собщения, кнопки, картинки"""

    def write_msg(self, user_id, message="", keyboard=None, attachment=None):
        post = {
            "user_id": user_id,
            "message": message,
            "random_id": randrange(10**7),
        }
        if message != "":
            post["message"] = message
        else:
            message = message
        if keyboard != None:
            post["keyboard"] = keyboard.get_keyboard()
        else:
            post = post
        if attachment != None:
            post["attachment"] = attachment
        else:
            post = post
        return self.vk_session.method("messages.send", post)

    """Список цветов"""

    def but_col(self):
        buttons_colors = [
            VkKeyboardColor.POSITIVE,
            VkKeyboardColor.NEGATIVE,
            VkKeyboardColor.PRIMARY,
            VkKeyboardColor.SECONDARY,
        ]
        return buttons_colors

    """Задаём цвет, количество кнопок в ответе бота"""

    def set_key_parameters(self, buttons, but_col):
        keyboard = VkKeyboard(one_time=True)
        if not isinstance(buttons, list) and not isinstance(but_col, list):
            buttons = [buttons]
            but_col = [but_col]
        count = 0
        for bnt, bnt_colors in zip(buttons, but_col):
            if count == 2:
                keyboard.add_line()
            if count == 4:
                keyboard.add_line()
            keyboard.add_button(bnt, bnt_colors)
            count += 1
        return keyboard

    """Собщения боту от пользователя"""

    def get_message(self):
        for event in self.long_pool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                message = event.text.lower()
                user_id = event.user_id
                return message, user_id

    def command_list_output(self):
        """Приветствие"""
        response = "Добро пожаловать в бот Vkinder.\nВыберите команду!"
        return response

    """Кнопки в приветствии бота, главное меню"""

    def greetings_bot(self):
        buttons = [
            "Избранные",
            "Мне нравится",
            "Черный список",
            "Начать поиск",
            "Завершить работу с ботом",
        ]
        but_col = self.but_col()
        keyboard = self.set_key_parameters(
            buttons, [but_col[2], but_col[2], but_col[2], but_col[0], but_col[1]]
        )
        return keyboard

    """Сообщение боту"""

    def query_bot(self):
        message, self.user_id = self.get_message()
        update_user(self.__session, self.user_id, 0, 0, "")
        return message, self.user_id

    """Показать гавлное меню"""

    def show_main_menu(self):
        # msg, user_id = self.query_bot()
        keyboard = self.greetings_bot()
        return self.write_msg(self.user_id, self.command_list_output(), keyboard)

    """Стартовое меню"""

    def start_bot(self):
        return self.show_main_menu()

    """Работа со списком избранных"""

    def show_favorites_list(self, user_id):
        def the_end(user_id):
            if count >= len(favorites_list) - 1:
                buttons = ["Вернуться в главное меню", "Вывести избранных"]
                but_col = self.but_col()
                keyboard = self.set_key_parameters(buttons, [but_col[1], but_col[0]])
                self.write_msg(user_id, "Это была последняя анкета", keyboard)
                message, user_id = self.get_message()
                if message.lower() == "вернуться в главное меню":
                    return self.start_bot()
                elif message.lower() == "вывести избранных":
                    return self.show_favorites_list(user_id)

        # base_data = [1, 2]  # Тут вставить БД
        favorites_list = get_favorites(self.__session, user_id)
        msg = "Избранные"
        self.write_msg(user_id, msg, keyboard=None)
        if favorites_list == []:
            msg = "Список избранных пуст"
            but_col = self.but_col()
            keyboard = self.set_key_parameters("Вернуться в главное меню", but_col[1])
            self.write_msg(user_id, msg, keyboard)
            message, user_id = self.query_bot()
            if message == "вернуться в главное меню":
                return self.start_bot()
        elif favorites_list != []:
            for count, user in enumerate(favorites_list):
                info_user = self.__vk.get_user(user)
                attachment_1 = f"photo{info_user.photos[0]['owner_id']}_{info_user.photos[0]['id']}"
                attachment_2 = f"photo{info_user.photos[1]['owner_id']}_{info_user.photos[1]['id']}"
                attachment_3 = f"photo{info_user.photos[2]['owner_id']}_{info_user.photos[2]['id']}"
                self.write_msg(
                    user_id,
                    f"{info_user.name}, дата рождения {info_user.bdate}, {info_user.city}",
                    keyboard=None,
                    attachment=None,
                )
                self.write_msg(user_id, "", keyboard=None, attachment=attachment_1)
                self.write_msg(user_id, "", keyboard=None, attachment=attachment_2)
                self.write_msg(user_id, "", keyboard=None, attachment=attachment_3)
                buttons = [
                    "Удалилить из избранного",
                    "Дальше",
                    "Вернуться в главное меню",
                ]
                but_col = self.but_col()
                keyboard = self.set_key_parameters(
                    buttons, [but_col[1], but_col[2], but_col[1]]
                )
                self.write_msg(user_id, "Выберите действие", keyboard)
                message, user_id = self.get_message()
                if message.lower() == "дальше":
                    the_end(user_id)
                elif message.lower() == "удалилить из избранного":
                    # тут удаляем из БД
                    unset_favorite(self.__session, user_id, user)
                    self.write_msg(user_id, "Анкета удалена", keyboard=None)
                    the_end(user_id)
                elif message.lower() == "вернуться в главное меню":
                    return self.start_bot()

    """Работа со списком мне нравится"""

    def show_like_list(self, user_id):
        def the_end(user_id):
            if count >= len(like_list) - 1:
                buttons = ["Вернуться в главное меню", "Показать мне нравится"]
                but_col = self.but_col()
                keyboard = self.set_key_parameters(buttons, [but_col[1], but_col[0]])
                self.write_msg(user_id, "Это была последняя анкета", keyboard)
                message, user_id = self.query_bot()
                if message.lower() == "вернуться в главное меню":
                    return self.start_bot()
                elif message.lower() == "показать мне нравится":
                    return self.show_like_list(user_id)

        # base_data = [1, 2]  # Тут вставить БД
        like_list = get_likes(self.__session, user_id)
        msg = "Мне нравится"
        self.write_msg(user_id, msg, keyboard=None)
        if like_list == []:
            msg = "Список мне нравится пуст!"
            but_col = self.but_col()
            keyboard = self.set_key_parameters("Вернуться в главное меню", but_col[1])
            self.write_msg(user_id, msg, keyboard)
            message, user_id = self.query_bot()
            if message == "вернуться в главное меню":
                return self.start_bot()
        elif like_list != []:
            for count, user in enumerate(like_list):
                info_user = self.__vk.get_user(user)
                attachment_1 = f"photo{info_user.photos[0]['owner_id']}_{info_user.photos[0]['id']}"
                attachment_2 = f"photo{info_user.photos[1]['owner_id']}_{info_user.photos[1]['id']}"
                attachment_3 = f"photo{info_user.photos[2]['owner_id']}_{info_user.photos[2]['id']}"
                self.write_msg(
                    user_id,
                    f"{info_user.name}, дата рождения {info_user.bdate}, {info_user.city}",
                    keyboard=None,
                    attachment=None,
                )
                self.write_msg(user_id, "", keyboard=None, attachment=attachment_1)
                self.write_msg(user_id, "", keyboard=None, attachment=attachment_2)
                self.write_msg(user_id, "", keyboard=None, attachment=attachment_3)
                buttons = [
                    "Удалилить из мне нравится",
                    "Дальше",
                    "Вернуться в главное меню",
                ]
                but_col = self.but_col()
                keyboard = self.set_key_parameters(
                    buttons, [but_col[1], but_col[2], but_col[1]]
                )
                self.write_msg(user_id, "Выберите действие", keyboard)
                message, user_id = self.get_message()
                if message.lower() == "дальше":
                    the_end(user_id)
                elif message.lower() == "удалилить из мне нравится":
                    # тут удаляем из БД
                    unset_like(self.__session, user_id, user)
                    self.write_msg(user_id, "Анкета удалена", keyboard=None)
                    the_end(user_id)
                elif message.lower() == "вернуться в главное меню":
                    return self.start_bot()

    """Работа с черным списком"""

    def show_black_list(self, user_id):
        def the_end(user_id):
            if count >= len(black_list) - 1:
                buttons = ["Вернуться в главное меню", "Показать черный список"]
                but_col = self.but_col()
                keyboard = self.set_key_parameters(buttons, [but_col[1], but_col[0]])
                self.write_msg(user_id, "Это была последняя анкета", keyboard)
                message, user_id = self.get_message()
                if message.lower() == "вернуться в главное меню":
                    return self.start_bot()
                elif message.lower() == "показать черный список":
                    return self.show_black_list(user_id)

        # base_data = [1, 2]  # Тут вставить БД
        black_list = get_blocklist(self.__session, user_id)
        msg = "Черный список"
        self.write_msg(user_id, msg, keyboard=None)
        if black_list == []:
            msg = "Черный список пуст!"
            but_col = self.but_col()
            keyboard = self.set_key_parameters("Вернуться в главное меню", but_col[1])
            self.write_msg(user_id, msg, keyboard)
            message, user_id = self.query_bot()
            if message == "вернуться в главное меню":
                return self.start_bot()
        elif black_list != []:
            for count, user in enumerate(black_list):
                info_user = self.__vk.get_user(user)
                attachment_1 = f"photo{info_user.photos[0]['owner_id']}_{info_user.photos[0]['id']}"
                attachment_2 = f"photo{info_user.photos[1]['owner_id']}_{info_user.photos[1]['id']}"
                attachment_3 = f"photo{info_user.photos[2]['owner_id']}_{info_user.photos[2]['id']}"
                self.write_msg(
                    user_id,
                    f"{info_user.name}, дата рождения {info_user.bdate}, {info_user.city}",
                    keyboard=None,
                    attachment=None,
                )
                self.write_msg(user_id, "", keyboard=None, attachment=attachment_1)
                self.write_msg(user_id, "", keyboard=None, attachment=attachment_2)
                self.write_msg(user_id, "", keyboard=None, attachment=attachment_3)
                buttons = [
                    "Удалилить из черного списка",
                    "Дальше",
                    "Вернуться в главное меню",
                ]
                but_col = self.but_col()
                keyboard = self.set_key_parameters(
                    buttons, [but_col[1], but_col[2], but_col[1]]
                )
                self.write_msg(user_id, "Выберите действие", keyboard)
                message, user_id = self.get_message()
                if message.lower() == "дальше":
                    the_end(user_id)
                elif message.lower() == "удалилить из черного списка":
                    # тут удаляем из БД
                    unset_blocklist(self.__session, user_id, user)
                    self.write_msg(user_id, "Анкета удалена", keyboard=None)
                    the_end(user_id)
                elif message.lower() == "вернуться в главное меню":
                    return self.start_bot()

    """Показ сообщения "Напишите возраст" и Возрат к выбору пола"""

    def back_to_gender(self, user_id):
        msg = "Напишите возраст особи цифрами, например 18."
        buttons = "Назад, к выбору пола."
        but_col = self.but_col()
        keyboard = self.set_key_parameters(buttons, but_col[1])
        return self.write_msg(user_id, msg, keyboard)

    """Показ сообщения "Напишите город для поиска" и Назад, к выбору возраста"""

    def back_to_age(self, user_id):
        msg = "Напишите город для поиска"
        buttons = "Назад, к выбору возраста."
        but_col = self.but_col()
        keyboard = self.set_key_parameters(buttons, but_col[1])
        return self.write_msg(user_id, msg, keyboard)

    """Обработка анкет, добавить в избранные, мне нравится или черный список"""

    def add_to_list(self, user_id):
        def the_end(user_id):
            if count >= len(self.result_requests_vkontakte) - 1:
                buttons = "Вернуться в главное меню"
                but_col = self.but_col()
                keyboard = self.set_key_parameters(buttons, but_col[1])
                self.write_msg(user_id, "Это была последняя анкета", keyboard)
                message, user_id = self.get_message()
                if message.lower() == "вернуться в главное меню":
                    return self.start_bot()

        # result_requests_vkontakte = []
        while True:
            usr = self.__vk.search_user_by_params(
                self.get_parametrs["sex"],
                self.get_parametrs["age"],
                self.get_parametrs["city"],
            )
            if not usr:
                break
            self.result_requests_vkontakte.append(usr)

        if self.result_requests_vkontakte == []:
            msg = "По вашему запросу анкет нет, измените параметры запроса!"
            but_col = self.but_col()
            keyboard = self.set_key_parameters("Вернуться в главное меню", but_col[1])
            self.write_msg(user_id, msg, keyboard)
            message, user_id = self.query_bot()
            if message == "вернуться в главное меню":
                return self.start_bot()
        elif self.result_requests_vkontakte != []:
            for count, info_user in enumerate(self.result_requests_vkontakte):
                self.get_parametrs["id"] = info_user.id
                if len(info_user.photos) >= 3:
                    attachment_1 = f"photo{info_user.photos[0]['owner_id']}_{info_user.photos[0]['id']}"
                    attachment_2 = f"photo{info_user.photos[1]['owner_id']}_{info_user.photos[1]['id']}"
                    attachment_3 = f"photo{info_user.photos[2]['owner_id']}_{info_user.photos[2]['id']}"
                else:
                    the_end(user_id)
                    continue
                self.write_msg(
                    user_id,
                    f"{info_user.name}, дата рождения {info_user.bdate}, {info_user.city}",
                    keyboard=None,
                    attachment=None,
                )
                self.write_msg(user_id, "", keyboard=None, attachment=attachment_1)
                self.write_msg(user_id, "", keyboard=None, attachment=attachment_2)
                self.write_msg(user_id, "", keyboard=None, attachment=attachment_3)
                buttons = [
                    "Добавить в избранное",
                    "Добавить в мне нравится",
                    "Добавить в черный список",
                    "Добавить в не нравится",
                    "Вернуться в главное меню",
                    "Дальше",
                ]
                but_col = self.but_col()
                keyboard = self.set_key_parameters(
                    buttons,
                    [
                        but_col[0],
                        but_col[0],
                        but_col[2],
                        but_col[2],
                        but_col[1],
                        but_col[3],
                    ],
                )
                self.write_msg(user_id, "Выберите действие", keyboard)
                message, user_id = self.get_message()
                if message.lower() == "добавить в избранное":
                    set_favorite(self.__session, user_id, info_user.id)
                    the_end(user_id)
                elif message.lower() == "добавить в мне нравится":
                    set_like(self.__session, user_id, info_user.id)
                    the_end(user_id)
                elif message.lower() == "добавить в черный список":
                    set_blocklist(self.__session, user_id, info_user.id)
                    the_end(user_id)
                elif message.lower() == "добавить в не нравится":
                    set_dislike(self.__session, user_id, info_user.id)
                    the_end(user_id)
                elif message.lower() == "дальше":
                    the_end(user_id)
                elif message.lower() == "вернуться в главное меню":
                    return self.start_bot()

    """Опрос пользователя для составления словаря для поиска."""

    def start_search(self, user_id):
        def search_age_city():
            message, user_id = self.query_bot()
            if message.lower() == "назад, к выбору пола.":
                return self.start_search(user_id)
            elif int(message) >= 18:
                self.get_parametrs["age"] = message
                self.back_to_age(user_id)
                message, user_id = self.query_bot()
                if message.lower() == "назад, к выбору возраста.":
                    self.back_to_gender(user_id)
                    search_age_city()
                else:
                    self.get_parametrs["city"] = message
                    msg = "Данные записаны, начинаем поиск!"
                    self.write_msg(user_id, msg, keyboard=None)
            elif int(message) < 18:
                msg = "Аккуратно! Статься 134 УК РФ!"
                self.write_msg(user_id, msg, keyboard=None)
                # time.sleep(5)
                return self.start_search(user_id)

        self.get_parametrs = {}
        msg = "Выберите пол особи"
        buttons = [
            "Особь женского пола",
            "Особь мужского пола",
            "Вернуться в главное меню",
        ]
        but_col = self.but_col()
        keyboard = self.set_key_parameters(
            buttons, [but_col[0], but_col[2], but_col[1]]
        )
        self.write_msg(user_id, msg, keyboard)
        message, user_id = self.query_bot()
        if message.lower() == "особь женского пола":
            self.get_parametrs[
                "sex"
            ] = "1"  # ВОТ ТУТ НЕ ЗНАЮ В ОТВЕТЕ ОТ ВКОНТАКТЕ ЧТО ПЕРЕДАЕТСЯ INT ИЛИ STR
            self.back_to_gender(user_id)
            search_age_city()
        elif message.lower() == "особь мужского пола":
            self.get_parametrs[
                "sex"
            ] = "2"  # ВОТ ТУТ НЕ ЗНАЮ В ОТВЕТЕ ОТ ВКОНТАКТЕ ЧТО ПЕРЕДАЕТСЯ INT ИЛИ STR
            self.back_to_gender(user_id)
            search_age_city()
        elif message == "вернуться в главное меню":
            return self.start_bot()


def main(vk: VKConnector):
    # Основной цикл
    vk_session = VkBot("config.ini", vk)
    message, user_id = vk_session.query_bot()
    if message.lower() == "1" or message.lower() in {"старт", "start", "привет", "hi"}:
        """Показывает главное меню"""
        vk_session.start_bot()
        """Следующий запрос на сообщение боту"""
    elif message.lower() == "избранные":
        vk_session.show_favorites_list(user_id)
    elif message.lower() == "мне нравится":
        vk_session.show_like_list(user_id)
    elif message.lower() == "черный список":
        vk_session.show_black_list(user_id)
    elif message.lower() == "начать поиск":
        vk_session.start_search(user_id)
        res = vk_session.get_parametrs  # Для поиска по Вконтакте
        if res:
            # time.sleep(3)
            vk_session.add_to_list(user_id)
    elif message.lower() == "завершить работу с ботом":
        msg = "До свидания"
        vk_session.write_msg(user_id, msg, keyboard=None)
        sys.exit()
