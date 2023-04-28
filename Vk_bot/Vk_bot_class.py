import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from configparser import ConfigParser
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sys
import time


def open_a_token(file_name):
    """Открытие токана для бота"""
    cofing = ConfigParser()
    cofing.read(file_name)
    group_token = cofing["Vk_info"]["group_token"]
    return group_token


class VkBot:
    def __init__(self, open_a_token):
        """Подключение к боту"""
        self.vk_session = vk_api.VkApi(token=open_a_token)
        self.vk_api = self.vk_session.get_api()
        self.long_pool = VkLongPoll(self.vk_session)

    def write_msg(self, user_id,message, keyboard=None, attachment=None):
        """Сообщение от бота: кому, сообщение, id собщения, кнопки, картинки"""
        post = {
            "user_id": user_id,
            "message": message,
            "random_id": randrange(10**7),
        }
        if keyboard != None:
            post["keyboard"] = keyboard.get_keyboard()
        else:
            post = post
        if attachment != None:
            post["attachment"] = attachment
        else:
            post = post
        self.vk_session.method("messages.send", post)

    def but_col(self):
        """Список цветов"""
        buttons_colors = [
            VkKeyboardColor.POSITIVE,
            VkKeyboardColor.NEGATIVE,
            VkKeyboardColor.PRIMARY,
            VkKeyboardColor.SECONDARY,
        ]
        return buttons_colors

    def set_key_parameters(self, buttons, but_col):
        """Задаём цвет, количество кнопок в ответе бота"""
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

    def get_message(self):
        """Собщения боту от пользователя"""
        for event in self.long_pool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                message = event.text.lower()
                user_id = event.user_id
                return message, user_id

    def command_list_output(self):
        """Приветствие"""
        response = "Добро пожаловать в бот Vkinder.\nВыберите команду!"
        return response

    def favorites_list(self):
        """Список избранных"""
        return [1, 2, 3]  # Должен вернуть список избраных пользователей,
        # при выборе пользователя, должен вывести фотографии и страницу
        # так возможность удалить его из это БД

    def like_list(self):
        """Список мне нравится"""
        return [1, 2, 3]  # Должен вернуть список понравившехся пользователей,
        # при выборе пользователя, должен вывести фотографии и страницу
        # так же возможность удалить пользователя из БД

    def black_list(self):
        """Черный список"""
        return [1, 2, 3]  # Должен вернуть черный список пользователей,
        # при выборе пользователя, должен вывести фотографии и страницу
        # так же возможность удалить его из БД

    
    # Кнопки главного меню
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
        return message, self.user_id
    
    """Показать гавлное меню"""
    def show_main_menu(self):
        # msg, user_id = self.query_bot()
        keyboard = self.greetings_bot()
        self.write_msg(self.user_id, self.command_list_output(), keyboard)

    """Стартовое меню"""
    def start_bot(self):
        self.show_main_menu()

    """Вывести список избранных"""
    def favorites_search(self, user_id):
        result = self.favorites_list()
        if result == []:
            msg = "Список избранных пуст"
            but_col = self.but_col()
            keyboard = self.set_key_parameters(
                "Вернуться в главное меню", but_col[1]
            )
            self.vk_session.write_msg(user_id, msg, keyboard)
            message, user_id = self.query_bot()
            if message == "вернуться в главное меню":
                self.start_bot()
                main()
        else:
            msg = "Избранные"
            buttons = ["Удалилить из избранного", "Вернуться в главное меню"]
            but_col = self.but_col()
            keyboard = self.set_key_parameters(buttons, [but_col[1], but_col[0]])
            self.write_msg(user_id, msg, keyboard=None)
            for i in result:
                self.write_msg(user_id, i, keyboard=None)
            self.write_msg(user_id, "Выберите команду", keyboard)
            message, user_id = self.query_bot()
            if message == "вернуться в главное меню":
                self.start_bot()
                main()
            elif message.lower() == "удалилить из избранного":
                pass  # Тут работа с БД

    """Вывести список мне нравится"""
    def like_search(self, user_id):
        result = self.like_list()
        if result == []:
            msg = "Список понравившихся пуст"
            but_col = self.but_col()
            keyboard = self.set_key_parameters(
                "Вернуться в главное меню", but_col[1]
            )
            self.write_msg(user_id, msg, keyboard)
            message, user_id = self.query_bot()
            if message == "вернуться в главное меню":
                self.start_bot()
                main()
        else:
            msg = "Мне нравится"
            buttons = ["Удалилить из понравившихся", "Вернуться в главное меню"]
            but_col = self.but_col()
            keyboard = self.set_key_parameters(buttons, [but_col[1], but_col[0]])
            self.write_msg(user_id, msg, keyboard=None)
            for i in result:
                self.write_msg(user_id, i, keyboard=None)
            self.write_msg(user_id, "Выберите команду", keyboard)
            message, user_id = self.query_bot()
            if message == "вернуться в главное меню":
                self.start_bot()
                main()
            elif message.lower() == "удалилить из понравившихся":
                pass  # Тут работа с БД

    """Вывести черный список"""
    def black_search(self, user_id):
        result = self.black_list()
        if result == []:
            msg = "Черный список пуст"
            but_col = self.but_col()
            keyboard = self.set_key_parameters(
                "Вернуться в главное меню", but_col[1]
            )
            self.write_msg(user_id, msg, keyboard)
            message, user_id = self.query_bot()
            if message == "вернуться в главное меню":
                self.start_bot()
                main()
        else:
            msg = "Черный список"
            buttons = ["Удалилить из черного списка", "Вернуться в главное меню"]
            but_col = self.but_col()
            keyboard = self.set_key_parameters(buttons, [but_col[1], but_col[0]])
            self.write_msg(user_id, msg, keyboard=None)
            for i in result:
                self.write_msg(user_id, i, keyboard=None)
            self.write_msg(user_id, "Выберите команду", keyboard)
            message, user_id = self.query_bot()
            if message == "вернуться в главное меню":
                self.start_bot()
                main()
            elif message.lower() == "удалилить из черного списка":
                pass  # Тут работа с БД

    """Показ сообщения "Напишите возраст" и Возрат к выбору пола"""
    def back_to_gender(self, user_id):
        msg = "Напишите возраст особи"
        buttons = "Назад, к выбору пола."
        but_col = self.but_col()
        keyboard = self.set_key_parameters(buttons, but_col[1])
        self.write_msg(user_id, msg, keyboard)

    """Показ сообщения "Напишите город для поиска" и Назад, к выбору возраста"""
    def back_to_age(self, user_id):
        msg = "Напишите город для поиска"
        buttons = "Назад, к выбору возраста."
        but_col = self.but_col()
        keyboard = self.set_key_parameters(buttons, but_col[1])
        self.write_msg(user_id, msg, keyboard)

    """Опрос пользователя для составления словаря для поиска."""
    def start_search(self, user_id):
        def search_age_city():
            message, user_id = self.query_bot()
            if message.lower() == "назад, к выбору пола.":
                self.start_search(user_id)
            elif int(message) >= 18:
                get_parametrs["age"] = message
                self.back_to_age(user_id)
                message, user_id = self.query_bot()
                if message.lower() == "назад, к выбору возраста.":
                    self.back_to_gender(user_id)
                    search_age_city()
                else:
                    get_parametrs["city"] = message
                    msg = "Данные записаны, начинаем поиск!"
                    self.write_msg(user_id, msg, keyboard=None)
            elif int(message) < 18:
                msg = "Аккуратно! Статься 134 УК РФ!"
                self.write_msg(user_id, msg, keyboard=None)
                time.sleep(5)
                self.start_search(user_id)

        get_parametrs = {}
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
            get_parametrs[
                "sex"
            ] = "1"  # ВОТ ТУТ НЕ ЗНАЮ В ОТВЕТЕ ОТ ВКОНТАКТЕ ЧТО ПЕРЕДАЕТСЯ INT ИЛИ STR
            self.back_to_gender(user_id)
            search_age_city()
        elif message.lower() == "особь мужского пола":
            get_parametrs[
                "sex"
            ] = "2"  # ВОТ ТУТ НЕ ЗНАЮ В ОТВЕТЕ ОТ ВКОНТАКТЕ ЧТО ПЕРЕДАЕТСЯ INT ИЛИ STR
            self.back_to_gender(user_id)
            search_age_city()
        elif message == "вернуться в главное меню":
            self.start_bot()
            main()


def main():
    
# Основной цикл
    vk_session = VkBot(open_a_token("confing.ini"))
    message, user_id = vk_session.query_bot()
    get_parametrs = []
    if message.lower() == "1":
        """Показывает главное меню"""
        vk_session.start_bot()
        """Следующий запрос на сообщение боту"""
    elif message.lower() == "избранные":
        vk_session.favorites_search(user_id)
    elif message.lower() == "мне нравится":
        vk_session.like_search(user_id)
    elif message.lower() == "черный список":
        vk_session.black_search(user_id)
    elif message.lower() == "начать поиск":
        vk_session.start_search(user_id)
    elif message.lower() == "завершить работу с ботом":
        msg = "До свидания"
        vk_session.write_msg(user_id, msg, keyboard=None)
        sys.exit()

    return get_parametrs

if __name__ == "__main__":
    while True:
        main()
        
        