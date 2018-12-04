# -*- coding: utf-8 -*-
import requests
from random import choice
from time import sleep
from bs4 import BeautifulSoup
from random import uniform
import os
import json

useragents = open('useragents.txt').read().split('\n')
proxies = open('proxies.txt').read().split('\n')


def get_html(url, useragent=None, proxy=None):
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text


def get_ip(html):
    print('New proxy & User-Agent:')
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('span', class_='ip').text.strip()
    ua = soup.find('span', class_='ip').find_next_sibling('span').text.strip()
    print(ip)
    print(ua)
    print('------')

def getting_w_proxy_and_sleep(url):
    a = uniform(3, 6)
    print(a)
    sleep(a)

    proxy = {'http': 'http://' + choice(proxies)}
    useragent = {'User-agent': choice(useragents)}
    try:
        html = get_html(url, useragent, proxy)
    except:
        print('err')
    print(html)
    return html


def write_txt(lyric, filename):
    with open(filename, 'w') as f:
        f.write(lyric)


def write_list(lst, filename):
    with open(filename, 'w') as f:
        json.dump(lst, f, indent=2, ensure_ascii=False)


def main():
    # url = 'http://sitespy.ru/my-ip'
    url = 'https://www.azlyrics.com/'
    names = []
    id_song = 0
    for part in abc:
        try:
            print(url + part + '.html')
            lst_bands = get_list_bands(getting_w_proxy_and_sleep(url + part + '.html'))
            for band in lst_bands:
                list_songs = get_list_songs(
                    getting_w_proxy_and_sleep(url + band['href']))
                band_name = band['href'].split('/')[-1].split('.')[0]
                names.append(band_name)
                if not os.path.exists(band_name):
                    os.mkdir(band_name)
                os.chdir(band_name)
                for song in list_songs:
                    url_lyric = url + song['href'].split('..')[1]
                    print(url_lyric)
                    lyric = get_lyric(getting_w_proxy_and_sleep(url_lyric))
                    id_song += 1
                    print(os.getcwd())
                    write_txt(lyric, str(id_song))
                    # print(song['href'].split('.')[-2])
                os.chdir('..')
        except:
            continue
    write_list(names, 'categories')


if __name__ == '__main__':
    main()
