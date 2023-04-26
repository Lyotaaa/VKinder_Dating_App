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
        buttons_colors = [
            VkKeyboardColor.POSITIVE,
            VkKeyboardColor.NEGATIVE,
            VkKeyboardColor.PRIMARY,
            VkKeyboardColor.SECONDARY,
        ]
        return buttons_colors

    def set_key_parameters(self, buttons, but_col):
        """Задаём цвет, количество кнопок в ответе бота"""
        keyboard = VkKeyboard()
        if not isinstance(buttons, list) and not isinstance(but_col, list):
            buttons = [buttons]
            but_col = [but_col]
        count = 0
        for bnt, bnt_colors in zip(buttons, but_col):
            if count == 2:
                keyboard.add_line()
            keyboard.add_button(bnt, bnt_colors)
            count += 1 
        keyboard.add_line()
        keyboard.add_button("Отмена", self.but_col()[1])
        return keyboard

    def get_message(self):
        """Собщения боту от пользователя"""
        for event in self.long_pool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                message = event.text.lower()
                user_id = event.user_id
                return message, user_id

    def command_list_output(self):
        response = """
Добро пожаловать в бот Vkinder.
"""
        return response


if __name__ == "__main__":
    while True:
        vk_session = VkBot(open_a_token("confing.ini"))
        query = vk_session.get_message()
        message, user_id = query
        if message == "1":
            buttons = ["kek", "cheburek"]
            bot_col = vk_session.but_col()
            keyboard = vk_session.set_key_parameters(buttons, [bot_col[0], bot_col[1]])
            vk_session.write_msg(user_id, vk_session.command_list_output(), keyboard)
        elif message == "2":
            vk_session.write_msg(user_id, "See you later", keyboard)
            break
