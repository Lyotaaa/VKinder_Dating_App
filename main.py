from Vk_bot.Vk_bot_class import main, open_user_token, VKConnector

if __name__ == "__main__":
    vk = VKConnector(open_user_token("config.ini"))
    while True:
        main(vk)
