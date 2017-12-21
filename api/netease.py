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


modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = b'0CoJUm6Qyw8W8jud'
pubKey = '010001'

def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    # aes加密需要byte类型。
    # 因为调用两次，下面还要进行补充位数。
    # 直接用try与if差不多。
    try:
        text = text.decode()
    except:
        pass
    text = text + pad * chr(pad)
    try:
        text = text.encode()
    except:
        pass
    encryptor = AES.new(secKey, 2, bytes('0102030405060708', 'utf-8'))
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext

def createSecretKey(size):
    # 2中 os.urandom返回是个字符串。3中变成bytes。
    # 不过加密的目的是需要一个字符串。
    # 因为密钥之后会被加密到rsa中一起发送出去。
    # 所以即使是个固定的密钥也是可以的。
    return bytes(''.join(random.sample('1234567890qwertyuipasdfghjklzxcvbnm', 16)), 'utf-8')

def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    # 3中将字符串转成hex的函数变成了binascii.hexlify, 2中可以直接 str.encode('hex')
    rs = int(binascii.hexlify(text), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)

def encrypted_request(text):
    # 这边是加密过程。
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    # 在那个js中也可以找到。
    # params加密后是个byte，解下码。
    data = {
        'params': encText.decode(),
        'encSecKey': encSecKey
    }
    return data 

# 不应该在这定义。
# 暂且放在这。
@contextmanager
def ignored(*exception):
    """
    使用上下文管理的方式忽略错误。
    with ignored(OSError):
        print(1)
        raise(OSError)
    print(2)
    """
    if exception:
        try:
            yield
        except exception:
            logger.error("error has ignored.", exc_info=True)
    else:
        try:
            yield 
        except:
            logger.error("error has ignored.", exc_info=True)

def requestsExceptionFilter(func):
    """
    若某一函数出错(一般是网络请求), 会再次进行2次重新请求，否则会传回False
    @requestsExceptionFilter
    def test():
        requests.get('http://www.thereAreNothing.com')
    
    test()
    ---
    False
    """
    def _filter(*args, **kwargs):
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except:
                logger.error("retry function {0} args {1}, kwargs {2} times:{3}".format(func, args, kwargs, i))
                continue
        else:
            logger.error("function {0} is wrong. args {1}, kwargs {2}".format(func, args, kwargs))
            return False
    
    return _filter


class HttpRequest(object):
    # 使用keep-alive，
    # keep-alive保持持久连接，没有必要开启很多个TCP链接，浪费资源。
    # 使用会话(session)来保持持久连接。
    # sessions = requests.session()
    # cookies也可以方便管理。 
    # TCP重传需要3秒。
    default_timeout = 3.05
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'music.163.com',
        'Referer': 'http://music.163.com/',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    }

    #  headers = {
    #     'Accept': 'lication/xml;q=0.9,*/*;q=0.8'
    #     'Accept-Encoding': 'gzip,deflate,sdch',
    #     'Accept-Language': 'zh-CN,zh;q=0.8',
    #     'Proxy-Connection': 'keep-alive',
    #     'Content-Type': 'application/x-www-form-urlencoded',
    #     'Host': 'music.163.com',
    #     'Referer': 'http://music.163.com/',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
    # }

    cookies = {}

    def __init__(self):
        self.sessions = requests.session()
        self.headers = self.headers.copy()

    @requestsExceptionFilter
    def httpRequest(self, action, method="GET", add=None, data=None, headers=None, cookies='',\
                    timeout=default_timeout, urlencode='utf-8', is_json=True):
        """
            默认以get方式请求，
            GET方式附加内容用add参数，POST方式提交内容用data参数。
            编码用urlencode参数，默认utf-8。
            默认cookies为空。
        """
        if not headers:
            headers = self.headers

        if method.upper() == 'GET':
            if add:
                html = self.sessions.get(action, params=add, headers=headers, cookies=cookies, timeout=timeout)
            else:
                html = self.sessions.get(action, headers=headers, cookies=cookies, timeout=timeout)
            html.encoding = urlencode

        elif method.upper() == 'POST':
            if data:
                html = self.sessions.post(action, data=data, headers=headers, cookies=cookies, timeout=timeout)
            else:
                html = self.sessions.post(action, headers=headers, cookies=cookies, timeout=timeout)
            html.encoding = urlencode

        return html

    def __del__(self):
        # 关闭请求。
        with ignored():
            self.sessions.close()

logger = logging.getLogger(__name__)
class NeteaseApi(HttpRequest):

    cookies = {
            'appver': '2.1.2.184499',
            'os': 'pc',
            'channel': 'netease',
        }
    
    default_timeout = 10

    def __init__(self):
        super(NeteaseApi, self).__init__()
        self.headers['Host'] = 'music.163.com'
        self.headers['Referer'] = 'http://music.163.com'
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.vertifyHeaders = self.headers.copy()
        self.vertifyHeaders['Host'] = 'ac.dun.163yun.com'
        self.vertifyHeaders['Accept'] = 'image/png,image/*;q=0.8,*/*;q=0.5'
        self.vertifyHeaders['Content-Type'] = ''

        self.urlEamilHeaders = self.headers.copy()
        self.urlEamilHeaders['Referer'] = ''
        self.urlEamilHeaders['Origin'] = 'orpheus://orpheus' 

    def httpRequest(self, *args, **kwargs):
        data = kwargs.get('data')
        if data:
            kwargs['data'] = encrypted_request(data)
        logger.info("进行网易云Url请求, args: {0}, kwargs: {1}".format(args, kwargs))
        html = super(NeteaseApi, self).httpRequest(*args, **kwargs)
        with ignored():
            return json.loads(html.text)
        
        logger.info("url: {0} 请求失败. Header: {1}".format(args[0], kwargs.get('headers')))
        return False


    def lyric(self, id_music):
        """
        通过网友渠道获取lyric
        可以直接拿
        """
        url_lrc = 'http://music.163.com/api/song/lyric?os=osx&id={0}&lv=-1&kv=-1&tv=-1'.format(id_music)
        requests_lrc = requests.get(url_lrc)
        json_lrc = json.loads(requests_lrc.text)
        return(json_lrc['lrc']['lyric'])

    def url_music(self, id_music:list):
        """
        2017/7/14更新。
        返回歌曲的URL。
        """
        data = {'csrf_token': '', 'ids': id_music, 'br': 999000}
        url = "http://music.163.com/weapi/song/enhance/player/url"
        html = self.httpRequest(url, method='POST', data=data)
        with ignored():
            return html['data']
        logger.info('歌曲请求失败: ids {0}'.format(id_music)) 
        return False

    def get_playlist(self):
        url = 'http://music.163.com/discover/toplist'
        r = requests(url, headers = headers)
        lists = BeautifulSoup(r.text, "lxml").find("ul", class_ = f-hide).find_All("li")
        return lists

if __name__ == '__main__':
    api = NeteaseApi()
    # print(api.lyric(68350))
    # print(api.url_music([68350]))
    print(api.get_playlist())
