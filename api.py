import requests
from requests import Session
from loguru import logger
from config import *

log = logger.bind(user="m站新站辅助工具")
s: Session = requests.Session()


def logapi(url, text):
    if 输出api返回信息:
        log.info(f"url:{url}\n返回信息:{text}")


def Server酱推送(msg):
    url = f"https://sctapi.ftqq.com/{Server酱_key}.send"
    data = {"title": f"【m站新站辅助工具】", "desp": msg}
    r = s.post(url, data=data)
    logapi(url, r.json())


def pushplus推送(msg):
    url = "http://www.pushplus.plus/send"
    data = {"token": pushplus_key, "title": f"【m站辅助工具】", "content": msg}
    r = s.post(url, data=data)
    logapi(url, r.json())


def 登录(账号, 密码):
    url = "https://api.mfuns.net/v1/auth/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2007J17C Build/RKQ1.200826.002)"
    }
    data = {
        "account": 账号,
        "password": 密码
    }

    r = s.post(url, headers=headers, data=data)
    logapi(url,r.json())
    access_token = r.json()['data']['access_token']
    return access_token


def 获取用户信息():
    url = "https://api.mfuns.net/v1/user/info"
    r = s.get(url).json()
    logapi(url, r)
    return r


def 获取等级(等级):
    url = 'https://api.mfuns.net/v1/user/badge_all'
    r = s.get(url).json()['data']['badges']
    logapi(url, r)
    for q in r:
        if q['id'] == 等级:
            return q['name']
    return ''


def 签到():
    url = "https://api.mfuns.net/v1/sign/sign"
    r = s.get(url)
    logapi(url, r)
    return r.json()
