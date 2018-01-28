# coding=utf-8
import socket
import subprocess
import urllib2
import config as config
from cesi_proxy import Cesi
from wifirst import Wifirst

fail = 0
config = config.config
cesi = Cesi(login=config["cesi"]["username"], password=config["cesi"]["password"])
wifirst = Wifirst(login=config["wifirst"]["username"], password=config["wifirst"]["password"])


def getWifiName():
    popen = subprocess.Popen(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for line in popen.stdout:
        if "Profil       " in line:
            return line.splitlines()[0].split(": ")[1][:-1]

    return False


def tryPortal():
    crawler = urllib2.build_opener()
    res = crawler.open("http://www.google.fr")
    return res.geturl() == "http://www.google.fr"


def tryPing():
    try:
        host = socket.gethostbyname("www.google.fr")
        socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


if tryPing():
    if not tryPortal():
        wifi = getWifiName()
        if wifi == "SmartCampus":
            if not wifirst.reconnect():
                fail += 1
            else:
                fail = 0
        elif wifi == "CESI_HotSpot":
            if not cesi.reconnect():
                fail += 1
            else:
                fail = 0
        print fail
