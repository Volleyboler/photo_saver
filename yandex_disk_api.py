import requests


class YandexDisk:
    def __init__(self, token):
        self.headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'Authorization': f'OAuth {token}'}

    def check_access(self):
        """
        Метод проверки доступа к яндекс диску
        :return: объект ответа на запрос
        """
        access_status = requests.get(
            'https://cloud-api.yandex.net/v1/disk',
            headers=self.headers
        )
        return access_status

    def create_folder(self, path: str):
        """
        Метод создания папки в яндекс диске
        :param path: путь к папке
        :return: объект ответа на запрос
        """
        creation_status = requests.put(
            'https://cloud-api.yandex.net/v1/disk/resources',
            params={
                'path': path,
            },
            headers=self.headers
        )
        return creation_status

    def upload_file(self, path: str, url_source: str):
        """
        Метод создания папки в яндекс диске
        :param url_source: источник файла - url адрес
        :param path: путь к папке и имя файла
        :return: объект ответа на запрос
        """
        upload_status = requests.post(
            'https://cloud-api.yandex.net/v1/disk/resources/upload',
            params={
                'path': path,
                'url': url_source
            },
            headers=self.headers
        )
        return upload_status
