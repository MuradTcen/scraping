# -*- coding: utf-8 -*-
import requests
# from getter import getter
from Links import Links
from User import User
from bs4 import BeautifulSoup
from random import choice
from time import sleep


LOGIN = ''
PASSWORD = ''

useragents = open('useragents.txt').read().split('\n')
proxies = open('proxies.txt').read().split('\n')


class Cabinet(Links, User):

    def __init__(self, login, password):
        super().__init__()
        self.data = {
            'username': login,
            'password': password
        }
        self.user = {
            'name': '',
            'debt': []
            # 6
        }

        self.proxy = {'http': 'http://' + choice(proxies)}
        self.useragent = {'User-agent': choice(useragents)}
        # headers=self.useragent, proxies=self.proxy

    def auth(self):
        self.session = requests.Session()
        # self.session.get(self.urls['login'], headers=self.useragent, proxies=self.proxy)
        # self.session.post(self.urls['login'], data=self.data, headers=self.useragent, proxies=self.proxy)
        self.session.get(self.urls['login'])
        self.session.post(self.urls['login'], data=self.data)

    def get_info(self):
        # res = self.session.get(self.urls['personal'], headers=self.useragent, proxies=self.proxy).text
        res = self.session.get(self.urls['personal']).text
        soup = BeautifulSoup(res, 'lxml')
        self.user['name'] = soup.find('span', class_='usertext').text
        print(self.user['name'])

    def get_debt(self):
        def get_debt(debt):
            tmp = []
            for d in debt:
                # print(d)
                data = {
                    '#': d.find_all('td')[0].text,
                    'Семестр': d.find_all('td')[1].text,
                    'Дисциплина': d.find_all('td')[2].text,
                    'Вид аттестации': d.find_all('td')[3].text,
                    'Кафедра': d.find_all('td')[4].text,
                    'ФИО преподавателя': d.find_all('td')[5].text
                }
                tmp.append(data)
            return tmp

        res = self.session.get(self.urls['debt']).text
        soup = BeautifulSoup(res, 'lxml')
        debt = soup.find('div', id='page').find_all('div', class_='container-fluid')[1]. \
            find('div').find('section').find_all('tr')
        del(debt[0])
        self.user['debt'] = get_debt(debt)

    def print_debt(self):
        for d in self.user['debt']:
            print(d['Семестр'], d['Дисциплина'], d['Вид аттестации'])
        print(len(self.user['debt']))


def main():
    my_cab = Cabinet(LOGIN, PASSWORD)
    my_cab.auth()
    my_cab.get_info()
    my_cab.get_debt()
    my_cab.print_debt()
if __name__ == '__main__':
    main()
