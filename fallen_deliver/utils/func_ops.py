#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
@Author: zhoushuke
@Email: zhoushuke@sensetime.com
@Date: 2020-04-25 16:06:16
LastEditors: zhoushuke
LastEditTime: 2022-04-11 15:47:54
FilePath: /fallen_deliver/utils/func_ops.py
'''
import os
import re
import time
import json
import random
import hashlib
import hmac
import pymysql
import base64
import requests
import subprocess
import platform
import wechat_work_webhook
from pathlib import Path
from config import cfg as CFG
from loguru import logger as LOGGER
from functools import wraps
from utils.sendxmail import MailService, EmailBySMTP
from utils.weixin_qiye_alert import WeChatAlerter
from utils.dingtalk_alert import DingtalkChatbot
from utils.sqlalchemy_db import get_iphone_role_by_email, get_oncall_info_by_role
from yaml import load, dump

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def change_main_yaml_version(path, app, version):
    with open(path, "r") as fh:
        pws = fh.read()
        pws_dict = load(pws, Loader=Loader)
        pws_dict["registry_image"] = app
        pws_dict["registry_tag"] = version
    with open(path, "w") as f:
        dump(pws_dict, f, default_flow_style=False, sort_keys=False)


def change_values_yaml_version(path, app, version):
    with open(path, "r") as fh:
        pws = fh.read()
        pws_dict = load(pws, Loader=Loader)
        pws_dict[app]["tag"] = version
    with open(path, "w") as f:
        dump(pws_dict, f, default_flow_style=False, sort_keys=False)


def run_time(exclude_time=0):
    """
    @exclude_time: should exclude time, like function sleep in func
    @return: the return run-time of the called function
    """
    def deco(f):
        @wraps(f)
        def new_func(*args, **kwargs):
            # Start the clock.
            start = time.time()
            # Execute the function and record the results.
            function_result = f(*args, **kwargs)
            # Calculate the elapsed time and add it to the function
            spend = time.time() - start - exclude_time
            # in case spend < 0
            new_func.elapsed = spend if spend > 0 else 0
            # logger run time
            LOGGER.info("runtime: {}".format(round(new_func.elapsed, 1)))
            # Returned the function with the added elapsed attribute
            return function_result

        return new_func

    return deco


def inject_into(event, something):
    # inject something into main content if need
    # something struct
    #   key||value
    # return string.
    content = CFG["mail"]["recordsplit"].join([event, something])
    return content


def send_alert_post(event):
    """
    tos=zhoushuke@sensetime.com,xxx@sensetime.com
    subject=Hello
    content=event_time||2020-04-19-10:00:01^^host_ip||127.0.0.1^^process_name||kestrel^^process_pid||2000
    format=template
    """
    LOGGER.error("EVENT HAPPEND: {}".format(event))
    subject = event.get("subject")
    content = event.get("content")
    # if need adding something
    # inject_into(content, "inject||something")
    title = event.get("title", CFG["mail"]["title"])
    fmt = event.get("format", CFG["mail"]["format"])
    if event.get("ifsendalert") and CFG["uniall"]["global_alert"]:
        m = MailService(CFG["mail"]["api"])
        m.send(CFG["mail"]["tos_private"], subject, content, title, fmt)
    else:
        LOGGER.error("get alert but send flag not open")


def send_alert_mail(event):
    LOGGER.error("alert [mail]: {}".format(event))
    subject = event.get("subject")
    summary = event.get("summary", "")
    content = event.get("content")
    sendto = event.get("sendto")
    cc = event.get("cc")
    # suit for wechat webhook
    if "@all" in sendto:
        sendto.remove("@all")
    m = EmailBySMTP(**{"sendto": sendto, "cc": cc})
    m.send(subject, summary, content)


def send_alert_wechat(event):
    LOGGER.error("alert [wechat]: {}".format(event))
    summary = event.get("summary") + "\n"
    # dict need transfor string
    content = ""
    for k, v in event.get("content").items():
        content += str(k) + ": " + str(v) + "\n"
    body = summary + content
    w = WeChatAlerter()
    w.alert(body)


def get_oncall_info(role):
    x = get_oncall_info_by_role(role)
    return {"phone": x[0][1], "email": x[0][2], "role": x[0][3]}


def transfer_from_emails_to_mobiles(s):
    if not isinstance(s, list):
        return []
    ss = []
    for email in s:
        res = get_iphone_role_by_email(email)
        if not res:
            # if not found phone, then send msg to op-oncall
            op_oncall_phone = get_oncall_info("op-oncall").get("phone")
            wechat = wechat_work_webhook.connect(CFG["wchook"]["webhook"])
            wechat.text(
                ("[Fallen] 查询失败\n根据{}查询对应手机号失败,请完善Fallen平台设置".format(email),
                 op_oncall_phone))
            ss.append(op_oncall_phone)
        else:
            ss.extend(res[0][1].split(
                ",")) if email in CFG["wchook"]["extend_role"] else ss.append(
                    res[0][1])
    return list(set(ss))


def transfer_dict_to_wchook_format(event={}):
    subject = event.get("subject")
    # id, title in content
    content = event.get("content")
    woid = content.get("工单ID") if content.get(
        "工单ID") else CFG["fallen"]["missing"]
    title = content.get("工单标题") if content.get(
        "工单标题") else CFG["fallen"]["missing"]
    content.pop("工单ID", None)
    content.pop("工单标题", None)
    s = subject + "\n工单ID: {}\n".format(woid) + "工单标题: {}".format(title)
    for k, v in content.items():
        s = s + "\n{}: {}".format(k, v)
    return s


def send_alert_webhook_wechat(event):
    LOGGER.error("alert [wchook]: {}".format(event))
    wechat = wechat_work_webhook.connect(CFG["wchook"]["webhook"])
    content = transfer_dict_to_wchook_format(event)
    sendto, cc = event.get("sendto"), event.get("cc")
    if "@all" in sendto:
        wechat.text(content, mentioned_mobile_list=["@all"])
    else:
        # attention: list.extend return None
        if cc:
            sendto.extend(cc)
        wechat.text(
            content,
            mentioned_mobile_list=transfer_from_emails_to_mobiles(sendto))


def send_alert_dingtalk(event):
    LOGGER.error("alert [dingtalk]: {}".format(event))
    summary = event.get("summary") + "\n"
    # dict need transfor string
    content = ""
    for k, v in event.get("content").items():
        content += str(k) + ": " + str(v) + "\n"
    body = summary + content
    w = DingtalkChatbot()
    w.send_text(msg=body, is_at_all=False)


# event is dict
def send_alert(event):
    LOGGER.error(event)
    if CFG["uniall"]["global_alert"] and event.get("ifsendalert"):
        for sender in event.get("alerter"):
            if "wchook" == sender and CFG["uniall"]["wchook"]:
                send_alert_webhook_wechat(event)
            elif "mail" == sender and CFG["uniall"]["mail"]:
                send_alert_mail(event)
            elif "wechat" == sender and CFG["uniall"]["wechat"]:
                send_alert_wechat(event)
            elif "dingtalk" == sender and CFG["uniall"]["dingtalk"]:
                send_alert_dingtalk(event)
            else:
                LOGGER.error("Unsupport alert type or send not open")
    else:
        LOGGER.info("Get alert but global_alert or ifsendalert flag not open")


def random_choice(n, s):
    ruuid = ""
    for i in range(n):
        ruuid += random.choice(s)
    return ruuid


def random_int(m, n):
    random.seed()
    return random.randint(m, n)


def get_repo_name_from_repo_url(s):
    return re.findall(r"https://.+/(.*)\.git",
                      s)[0] if ".git" in s else re.findall(
                          r"https://.+/(.*)", s)[0]


def find_context_in_file_by_re(pth, rgx):
    if not os.path.exists(pth):
        return False
    regex = re.compile(rgx)
    if [1 for line in open(pth, "r") if re.findall(regex, line)]:
        return True
    else:
        return False


def replace_string_under_dir(p, src_str, dst_str):
    if not os.path.exists(p):
        return
    # if macOS
    if "Darwin" == platform.system():
        cmd = "find {} -type f -exec sed -i \"\" 's/{}/{}/g".format(
            p, src_str, dst_str) + "' {} +"
    else:
        cmd = "find {} -type f -exec sed -i 's/{}/{}/g".format(
            p, src_str, dst_str) + "' {} +"
    subprocess.Popen(cmd, shell=True)


def create_sha256_signature(message, key):
    message = message.encode()
    key = key.encode()
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def readlines_from_file(filepath, mode="r"):
    with open(filepath, mode) as f:
        contents = f.read()
        return contents


def download_file_to_local(url):
    local_filename = url.split("/")[-1].split("?", 1)[0]
    r = requests.get(url.replace("'", ""), stream=True, timeout=30)
    with open(local_filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    # return local_filename


def check_md5sum(filename, md5sum):
    return True if md5sum == hashlib.md5(open(
        filename, "rb").read()).hexdigest() else False


def save_content_info_file(filepath, content, mode="w"):
    with open(filepath, mode) as f:
        f.write(content)


def delfile(filepath, filetype):
    _files = [
        _file for _file in os.listdir(filepath) if _file.endswith(filetype)
    ]
    for _file in _files:
        os.remove(_file)


def files_not_endwith(filetype=""):
    return lambda d, files: [
        f for f in files
        if (Path(d) / Path(f)).is_file() and not f.endswith(filetype)
    ]


def files_endwith(filetype=""):
    return lambda d, files: [
        f for f in files
        if (Path(d) / Path(f)).is_file() and f.endswith(filetype)
    ]


def get_ts_from_now(s=300):
    # now timestamp
    now_time = int(time.time())
    s_time = now_time - int(s)
    # from now
    return (s_time, now_time)


def convert_time_to_seconds(t="24h"):
    tt = t.upper()
    if "H" in tt:
        s = int(''.join(filter(str.isdigit, tt))) * 60 * 60
    elif "M" in tt:
        s = int(''.join(filter(str.isdigit, tt))) * 60
    else:
        LOGGER.error("Time Format Invalid")
        os._exit(1)
    return s


def imgBase64(img_path):
    with open(img_path, "rb") as f:
        base64_str = base64.b64encode(f.read())
    return str(base64_str, encoding="utf-8")


'''
@description: 
@name: get_apps_from_subform
@param {*} apps
@param {*} cluster: a list like ["test", "3s"]
@param {object} kwargs, if joined, then join cluster and apps, if not, get pure app
@return {*} a list like [{"name": "xxx", "version": ""}, {...}]
@author: zhoushuke
'''


def get_apps_from_subform(apps, cluster, **kwargs):
    joins = []
    for app in apps:
        name = app.get(CFG["fallen"]["deploy_app_id"]).strip() if app.get(
            CFG.get("fallen").get("deploy_app_id"), None) else app.get(
                CFG["fallen"]["select_deploy_app_id"]).strip()
        version = app.get(CFG["fallen"]["deploy_release_version_id"]).strip()
        if kwargs.get("joined"):
            for c in cluster:
                joins.append({"name": name + "-" + c, "version": version})
        else:
            joins.append({"name": name, "version": version})
    if len(joins) != len(set([d["name"] for d in joins])):
        LOGGER.warning("子表单中发现相同的应用")
    return joins

    # # check if have same app version, [remove to PreCheck]
    # if len(joins) != len(set([d["name"] for d in joins])):
    #     event = {
    #         "ifsendalert": True,
    #         "alerter": "mail",
    #         "subject": "[Fallen] 操作失败",
    #         "summary": "Fallen Alert",
    #         "content": {
    #             "工单标题": kwargs.get("title"),
    #             "失败原因": "子表单中发现相同的应用,请正确填写"
    #         },
    #         "sendto": kwargs.get("sendto")
    #     }
    #     send_alert(event)
    # else:
    #     return joins


def transfer_wotyep_to_int(i):
    switcher = {"提测单": 1, "修复单": 2, "变更单": 3, "同步单": 4}
    return switcher.get(i, "Invalid type")
    # 提测单 -> 1
    # 修复单 -> 2
    # 变更单 -> 3
    # 同步单 -> 4


# arg_dict is a string
# include: title, deploy env, dev's email
'''
@description:
@name: parse_from_formdata
@param {*} arg_dict: string
@param {*} join_flag: join cluster and app with '-'
@return {*} all needed information about workorder
@author: zhoushuke
'''


def parse_from_formdata(arg_dict, join_flag=True):
    arg = json.loads(arg_dict)
    apps_info, kw = {}, {}
    form_data = arg.get(CFG["fallen"]["form_data_id"])[0]
    # deploy_clusters is list
    deploy_clusters = form_data.get(CFG["fallen"]["deploy_cluster_id"])
    wotype = form_data.get(CFG["fallen"]["wotype_id"])
    title = arg.get(CFG["fallen"]["title_id"])
    woid = arg.get(CFG["fallen"]["wo_id"])
    # get creator, leader email from form_data by workorder id
    cl = get_fallen_creator_and_leader_by_workorderID(woid)
    apps_info["order_creator_email"] = form_data.get(
        CFG["fallen"]["order_create_email_id"],
        cl.get("creator_email")).strip()
    apps_info["creator_leader_email"] = cl.get("leader_email")
    apps_info["other_senders_emails"] = form_data.get(
        CFG["fallen"]["other_senders_emails_id"], "")
    kw["sendto"] = remove_repeat_str(apps_info.get("order_creator_email"))
    kw["title"] = title
    kw["woid"] = woid
    kw["joined"] = join_flag
    apps = parse_from_sub_formdata(
        form_data.get(CFG["fallen"]["subform_version_info_id"]),
        deploy_clusters, **kw)

    apps_info["clusters"] = deploy_clusters
    apps_info["apps"] = apps
    apps_info["woid"] = woid
    apps_info["title"] = title
    apps_info["wotype"] = transfer_wotyep_to_int(wotype)
    return apps_info


# get argocd app info, apps is a list
# frontend may be empty, no force
def parse_from_sub_formdata(subform, clusters, **kwargs):
    if not subform or not isinstance(subform, list):
        event = {
            "ifsendalert": True,
            "alerter": ["mail", "wchook"],
            "subject": "[Fallen] 操作失败",
            "summary": "Fallen Alert",
            "content": {
                "工单ID": kwargs.get("woid"),
                "工单标题": kwargs.get("title"),
                "失败原因": "子表单中未发现应用相关信息,请正确填写"
            },
            "sendto": kwargs.get("sendto"),
            "cc": CFG["emailhtml"]["email_cc"]
        }
        send_alert(event)
    else:
        return get_apps_from_subform(subform, clusters, **kwargs)


# return list
def remove_repeat_str(s):
    if not s:
        return s
    ss = filter(None, re.split(r',', s))
    return list(set(ss))


def close_workorder_by_id(woid):
    # is_end: 0 not finish, 1 done
    sql = "update p_work_order_info set is_end = 1 where id = {}".format(
        str(woid))
    LOGGER.info("update sql: {}".format(sql))
    DbHandle = DataBaseHandle()
    data = DbHandle.updateDB(sql)
    if data is False:
        event = {
            "ifsendalert": True,
            "alerter": ["mail", "wchook"],
            "subject": "[Fallen] 更新失败",
            "summary": "Fallen Alert",
            "content": {
                "工单ID": str(woid),
                "失败原因": "更新工单结束状态失败,请OP确认"
            },
            "sendto": [flask_get_oncall_info("op-oncall").get("email")],
            "cc": CFG["emailhtml"]["email_to"]
        }
        send_alert(event)


def get_fallen_creator_and_leader_by_workorderID(woid):
    sql = "select IF(z.user_id=p.creator,'True','False') is_creator, z.email from sys_user z, p_work_order_info p, (select a.user_id, b.leader from sys_user a, sys_dept b where b.dept_id=a.dept_id) c where p.id={} and p.creator=c.user_id and z.user_id in (p.creator, c.leader);".format(
        str(woid))
    LOGGER.info("query sql: {}".format(sql))
    # sql return
    # +------------+---------------------+-----------------------------------+
    # | is_creator | username            | email                             |
    # +------------+---------------------+-----------------------------------+
    # | False      | linchaoqi           | linchaoqi@sensetime.com           |
    # | True       | longxianbing_vendor | longxianbing_vendor@sensetime.com |
    # +------------+---------------------+-----------------------------------+
    DbHandle = DataBaseHandle()
    data = DbHandle.selectDB(sql)
    if data is False or len(data) == 0:
        event = {
            "ifsendalert": True,
            "alerter": ["mail", "wchook"],
            "subject": "[Fallen] 查询失败",
            "summary": "Fallen Alert",
            "content": {
                "工单ID": str(woid),
                "失败原因": "在数据库中查询工单创建人失败,请OP确认"
            },
            "sendto": [flask_get_oncall_info("op-oncall").get("email")],
            "cc": CFG["emailhtml"]["email_to"]
        }
        send_alert(event)
    # if the creator and leader is the same person
    elif len(data) == 1:
        return {
            "creator_email": data[0].get("email"),
            "leader_email": data[0].get("email")
        }
    else:
        (creator_email, leader_email) = (
            data[0].get("email"),
            data[1].get("email")) if data[0].get("is_creator") == "True" else (
                data[1].get("email"), data[0].get("email"))
        return {"creator_email": creator_email, "leader_email": leader_email}
    # like [{'is_creator': 'true', 'username':'creator', 'email': 'creator@sensetime.com'}, {'is_creator': 'false', 'username':'leader', 'email': 'leader@sensetime.com'}]


def flask_get_oncall_info(role):
    x = get_oncall_info_by_role(role)
    # return [] if given email is not exists.
    if not x:
        event = {
            "ifsendalert": True,
            "alerter": ["mail", "wchook"],
            "subject": "[Fallen] 查询失败",
            "summary": "Fallen Alert",
            "content": {
                "角色": str(role),
                "失败原因": "未找到角色相关信息,请OP确认"
            },
            "sendto": CFG["emailhtml"]["email_to"]
        }
        send_alert(event)
    else:
        return {"phone": x[0][1], "email": x[0][2], "role": x[0][3]}


def get_iphone_by_email_from_fallen(email):
    x = get_iphone_role_by_email(email)
    # return [] if given email is not exists.
    if not x:
        event = {
            "ifsendalert": True,
            "alerter": ["mail", "wchook"],
            "subject": "[Fallen] 查询失败",
            "summary": "Fallen Alert",
            "content": {
                "用户EMAIL": str(email),
                "失败原因": "根据用户EMAIL查询手机号为空,请OP确认"
            },
            "sendto": CFG["emailhtml"]["email_to"]
        }
        send_alert(event)
    else:
        return {"phone": x[0][1], "role": x[0][2]}


# DbHandle = DataBaseHandle()
# DbHandle.insertDB("INSERT INTO minitor(id,used_order) VALUES ("999","321")")
# DbHandle.deleteDB("DELETE FROM minitor WHERE id="999"")
# DbHandle.updateDB("UPDATE minitor SET used_order="888" WHERE id="999"")
# dataList = [{"id":123,"used_order":777},{"id":789,"used_order":555}]
# DbHandle.insertListDB("minitor",dataList)
class DataBaseHandle(object):
    def __init__(self):
        self.host = CFG["fallen"]["mysql"]["host"]
        self.port = CFG["fallen"]["mysql"]["port"]
        self.username = CFG["fallen"]["mysql"]["username"]
        self.password = CFG["fallen"]["mysql"]["password"]
        self.database = CFG["fallen"]["mysql"]["database"]
        self.charset = CFG["fallen"]["mysql"]["charset"]
        self.unix_socket = None
        self.db = pymysql.connect(host=self.host,
                                  user=self.username,
                                  password=self.password,
                                  database=self.database,
                                  port=self.port,
                                  unix_socket=self.unix_socket,
                                  charset=self.charset)

    def insertDB(self, sql):
        """插入数据"""
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as err:
            LOGGER.error("insert data error, sql: {}, err: {}".format(
                sql, err))
            self.db.rollback()
        finally:
            self.cursor.close()

    def insertListDB(self, table, dataList):
        """批量插入列表数据
        Params:
            table:插入数据的表名称
            dataList:数据列表 [{key:value,}{key:value,},...]
        """
        self.cursor = self.db.cursor()
        cols = ", ".join("`{}`".format(k) for k in dataList[0].keys())
        val_cols = ", ".join("%({})s".format(k) for k in dataList[0].keys())
        sql = "INSERT INTO {}(%s) values(%s)".format(table)
        res_sql = sql % (cols, val_cols)
        try:
            self.cursor.executemany(res_sql, dataList)
            self.db.commit()
        except Exception as err:
            LOGGER.error("insert many data error, err: {}".format(err))
            self.db.rollback()
        finally:
            self.cursor.close()

    def deleteDB(self, sql):
        """删除数据"""
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as err:
            LOGGER.error("delete data error, sql: {}, err: {}".format(
                sql, err))
            self.db.rollback()
        finally:
            self.cursor.close()

    def updateDB(self, sql):
        """修改数据"""
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as err:
            LOGGER.error("update data error, sql: {}, err: {}".format(
                sql, err))
            return False
            # self.db.rollback()
        finally:
            self.cursor.close()

    def selectDB(self, sql):
        """查询数据"""
        # self.cursor = self.db.cursor()  # 以元组格式返回查询结果
        self.cursor = self.db.cursor(
            cursor=pymysql.cursors.DictCursor)  # 以字典格式返回查询结果
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
        except Exception as err:
            # data = tuple()
            LOGGER.error("query sql error, sql: {}, err: {}".format(sql, err))
            return False
        finally:
            self.cursor.close()
        LOGGER.info(data)
        return data

    def closeDB(self):
        """关闭数据库连接"""
        self.db.close()


def subprocess_exec_cmd(cmd):
    proc = subprocess.Popen(cmd,
                            shell=True,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    std_out, std_err = proc.communicate()
    rnt = proc.returncode
    if rnt != 0:
        return rnt, std_err
    # info is a bytes in py3, but a str in py2
    return rnt, std_out.strip()


'''
@description:
@name: update_dic_in_list_with_another_list
@param {*} old
@param {*} new
@return {*}
@author: zhoushuke
'''


def update_dic_in_list_with_another_list(old=[], new=[]):
    # ps = old
    for x in new:
        for y in old:
            # todo,support update image which is not in old.
            if x["name"] == y["name"]:
                # print(old.index(y))
                # ps[old.index(y)]["value"] = x["version"]
                y["value"] = x["version"]
                break
    return old


def update_values_yaml_of_helm_by_app(src_pth, dst_pth, app, ver=''):
    if not os.path.exists(src_pth) or not os.path.exists(dst_pth):
        return
    with open(src_pth, "rt") as f:
        src_cfg = load(f, Loader=Loader)

    with open(dst_pth, "rt") as h:
        dst_cfg = load(h, Loader=Loader)

    # if app in yaml file, then update context by app's values.yaml, otherwise append to tail.
    # update src values.yaml's version by ver
    if ver:
        src_cfg[app]["tag"] = ver
    dst_cfg[app] = src_cfg[app]

    with open(dst_pth, "w") as f:
        dump(dst_cfg,
             f,
             default_flow_style=False,
             sort_keys=False,
             encoding=("utf-8"),
             allow_unicode=True)
