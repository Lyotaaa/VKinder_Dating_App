
import requests

VK_TOKEN_FILENAME = "vk_token.txt"

class VKException(Exception):
    """
    Класс для ошибок, возникающих при доступе к VK
    """
    pass


class VKUser():
    """
    Класс для хранения данных о пользователе VK
    """

    def __init__(self, id: str, name: str, bdate: str, sex: str, city: str, photo, photos: list):
        if id == None or id == "":
            raise VKException(f'VKUser: id пользователя не может быть пустым')
        if name == None or name == "":
            raise VKException(f'VKUser: Имя пользователя не может быть пустым')
        if bdate == None or bdate == "":
            raise VKException(f'VKUser: Дата рождения пользователя не может быть пустой')
        if sex == None or sex == "":
            raise VKException(f'VKUser: Пол пользователя не может быть пустым')
        if  city == None or city == "":
            raise VKException(f'VKUser: Город проживания пользователя не может быть пустым')
        self.__id = id
        self.__name = name
        self.__bdate = bdate
        self.__sex = sex
        self.__city = city
        self.__photo = photo
        self.__photos = photos

    def __repr__(self):
        return f'VKUser({self.__id}, "{self.__name}", {self.__bdate}, {self.__sex}, "{self.__city}", "{self.url}")'

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def bdate(self):
        return self.__bdate

    @property
    def sex(self):
        return self.__sex

    @property
    def city(self):
        return self.__city

    @property
    def url(self):
        return f'https://vk.com/id{self.__id}'

    @property
    def photo(self):
        return self.__photo

    @property
    def photos(self):
        return self.__photos

    @photos.setter
    def photos(self, ph):
        if isinstance(ph, list):
            self.__photos = ph

class VKConnector:
    """
    Класс для работы с VK
    """
    def __init__(self):
        with open(VK_TOKEN_FILENAME, "r", encoding="utf-8") as inf:
            token = inf.readline()
            if token == None or token == "":
                raise VKException(f'Не возможно считать токен из файла "{VK_TOKEN_FILENAME}"')
            self.token = token
            self.version = '5.89'
            self.params = {'access_token': self.token, 'v': self.version}
            self.__searches = {}

    def get_user_info(self, id: str) -> dict:
        """
        Возвращает информацию о пользователе
        :return:
        """
        url = 'https://api.vk.com/method/users.get'
        params = {
            'user_ids': id,
            "fields":"education,sex,bdate,city"
        }
        response = requests.get(url, params={**self.params, **params})
        if response.status_code != 200:
            raise(VKException(f'get_user_info: Ошибка при запросе фото'))
        return response.json()


    def get_user(self, id: str) -> VKUser:
        ud = self.get_user_info(id)
        photos_list, photos = self.get_user_photos(id), []
        if photos_list:
            photos = sorted(photos_list, key=lambda p: int(p["likes"]), reverse=True)[:3]

        return VKUser(ud["response"][0]["id"],
                      ud["response"][0]["first_name"] + ' ' + ud["response"][0]["last_name"],
                      ud["response"][0]["bdate"], ud["response"][0]["sex"],
                      ud["response"][0]["city"]["title"], photos)

    def _is_img_type_better(self, type1, type2):
        """
        Сравнивает типы аватарок. Нужно для того, чтобы выбрать бОльшую по размеру.
        Связано с тем, что иногда VK не возвращает размер фото, и нужно смотреть на тип
        :return:
        """
        types = ['s', 'm', 'o', 'p', 'q', 'r', 'x', 'y', 'z', 'w']

        if type1 in types and type2 in types and types.index(type1) > types.index(type2):
            return False
        return True

    def get_user_photos(self, id: str, offset=0, number=200):
        """
        Возвращает number фото, загруженных пользователем owner
        :param query:
        :return:
        """
        photo_params = {
            "owner_id": id,
            # "album_id": "profile",
            "extended": 1,
            "offset": offset,
            "count": number
        }

        result = requests.get(
            "https://api.vk.com/method/photos.getAll",
            params={**self.params, **photo_params})
        if result.status_code != 200:
            raise(VKException(f'get_user_photos: Ошибка при запросе фото'))
        if "response" not in result.json():
            return []
        ret = []
        for ph in result.json()["response"]["items"]:
            size, url, img_type = None, None, None
            for s in ph["sizes"]:
                if not url or int(s["height"]) + int(s["width"]) > size or \
                        self._is_img_type_better(img_type, s["type"]):
                    size = int(s["height"]) + int(s["width"])
                    url = s["url"]
                    img_type = s["type"]
            ret.append({"likes": ph["likes"]["count"], "date": ph["date"], "url": url, "type": img_type})
        return ret

    def search_users(self, sex: int, age: int, city: str) -> list:
        """
        Ищет пользователей по параметрам
        """
        url = 'https://api.vk.com/method/users.search'
        params = {
            'user_ids': id,
            "fields":"education,sex,bdate,city,photo_max_orig",
            "hometown": city,
            "sex": sex,
            "status": 6,
            "age_from": age,
            "age_to": age,
            "has_photo": 1,
            "is_closed": 0,
            "count": 1000
        }
        response = requests.get(url, params={**self.params, **params})
        if response.status_code != 200:
            raise(VKException(f'search_user_info: Ошибка при поиске пользователя'))
        return response.json()

    def get_search_results(self, sex: int, age: int, city: str):
        """
        Возвращает результаты поиска пользователей ВК
        """
        ud = self.search_users(sex, age, city)
        results = []
        if isinstance(ud, dict) and "response" in ud and "items" in ud["response"] and \
            isinstance(ud["response"]["items"], list) and len(ud["response"]["items"]):
            for u in ud["response"]["items"]:
                if "bdate" in u and "city" in u:
                    results.append(VKUser(u["id"], u["first_name"] + ' ' + u["last_name"],
                                          u["bdate"], u["sex"], u["city"]["title"], u["photo_max_orig"], None))
        self.__searches[f'{sex}-{age}-{city.lower()}'] = {"next_ind": 0, "results": results}

    def search_user_by_params(self, sex: int, age: int, city: str) -> VKUser:
        """
        Возвращает результаты поиска пользователя ВК по параметрам
        """
        skey = f'{sex}-{age}-{city.lower()}'
        if skey not in self.__searches:
            self.get_search_results(sex, age, city)

        next_ind = self.__searches[skey]["next_ind"]
        search_results = self.__searches[skey]["results"]
        if next_ind >= len(self.__searches[skey]["results"]):
            return None
        next_user = search_results[next_ind]
        self.__searches[skey]["next_ind"] = next_ind + 1

        if next_user.photos == None:
            photos_list, photos = self.get_user_photos(next_user.id), []
            if photos_list:
                photos = sorted(photos_list, key=lambda p: int(p["likes"]), reverse=True)[:3]
            next_user.photos = photos

        return next_user
def main():
    vk = VKConnector()
    # usr = vk.get_user("763904")
    # print(usr)
    print(vk.search_user_by_params(1, 30, "москва"))
    print(vk.search_user_by_params(1, 25, "казань"))
    print(vk.search_user_by_params(1, 18, "красноярск"))
    print(vk.search_user_by_params(1, 40, "санкт-петербург"))
    for _ in range(10):
        usr = vk.search_user_by_params(1, 30, "москва")
        print(usr)
        if len(usr.photos) > 2:
            print(usr.photos[0])
            print(usr.photos[1])
            print(usr.photos[2])

if __name__ == "__main__":
    main()