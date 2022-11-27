#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2021-06-01 11:56:35
LastEditors: zhoushuke
LastEditTime: 2021-08-19 17:39:54
FilePath: /fallen_deliver/utils/standard_ops.py
'''

import os
import random
import time

from config import cfg as CFG
from utils.func_ops import (parse_from_formdata, remove_repeat_str, send_alert,
                            subprocess_exec_cmd)
from utils.git_ops import GitRepository, git_expection


# no use
class Standard_Ops(object):
    def __init__(self, args):
        self.subject = "[Fallen] 标准化OP操作失败"
        self.summary = "Fallen Alert"
        self.repo_name = CFG["standartop"]["repo_name"]
        self.repo = self.pull_repo()
        self.apps_info(args)

    def _send_alert(self, **kwargs):
        kwargs["工单标题"] = self.title
        kwargs["工单ID"] = self.woid
        event = {
            "ifsendalert": True,
            "alerter": "mail",
            "subject": self.subject,
            "summary": self.summary,
            "content": kwargs,
            "sendto": self.sendto
        }
        send_alert(event)

    def apps_info(self, args):
        apps_info = parse_from_formdata(args)
        self.apps = apps_info.get("apps")
        # apps like: [{"name": "模型训练", "version": "03.00.01"}, {"name": "tokestrel", "version": "02.00.00"}, ...]
        self.woid = apps_info.get("woid")
        self.title = apps_info.get("title")
        # sendto need to be a list
        self.sendto = remove_repeat_str(
            apps_info.get("order_creator_email") + "," +
            apps_info.get("other_senders_emails"))

    def get_op_id(self, name, version):
        cmd = "/usr/local/bin/sprcli list" + name + version
        rnt, out = subprocess_exec_cmd(cmd)
        return out
        # return opid

    def export_ops_push_git(self):
        for app in self.apps:
            name, version = app.get("name"), app.get("version")
            opid = self.get_op_id(name, version)
            if not opid:
                content = {"OP名称": name, "OP版本": version, "失败原因": "未找到对应的OP"}
                self._send_alert(**content)
            # export op by id
            cmd = "/usr/local/bin/op export -i " + str(opid)
            rnt, out = subprocess_exec_cmd(cmd)
        self.push_ops_to_git()

    def pull_repo(self):
        local_path = os.path.join(CFG["standartop"]["git_path_tmp"],
                                  self.repo_name)
        url = CFG["standartop"]["repo_url"]
        branch = CFG["standartop"]["repo_branch"]
        try:
            repo = GitRepository(local_path, url, branch)
            # checkout is ok ,becease current status is in a branch
            repo.change_to_branch(branch)
            repo.pull()
            return repo
        except Exception:
            git_expection(self.repo_name, "git pull异常")

    def push_ops_to_git(self):
        try:
            self.repo.config_set()
            self.repo.add_push_all("auto commit by Fallen")
            # sleep for random seconds
            time.sleep(random.randint(5, 10))
        except Exception:
            git_expection(self.repo_name, "git push异常")

    def __call__(self):
        self.export_ops_push_git
