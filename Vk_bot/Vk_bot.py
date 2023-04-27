import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from configparser import ConfigParser
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


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

    def write_msg(self, user_id, message, keyboard=None, attachment=None):
        """Сообщение от бота: кому, сообщение, id собщения, кнопки, картинки"""
        post = {
            "user_id": user_id,
            "message": message,
            "random_id": randrange(10**7),
        }
        if attachment != None:
            post["attachment"] = attachment
        else:
            post = post
        if keyboard != None:
            post["keyboard"] = keyboard.get_keyboard()
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
        keyboard = VkKeyboard(inline=True)
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
        # keyboard.add_line()
        # keyboard.add_button("Отмена", self.but_col()[1])
        return keyboard

    def get_message(self):
        """Собщения боту от пользователя"""
        for event in self.long_pool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                message = event.text.lower()
                user_id = event.user_id
                return message, user_id

    def command_list_output(self):
        response = "Добро пожаловать в бот Vkinder."
        return response

    # Кнопки главного меню
    def greetings_bot(self):
        buttons = [
            "Вывести избранных",
            "Вывести черный список",
            "Вывести понравившихся",
            "Начать поиск",
            "Завершить работу с ботом",
        ]
        but_col = vk_session.but_col()
        keyboard = vk_session.set_key_parameters(
            buttons, [but_col[3], but_col[3], but_col[3], but_col[0], but_col[1]]
        )
        return keyboard

    # Показать гавлное меню
    def show_main_menu(self):
        keyboard = self.greegreetings_bot()
        vk_session.write_msg(user_id, vk_session.command_list_output(), keyboard)

    def favorites_list(self):
        pass  # Должен вернуть список избраных пользователей,
        # при выборе пользователя, должен вывести фотографии и страницу
        # так возможность удалить его из это БД

    def like_list(self):
        pass  # Должен вернуть список понравившехся пользователей,
        # при выборе пользователя, должен вывести фотографии и страницу
        # так же возможность удалить пользователя из БД

    def black_list(self):
        pass  # Должен вернуть черный список пользователей,
        # при выборе пользователя, должен вывести фотографии и страницу
        # так же возможность удалить его из БД


if __name__ == "__main__":
    while True:
        vk_session = VkBot(open_a_token("confing.ini"))
        message, user_id = vk_session.get_message()
        if message.lower() == "привет":
            # Показывает главное меню
            vk_session.show_main_menu()
            # Следующий запрос на сообщение боту
            message, user_id = vk_session.get_message()
            if message.lower() == "Вывести избранных":
                result = vk_session.favorites_list()
                if result == []:
                    msg = "Список избранных пуст"
                    but_col = vk_session.but_col()
                    keyboard = vk_session.set_key_parameters(
                        "Вернуться в главное меню", but_col[1]
                    )
                    vk_session.write_msg(user_id, msg, keyboard)
                else:
                    msg = "Список избранных"
                    buttons = "Вернуться в главное меню"
                    but_col = vk_session.but_col()
                    keyboard = vk_session.set_key_parameters(buttons, but_col()[1])
                    vk_session.set_key_parameters(
                        "Вернуться в главное меню", vk_session.but_col()[1]
                    )
                    vk_session.write_msg(
                        user_id,
                    )
            elif message == "Вывести понравившихся":
                result = vk_session.like_list()
                if result == []:
                    msg = "Список понравившихся пуст"
                    but_col = vk_session.but_col()
                    keyboard = vk_session.set_key_parameters("Назад", but_col[1])
                else:
                    msg = "Список понравившихся"
                    result  # # Дальше управление с Бот и БД, удалить, перенести и т.д

                # vk_session.
            elif message == "Вывести черный список":
                if black_list == []:
                    msg = "Черный список пуст"
                    but_col = vk_session.but_col()
                    keyboard = vk_session.set_key_parameters("Назад", but_col[1])
                    vk_session.write_msg(user_id, msg, keyboard)
                else:
                    msg = "Черный список"
                    get_black_list()  # Дальше управление с Бот и БД, удалить, перенести и т.д
            elif message.lower() == "завершить работу с ботом":
                msg = "До свидания"
                vk_session.write_msg(user_id, msg, keyboard=None)
                break
            elif message == "Назад":
                keyboard = greetings_bot()
                vk_session.write_msg(
                    user_id, vk_session.command_list_output(), keyboard
                )
            elif message == "Начать поиск":
                msg = "Выберите пол особи"
                buttons = ["Особь женского пола", "Особь мужского пола"]
                keyboard = vk_session.set_key_parameters(
                    buttons, [but_col[0], but_col[2]]
                )
                vk_session.write_msg(user_id, msg, keyboard)
                message, user_id = vk_session.get_message()
                if message == "Особь женского пола":
                    msg = "Выбирете возсрат особи"
                    buttons = ["18-25", "26-35", "36-45", "46-55", "56+", "Назад"]
                    keyboard = vk_session.set_key_parameters(
                        buttons,
                        [
                            but_col[3],
                            but_col[3],
                            but_col[3],
                            but_col[3],
                            but_col[3],
                            but_col[1],
                        ],
                    )
                    vk_session.write_msg(user_id, msg, keyboard)
                    message, user_id = vk_session.get_message()
                    if message in ["18-25", "26-35", "36-45", "46-55", "56+"]:
                        msg = "Выбирете "
                        buttons = ["18-25", "26-35", "36-45", "46-55", "56+", "Назад"]
