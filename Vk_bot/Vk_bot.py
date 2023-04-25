import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from configparser import ConfigParser


def open_a_token(file_name):
    cofing = ConfigParser()
    cofing.read(file_name)
    group_token = cofing["Vk_info"]["group_token"]
    return group_token


class VkBot:
    def __init__(self, open_a_token):
        self.vk_session = vk_api.VkApi(token=open_a_token)
        self.vk_api = self.vk_session.get_api()
        self.long_pool = VkLongPoll(self.vk_session)

    def write_msg(self, user_id, message, attachment=None):
        self.vk_session.method(
            "messages.send",
            {
                "user_id": user_id,
                "message": message,
                "random_id": randrange(10**7),
                "attachment": attachment,
            },
        )

    def get_message(self):
        for event in self.long_pool.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    message = event.text.lower()
                    user_id = event.user_id
                    return message, user_id

    def command_list_output(self):
        response = """
Добро пожаловать в бот Vkinder.
Список доступных команд для работы со мной.
Команда "найти" или "0" - запускает процесс поиска пользователей;
Команда "мне нравится" или "1" - выведет список пользователей, которым Вы поставили мне нравится.
Команда "черный список" или "2" - покажет, пользователей в черном списке.
Команда "избранные" или "3" - покажет избранных пользователей.
"""
        return response


if __name__ == "__main__":
    while True:
        vk_session = VkBot(open_a_token("confing.ini"))
        query = vk_session.get_message()
        message, user_id = query
        if message == "привет":
            vk_session.write_msg(user_id, vk_session.command_list_output())
