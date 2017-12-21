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

class myApi(object):

    def __init__(self):
        pass

    def get_songnames_songids_by_artistid(self, id_artist):
        """
        API更新：2017-12-20 by Didiwei
        输入： 歌手的ID
        返回： Dict { 'NumX'：{ 歌曲ID, 歌曲名} }
        """
        url = 'http://music.163.com/artist?id={0}'.format(id_artist)
        r = requests.get(url, headers = headers).text
        list_songs = BeautifulSoup(r, "lxml").find("ul", {"class", "f-hide"}).find_all("li")
        dict_songs = {}
        i = 0
        for x in list_songs:
            key = "Num{0}".format(i)
            i = i + 1
            song_name = x.text
            str_tag = str(x.a)
            song_id = re.sub("\D", "", str_tag)
            songs = {}
            songs["id"] = song_id
            songs["name"] = song_name
            dict_songs[key] = songs
        return dict_songs

    def lyric(self, id_music):
        """
        通过网友渠道获取lyric
        可以直接拿
        """
        url_lrc = 'http://music.163.com/api/song/lyric?os=osx&id={0}&lv=-1&kv=-1&tv=-1'.format(id_music)
        requests_lrc = requests.get(url_lrc)
        json_lrc = json.loads(requests_lrc.text)
        return(json_lrc['lrc']['lyric'])


if __name__ == '__main__':
    api = myApi()
    x = api.get_songnames_songids_by_artistid(9621)
    for i in range(0,49):
        print(x['Num{0}'.format(i)]['name'])
    # print(x['0']['name'])

    
