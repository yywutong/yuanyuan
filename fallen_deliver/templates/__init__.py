#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
@Author: zhoushuke
@Email: zhoushuke@sensetime.com
@Date: 2020-06-03 16:22:44
LastEditors: zhoushuke
LastEditTime: 2021-04-22 15:55:17
FilePath: /fallen_deliver/templates/__init__.py
'''
import os
from jinja2 import Environment, FileSystemLoader


def render_html(summary_str, data):
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    template = env.get_template('mail.html.tpl')
    out = template.render(summary_str=summary_str, data=data)
    with open('/tmp/mail.html', 'w', encoding='utf-8') as f:
        f.write(out)
    return out
