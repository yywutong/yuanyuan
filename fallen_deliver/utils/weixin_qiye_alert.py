#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
@Author: zhoushuke
@Email: zhoushuke@sensetime.com
@Date: 2020-06-05 14:31:23
LastEditors: zhoushuke
LastEditTime: 2021-04-23 11:21:54
FilePath: /fallen_deliver/utils/weixin_qiye_alert.py
'''

import os
import json
# from MyEncoder import MyEncoder
import datetime
import requests
from loguru import logger as LOGGER
from config import cfg as CFG
from requests.exceptions import RequestException


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


class WeChatAlerter(object):
    def __init__(self, *args):
        super(WeChatAlerter, self).__init__(*args)
        self.url = CFG['wechat']['api']
        self.corp_id = CFG['wechat']['corp_id']  # 企业号id
        self.secret = CFG['wechat']['secret']  # secret
        self.agent_id = CFG['wechat']['agent_id']  # 应用id
        self.party_id = CFG['wechat']['party_id']  # 部门id
        self.user_id = CFG['wechat']['user_id']  # 用户id，多人用 | 分割，全部用 @all
        self.tag_id = CFG['wechat']['tag_id']  # 标签id
        self.access_token = ''  # 微信身份令牌
        self.expires_in = datetime.datetime.now() - datetime.timedelta(
            seconds=60)

    # def create_default_title(self, matches):
    #     subject = 'ElastAlert: %s' % (self.rule['name'])
    #     return subject

    def alert(self, body):
        if not self.party_id and not self.user_id and not self.tag_id:
            LOGGER.warn("All touser & toparty & totag invalid")
        # http://qydev.weixin.qq.com/wiki/index.php?title=AccessToken
        self.get_token()
        self.senddata(body)
        # LOGGER.info("send message to %s" % (self.corp_id))

    def get_token(self):

        # 获取token是有次数限制, 正常够用, 2000/day
        if self.expires_in >= datetime.datetime.now() and self.access_token:
            return self.access_token

        # 构建获取token的url
        get_token_url = self.url + '/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (
            self.corp_id, self.secret)

        try:
            response = requests.get(get_token_url)
            response.raise_for_status()
        except RequestException as e:
            LOGGER.error("get access_token failed , stacktrace:%s" % e)
            os._exit(1)

        token_json = response.json()

        if 'access_token' not in token_json:
            LOGGER.error("get access_token failed , , the response is :%s" %
                         response.text())
            os._exit(1)

        # 获取access_token和expires_in
        self.access_token = token_json['access_token']
        self.expires_in = datetime.datetime.now() + datetime.timedelta(
            seconds=token_json['expires_in'])

        return self.access_token

    def senddata(self, content):

        # http://qydev.weixin.qq.com/wiki/index.php?title=%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F
        # 微信企业号有字符长度限制（2048），超长自动截断

        # 参考 http://blog.csdn.net/handsomekang/article/details/9397025
        # len utf8 3字节，gbk2 字节，ascii 1字节
        if len(content) > 2048:
            content = content[:2045] + "..."

        # 微信发送消息文档
        # http://qydev.weixin.qq.com/wiki/index.php?title=%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F
        send_url = self.url + '/cgi-bin/message/send?access_token=%s' % (
            self.access_token)

        headers = {'content-type': 'application/json'}

        # 最新微信企业号调整校验规则，tagid必须是string类型，如果是数字类型会报错，故而使用str()函数进行转换
        payload = {
            "touser": self.user_id and str(self.user_id) or '',  # 用户账户，建议使用tag
            "toparty": self.party_id and str(self.party_id)
            or '',  # 部门id，建议使用tag
            "totag": self.tag_id and str(self.tag_id) or
            '',  # tag可以很灵活的控制发送群体细粒度。比较理想的推送应该是，在heartbeat或者其他elastic工具自定义字段，添加标签id。这边根据自定义的标签id，进行推送
            'msgtype': "text",
            "agentid": self.agent_id,
            "text": {
                "content":
                content.encode('UTF-8').decode("latin1")  # 避免中文字符发送失败
            },
            "safe": "0"
        }

        # set https proxy, if it was provided
        # 如果需要设置代理，可修改此参数并传入requests
        # proxies = {'https': self.pagerduty_proxy} if self.pagerduty_proxy else None
        try:
            # response = requests.post(send_url, data=json.dumps(payload, ensure_ascii=False), headers=headers)
            response = requests.post(send_url,
                                     data=json.dumps(payload,
                                                     cls=MyEncoder,
                                                     indent=4,
                                                     ensure_ascii=False),
                                     headers=headers)
            response.raise_for_status()
        except RequestException as e:
            LOGGER.error("send message has error: %s" % e)

        LOGGER.info("send [wechat] response: %s" % response.text)

    def get_info(self):
        return {'type': 'WeChatAlerter'}
