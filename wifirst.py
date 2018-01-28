import cookielib
import urllib
import urllib2

import lxml.html


class Wifirst:
    def __init__(self, login, password):
        USER_AGENT = 'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
        self.TOKEN_URL = 'https://selfcare.wifirst.net/sessions/new'
        self.SESSION_URL = 'https://selfcare.wifirst.net/sessions'
        self.LOGIN_URL = 'https://connect.wifirst.net/?perform=true'
        self.REQUEST_URL = 'https://wireless.wifirst.net:8090/goform/HtmlLoginRequest'
        self.SUCCESS_URL = 'https://apps.wifirst.net/?redirected=true'
        self.ERROR_URL = 'https://connect.wifirst.net/login_error'

        self.TOKEN_XPATH = '//input[@name=\'authenticity_token\']/@value'
        self.USERNAME_XPATH = '//input[@name=\'username\']/@value'
        self.PASSWORD_XPATH = '//input[@name=\'password\']/@value'

        self.login = login
        self.password = password

        self.cookies = cookielib.CookieJar()

        self.crawler = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        self.crawler.addheaders = [('User-Agent', USER_AGENT)]

    def reconnect(self):
        token = self.fetch_token()
        return self.authenticate(self.login, self.password, token)

    def fetch_token(self):
        response = self.crawler.open(self.TOKEN_URL)
        tree = lxml.html.parse(response)
        token = tree.xpath(self.TOKEN_XPATH)[0]
        return token

    def authenticate(self, login, password, token):
        self.crawler.open(self.SESSION_URL, urllib.urlencode({
            'login': login,
            'password': password,
            'authenticity_token': token
        }))

        response = self.crawler.open(self.LOGIN_URL)
        tree = lxml.html.parse(response)
        username = tree.xpath(self.USERNAME_XPATH)[0]
        tmp_pass = tree.xpath(self.PASSWORD_XPATH)[0]

        response = self.crawler.open(self.REQUEST_URL, urllib.urlencode({
            'username': username,
            'password': tmp_pass,
            'qos_class': 0,
            'success_url': self.SUCCESS_URL,
            'error_url': self.ERROR_URL
        }))
        return response.geturl() == self.SUCCESS_URL
