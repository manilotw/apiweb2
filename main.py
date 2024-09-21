import requests
from urllib.parse import urlparse
from environs import Env


def shorten_link(token,
                  url):
    params = {
        'access_token': token,
        'url': url,
        'v': '5.199'
    }
    response = requests.get('https://api.vk.com/method/utils.getShortLink', params=params)
    response.raise_for_status()
    json_data = response.json()

    if 'response' not in json_data:
        raise requests.exceptions.HTTPError('Ошибка при сокращении ссылки')

    return json_data['response']['short_url']


def count_clicks(token,
                  url):
    params = {
        'access_token': token,
        'key': urlparse(url).path.strip('/'),
        'v': '5.199'
    }
    response = requests.get('https://api.vk.com/method/utils.getLinkStats', params=params)
    response.raise_for_status()
    json_data = response.json()

    if 'response' not in json_data:
        raise requests.exceptions.HTTPError('Ошибка при получении статистики')

    return json_data['response']['stats'][0]['views']


def is_shorten_link(url):
    return urlparse(url).netloc == 'vk.cc'


def main():
    env = Env()
    env.read_env()

    vk_token = env.str('VK_TOKEN')
    url = input('Введите ссылку: ')

    try:
        if is_shorten_link(url):
            clicks = count_clicks(vk_token,
                                   url)
            print('Количество посещений:', clicks)
        else:
            short_url = shorten_link(vk_token,
                                      url)
            print('Короткая ссылка:', short_url)
    except requests.exceptions.HTTPError as e:
        print('Ошибка:', e)


if __name__ == "__main__":
    main()
