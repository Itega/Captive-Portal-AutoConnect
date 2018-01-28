# coding: utf-8
try:
    from httplib import HTTPSConnection
    from urllib import urlencode
except ImportError:
    from http.client import HTTPSConnection
    from urllib.parse import urlencode

import ssl


class Cesi:
    def __init__(self, login, password):
        self.username = login
        self.password = password
        self.gateway = "wifi.viacesi.fr:1003"

    def reconnect(self):
        r = HTTPSConnection('google.fr', context=ssl._create_unverified_context())
        r.request('GET', '/')
        try:
            resp = r.getresponse()
        except Exception as e:
            print e.message
        magic = resp.getheader('location').split('?')[-1]
        page = "/%s" % resp.getheader('location').split('/')[-1]

        r = HTTPSConnection(self.gateway, context=ssl._create_unverified_context())
        try:
            print r.request('GET', page)

            r.getresponse()
        except Exception as e:
            print e.message
        req = urlencode({'magic': magic, 'answer': '1', '4Tredir': 'https://google.fr/'})
        r.request('POST', page, req)
        try:
            r.getresponse()
        except Exception as e:
            print e

        req = urlencode(
            {'magic': magic, 'username': self.username, 'password': self.password, '4Tredir': 'https://google.fr/'})
        r.request('POST', page, req)
        try:
            r.getresponse()
        except Exception as e:
            print e

