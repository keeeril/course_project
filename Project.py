import requests
from pprint import pprint
import json
import os
import glob

with open('/Users/keeeril/Desktop/token.txt', 'rt', encoding='utf-8') as file:
    token = file.readline()

def get_photo(ident):
    url = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': ident,
        'album_id': 'profile',
        'access_token': token,
        'v': '5.131',
        'rev': '1',
        'extended': 1
    }

    files = {}

    response = requests.get(url, params=params)
    response_outfit = response.json()
    for albums in response_outfit['response']['items']:
        ph_name = albums['likes']['count']
        if ph_name in files:
            ph_name = str(ph_name) + ' ' + str(albums['date'])
        else:
            ph_name = ph_name
        quality_list = []
        for i in albums['sizes']:
        #     print(i)
        #     quality_list.append(i['width'])
        #     max_quality = max(quality_list)
        #     print(max_quality)
        # if max_quality in str(i['width']):
        #     ph_url = i['url']
            if 'w' in i['type']:
                quality = i['width']
                quality_list.append(quality)
            elif 'z' in i['type']:
                ph_url = i['url']
            elif 'y' in i['type']:
                ph_url = i['url']
            elif 'r' in i['type']:
                ph_url = i['url']
        files[ph_name] = ph_url
    return files

ident = int(input('Введите ID VK: '))
def upload_files(yandex_token):
    files = get_photo(ident)
    counter = 0
    headers = {
            "Accept": "application/json",
            "Authorization": "OAuth " + yandex_token
    }
    params = {
            'path':'course/'
    }

    url = "https://cloud-api.yandex.net/v1/disk/resources"
    r = requests.put(url=url, params=params, headers=headers)

    for name_photo, file_url in files.items():
        headers = {
            "Accept": "application/json",
            "Authorization": "OAuth " + yandex_token
        }

        params = {
            'path':'course/' + str(name_photo),
            'url': file_url
        }

        url = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
        r = requests.post(url=url, params=params, headers=headers)
        res = r.json()
        counter += 1
        print(f'Загружено {counter} из {len(files)}')
    print('Загрузка завершена!')
        # print(json.dumps(res, sort_keys=True, indent=4, ensure_ascii=False))
yandex_token = str(input('Ввеите токен яндекс: '))
upload_files(yandex_token)
