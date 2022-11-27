#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: zhoushuke
@Email: zhoushuke@sensetime.com
@Date: 2020-04-24 16:43:37
LastEditors: zhoushuke
LastEditTime: 2021-08-19 14:35:01
FilePath: /fallen_deliver/utils/sendxmail.py
'''

import os
# urllib
import requests
from loguru import logger as LOGGER
from config import cfg as CFG
from templates import render_html
from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP
from smtplib import SMTPAuthenticationError
from smtplib import SMTPException
from socket import error


# send mail by http post
class MailService(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def send(self, dst, subject, content, title='MailFound', fmt='template'):
        url = self.base_url
        data = {
            'tos': dst,
            'subject': subject,
            'title': title,
            'format': fmt,
            'content': content
        }
        try:
            # data = urllib.parse.urlencode(data).encode('utf-8')
            # res = urllib.request.urlopen(url, data)
            res = requests.post(url=url, data=data)
        except Exception as e:
            LOGGER.error(
                'Send mail failed, exception: {}, POST url: {}, mail content: {}'
                .format(e, url, content))
            os._exit(1)
        else:
            res_content = res.json()
            if res_content and 'ok' in res_content.get('msg'):
                LOGGER.info('Send mail successfully')
            else:
                LOGGER.error('Mail response not OK, content: {}'.format(
                    str(res_content)))

    def get_info(self):
        return {"type": "MailAlerter"}


# send mail by local smtp
class EmailBySMTP(object):
    def __init__(self, **kwargs):
        self.smtp_host = CFG['emailhtml']['smtp_host']
        self.smtp_port = CFG['emailhtml']['smtp_port']
        self.username = CFG['emailhtml']['username']
        self.password = CFG['emailhtml']['password']
        self.format = CFG['emailhtml']['format']
        self.email_from = CFG['emailhtml']['from_addr']
        # email_to, email_cc need to be a list
        self.email_to = kwargs.get("sendto")
        self.email_cc = kwargs.get("cc")
        self.email_bcc = kwargs.get("bcc")

    # subject: string
    # summary_str: string
    # data: dict
    def send(self, subject, summary_str, data):
        body = render_html(summary_str=summary_str, data=data)
        if 'html' == self.format:
            email_msg = MIMEText(body, 'html', _charset='UTF-8')
        else:
            email_msg = MIMEText(body, _charset='UTF-8')
        email_msg['Subject'] = Header(subject, 'UTF-8')
        email_msg['To'] = ','.join(self.email_to)
        email_msg['From'] = self.email_from
        if self.email_cc:
            email_msg['Cc'] = ','.join(self.email_cc)
            self.email_to += self.email_cc
        if self.email_bcc:
            # email_msg['Bcc'] = ','.join(self.email_bcc)
            self.email_to += self.email_bcc
        try:
            if self.smtp_port:
                self.smtp = SMTP(self.smtp_host, self.smtp_port)
            else:
                self.smtp = SMTP(self.smtp_host)
            self.smtp.ehlo()
            if self.smtp.has_extn('STARTTLS'):
                self.smtp.starttls()
            self.smtp.login(self.username, self.password)
        except (SMTPException, error) as e:
            LOGGER.error("Error connecting to SMTP host: %s" % (e))
        except SMTPAuthenticationError as e:
            LOGGER.error("SMTP username/password rejected: %s" % (e))
        self.smtp.sendmail(self.email_from, self.email_to,
                           email_msg.as_string())
        self.smtp.quit()

    @staticmethod
    def get_info(self):
        return {"type": "MailAlerter"}
