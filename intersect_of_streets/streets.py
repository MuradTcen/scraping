#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
from bs4 import BeautifulSoup
import json
# import csv
# from datetime import datetime
# from time import sleep

# http://mapdata.ru/sankt-peterburg/ulicy/
# http://mapdata.ru/chelyabinskaya-oblast/magnitogorsk/ulicy/


def write_json(data, filename='streets.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('ul', class_='pagination').find_all('a')[-1].text
    return int(pages)


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    streets = soup.find_all('div', class_='content-item')
    streets_lst = []
    for street in streets:
        name = street.find('a').text
        streets_lst.append(name)
        # print(name)
    return streets_lst


def get_list_streets(html_city):
    html = get_html(html_city)
    page_part = 'stranica-'
    count_pages = get_total_pages(html)
    # print(get_page_data(get_html(test)))
    list_of_streets = []
    for i in range(1, count_pages + 1):
        # print(url_magn + page_part + str(i))
        url = html_city + page_part + str(i)
        list_of_streets.extend(get_page_data(get_html(url)))
    print(len(list_of_streets))
    return list_of_streets


def main():
    url = 'http://mapdata.ru/'
    url_magn = url + 'chelyabinskaya-oblast/magnitogorsk/ulicy/'
    url_spb = url + 'sankt-peterburg/ulicy/'
    # magn_list = get_list_streets(url_magn)
    # spb_list = get_list_streets(url_spb)
    # write_json(magn_list, 'magn.json')
    # write_json(spb_list, 'spb.json')
    magn_file = open('magn.json', 'r')
    magn_list = json.loads(magn_file.read())
    magn_file.close()
    spb_file = open('spb.json', 'r')
    spb_list = json.loads(spb_file.read())
    spb_file.close()
    # spb_list = json.loads((open('spb.json', 'r')).read())
    # print(magn_list)
    # print(spb_list)
    result = []
    for i in magn_list:
        if i in spb_list:
            result.append(i)
    print(len(result))
    write_json(result, 'intersect.json')


if __name__ == '__main__':
    main()
