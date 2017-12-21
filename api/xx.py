import os
import sys

import urllib
import urllib.parse

import requests

import base64
import bs4
from bs4 import BeautifulSoup

import hashlib
import binascii
import random
import re
import logging
from contextlib import contextmanager

import json
import lxml
import html5lib 

try:
    from Cryptodome.Cipher import AES
except:
    from Crypto.Cipher import AES


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'music.163.com',
    'Referer': 'http://music.163.com/',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}


url = 'http://music.163.com/artist?id=9621'
r = requests.get(url, headers = headers).text
lists = BeautifulSoup(r, "lxml").find("ul", {"class", "f-hide"}).find_all("li")
for x in lists:
    tag = x.a
    str_n = str(tag)
    str_n = re.sub("\D", "", str_n)
    str_n = str_n + ": " + x.text
    print(str_n)


