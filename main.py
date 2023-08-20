import vk_api as vk
import yandex_disk_api as yad
from vk_app_token import access_token
import json
from tqdm import tqdm


"""
Токен доступа к API VK находится в файле "vk_app_token", переменная access_token = ""
"""


def input_user_id_vk():
    """
    Метод получения id Вконтакте от пользователя
    :return:
    """
    while True:
        user_id = input('Введите id пользователя VK:\n')
        vk_access = vk.VK(access_token, user_id)
        if 300 > vk_access.users_info().status_code >= 200:
            return user_id, vk_access
        else:
            print(f'Пользователя с id - {user_id} не существует, либо нет доступа')


def input_yandex_disk_token():
    """
    Метод получения токена доступа к яндекс диску от пользователя
    :return:
    """
    while True:
        yad_token = input('Введите токен доступа к Яндекс Диску:\n')
        yad_access = yad.YandexDisk(yad_token)
        check = yad_access.check_access().status_code
        if check == 200:
            return yad_access
        else:
            print(f'Ошибка доступа. {check.json().get("message")}')


def input_amount_photo_to_save():
    """
    Метод получения количества фото для загрузки от пользователя, по умолчанию 5.
    :return:
    """
    while True:
        amount_photo = input('Введите количество фотографий из альбома - '
                             '"Профиль", которые вы хотите сохранить в облаке'
                             '(при некорректном вводе будет принято значение по умолчанию - 5):\n')
        try:
            int(amount_photo)
            print(f'Будут сохранены {amount_photo} фотографий из альбома "Профиль"')
            return int(amount_photo)
        except():
            print(f'Некорректный ввод. Будут сохранены 5 фотографий из альбома "Профиль"')
            return 5


def get_pictures_info_to_upload(final_amount_photos: int, items_for_json: list, user_id: str):
    """
    метод создает в папке "results" json файл с информацией о загруженных фотографиях на яндекс диск
    :param final_amount_photos: количество загруженных фото
    :param items_for_json: информация по фото
    :param user_id:
    :return:
    """
    data = {'count': final_amount_photos, 'items': items_for_json}
    with open(f'results/results_{user_id}.json', 'w', encoding='utf8') as f:
        json.dump(data, f)


def main():
    user_id, vk_access = input_user_id_vk()
    yad_access = input_yandex_disk_token()
    folder_name = f'photo_vk_id{user_id}'
    amount_photos = input_amount_photo_to_save()
    photos_info = vk_access.get_list_of_biggest_photos(amount_photos)
    final_amount_photos = len(photos_info)
    yad_access.create_folder(folder_name)
    items_for_json = []
    flag_for_adding_data_in_file_name = False
    for count, photo in tqdm(enumerate(photos_info), ncols=80, ascii=True, desc='Total', unit=' file is saving'):
        if not flag_for_adding_data_in_file_name and photo[0] != photos_info[0]:
            file_name = f'{photo[0]}.jpg'
        else:
            if flag_for_adding_data_in_file_name and photo[0] != photos_info[0]:
                flag_for_adding_data_in_file_name = False
            elif not flag_for_adding_data_in_file_name and photo[0] == photos_info[0]:
                flag_for_adding_data_in_file_name = True
            file_name = f'{photo[0]}_{photo[1]}.jpg'
        items_for_json.append({"file_name": file_name, "size": photo[3]})
        yad_access.upload_file(f'{folder_name}/{file_name}', photo[2])
    get_pictures_info_to_upload(final_amount_photos, items_for_json, user_id)
    print('Загрузка завершена')


if __name__ == '__main__':
    main()
