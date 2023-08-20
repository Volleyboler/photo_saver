import requests
from datetime import datetime


class VK:
    sizes_of_photo = {'s': 0, 'm': 1, 'x': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'y': 7, 'z': 8, 'w': 9}

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        """
        Метод получения информации о пользователе, используется для проверки доступа
        :return:
        """
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response

    def get_user_photos(self, owner_id):
        """
       Метод получения всех фото в альбоме профиля пользователя
       :param owner_id: id пользователя, по которому запрашивается информация
       :return: объект ответа на запрос
       """
        info_resp = requests.get(
            'https://api.vk.com/method/photos.get',
            params={
                'access_token': self.token,
                'v': self.version,
                'album_id': 'profile',
                'extended': 1,
                'owner_id': owner_id,
                'photo_sizes': 1,
            }
        )
        return info_resp

    def get_list_of_biggest_photos(self, amount_photo):
        """
        Метод получения списка фото самого большого размера, с информацией по каждому
        :param amount_photo: Количество запрошенных фото
        :return:
        """
        response_vk_json = self.get_user_photos(self.id).json()
        amount_photo_in_album = response_vk_json.get('response').get('count')
        if amount_photo > amount_photo_in_album:
            amount_photo = amount_photo_in_album
        photo_list = response_vk_json.get('response').get('items')
        info_photos = []

        for photo in photo_list:
            likes_amount = photo.get('likes').get('count')
            date_time_posted_photo = datetime.fromtimestamp(photo.get('date'))
            date_posted_photo = str(date_time_posted_photo).split(' ')[0]
            max_size = -1
            current_url = ''
            photo_size_type = ''
            for size in photo.get('sizes'):
                photo_size_type = size.get('type')
                if self.sizes_of_photo[photo_size_type] > max_size:
                    max_size = self.sizes_of_photo[photo_size_type]
                    current_url = size.get('url')
            info_photos.append((max_size, (likes_amount, date_posted_photo, current_url, photo_size_type)))
        info_photos.sort(reverse=True)
        photos_list_cutted_by_requested_amount = []
        for photo in info_photos[:amount_photo]:
            photos_list_cutted_by_requested_amount.append(photo[1])
        photos_list_cutted_by_requested_amount.sort()
        return photos_list_cutted_by_requested_amount


