import requests
from urllib.parse import urlparse
from environs import Env

env = Env()
env.read_env()

token = env.str('token')

def shorten_link(token, url):
    params = {
        'access_token': token,
        'url': url,
        'v': '5.199'
    }
    response = requests.get('https://api.vk.com/method/utils.getShortLink', params=params)
    response.raise_for_status()
    data = response.json()

    if 'response' not in data:
        raise requests.exceptions.HTTPError('Ошибка при сокращении ссылки')

    return data['response']['short_url']

def count_clicks(token, url):
    params = {
        'access_token': token,
        'key': urlparse(url).path.strip('/'),
        'v': '5.199'
    }
    response = requests.get('https://api.vk.com/method/utils.getLinkStats', params=params)
    response.raise_for_status()
    data = response.json()

    if 'response' not in data:
        raise requests.exceptions.HTTPError('Ошибка при получении статистики')

    return data['response']['stats'][0]['views']

def is_shorten_link(url):
    return urlparse(url).netloc == 'vk.cc'

def main():
    url = input('Введите ссылку: ')

    try:
        if is_shorten_link(url):
            clicks = count_clicks(token, url)
            print('Количество посещений:', clicks)
        else:
            short_url = shorten_link(token, url)
            print('Короткая ссылка:', short_url)
    except requests.exceptions.HTTPError as e:
        print('Ошибка:', e)

main()
