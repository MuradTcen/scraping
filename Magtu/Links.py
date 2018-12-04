# -*- coding: utf-8 -*-


class Links:

    def __init__(self):
        self.base = 'http://newlms.magtu.ru/'
        self.urls = {
            'login': 'login/index.php',
            'record': 'report/record_book/',
            'group': 'report/magtu_group_for_student/',
            'debt': 'report/magtu_debtor_for_student/',
            'personal': 'my/'
        }
        self.aggregate_full_links()

    def aggregate_full_links(self):
        for key, value in self.urls.items():
            self.urls[key] = self.base + value
