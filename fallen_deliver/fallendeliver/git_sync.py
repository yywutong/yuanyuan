#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2021-04-20 15:22:57
LastEditors: zhoushuke
LastEditTime: 2021-12-07 13:31:36
FilePath: /fallen_deliver/fallendeliver/git_sync.py
'''

import sys
from config import cfg as CFG
from utils.redis_lock import rds_lock_decorator
from utils.func_ops import parse_from_formdata, get_repo_name_from_repo_url, find_context_in_file_by_re
from utils.git_ops import clone_repo, git_pull_by_app, sync_c4_app_deploy_dir_to_apps_standard, sync_apps_standard_to_c4_standard, sync_apps_standard_to_spring_deploy, sync_app_deploy_dir_to_c4_standard, sync_app_deploy_dir_to_apps_standard, git_expection


@rds_lock_decorator("apps_standard")
def git_sync_to_apps_standard(args, productline="spring"):
    # sleep for random seconds, in case of many workorder to git push at same time
    # time.sleep(random_int(1, 30))
    apps_info = parse_from_formdata(args)
    # apps_info like: {"order_creator_email": "xxx@sensetime.com", apps: [{"name": "xxx", "version": "yyy"}, {}, ...]}}
    apps = apps_info.get("apps")
    wt = {"woid": apps_info.get("woid"), "title": apps_info.get("title")}
    # apps like: [{"name": "xx-test", "version": "oo"}, {"name": "xx-dev", "version": "yy"}, ...]
    repo_path_tmp = CFG["gitinfo"]["git_path_tmp"]
    repo_url = CFG["gitinfo"]["apps_repo"]
    repo_name = get_repo_name_from_repo_url(repo_url)
    repo = clone_repo(repo_url, CFG["gitinfo"]["apps_repo_branch"],
                      repo_path_tmp)
    for app in apps:
        name, version = app.get("name"), app.get("version")
        # maybe have more cluster, just sync test cluster
        if "test" == name.rsplit("-", 1)[1]:
            real_name = name.rsplit("-", 1)[0]
            src_path = repo_path_tmp + "/" + real_name
            dst_path = repo_path_tmp + "/" + repo_name
            if git_pull_by_app(real_name, version, repo_path_tmp):
                sync_app_deploy_dir_to_apps_standard(src_path, dst_path,
                                                     real_name, version,
                                                     productline)
            else:
                git_expection(app, "git pull异常", **wt)
    try:
        repo.config_set()
        repo.add_push_all("auto commit by Fallen")
        # sleep for random seconds
        # time.sleep(random_int(10, 30))
    except Exception:
        git_expection(repo_name, "git push异常", **wt)


@rds_lock_decorator("spring_deploy")
def git_sync_to_spring_deploy(args):
    # sleep for random seconds, in case of many workorder to git push at same time
    # time.sleep(random_int(1, 30))
    # not need to fix app with env choose
    apps_info = parse_from_formdata(args, False)
    # apps_info like: {"order_creator_email": "xxx@sensetime.com", apps: [{"name": "xxx", "version": "yyy"}, {}, ...]}}
    apps = apps_info.get("apps")
    wt = {"woid": apps_info.get("woid"), "title": apps_info.get("title")}
    # apps like: [{"name": "xx", "version": "xx"}, {"name": "yy", "version": "yy"}, ...]
    repo_path_tmp = CFG["gitinfo"]["git_path_tmp"]
    src_repo_url = CFG["gitinfo"]["apps_repo"]
    src_repo_name = get_repo_name_from_repo_url(src_repo_url)
    # clone apps_standard
    clone_repo(src_repo_url, CFG["gitinfo"]["apps_repo_branch"], repo_path_tmp)
    dst_repo_url = CFG["gitinfo"]["ci_repo"]
    dst_repo_name = get_repo_name_from_repo_url(dst_repo_url)
    # clone spring-deploy
    repo = clone_repo(dst_repo_url, CFG["gitinfo"]["ci_branch"], repo_path_tmp)
    src_path = repo_path_tmp + "/" + src_repo_name
    dst_path = repo_path_tmp + "/" + dst_repo_name
    for app in apps:
        name, version = app.get("name"), app.get("version")
        # real_name = name.rsplit("-", 1)[0]
        if find_context_in_file_by_re(
                src_path + "/spring/" + name + "/vars/main.yml",
                "^registry_tag: {}$".format(version)):
            sync_apps_standard_to_spring_deploy(src_path, dst_path, name)
        else:
            git_expection(name, "上线版本与[apps-standard]下/var/main.yml中的版本不匹配",
                          **wt)
    try:
        repo.config_set()
        repo.add_push_all("auto commit by Fallen")
        # time.sleep(random_int(10, 30))
    except Exception:
        git_expection(dst_repo_name, "git push异常", **wt)


@rds_lock_decorator("apps_standard")
def git_sync_c4_app_to_apps_standard(args):
    # sleep for random seconds, in case of many workorder to git push at same time
    # time.sleep(random_int(1, 30))
    apps_info = parse_from_formdata(args)
    # apps_info like: {"order_creator_email": "xxx@sensetime.com", apps: [{"name": "xxx", "version": "yyy"}, {}, ...]}}
    apps = apps_info.get("apps")
    wt = {"woid": apps_info.get("woid"), "title": apps_info.get("title")}
    # apps like: [{"name": "xx-test", "version": "oo"}, {"name": "xx-dev", "version": "yy"}, ...]
    repo_path_tmp = CFG["gitinfo"]["git_path_tmp"]
    repo_url = CFG["gitinfo"]["apps_repo"]
    repo_name = get_repo_name_from_repo_url(repo_url)
    repo = clone_repo(repo_url, CFG["gitinfo"]["apps_repo_branch"],
                      repo_path_tmp)
    for app in apps:
        name, version = app.get("name"), app.get("version")
        # maybe have more cluster, just sync test cluster
        if "test" == name.rsplit("-", 1)[1]:
            real_name = name.rsplit("-", 1)[0]
            src_path = repo_path_tmp + "/" + real_name
            dst_path = repo_path_tmp + "/" + repo_name
            if git_pull_by_app(real_name, version, repo_path_tmp):
                sync_c4_app_deploy_dir_to_apps_standard(
                    src_path, dst_path, real_name, version)
            else:
                git_expection(app, "git pull异常", **wt)
    try:
        repo.config_set()
        repo.add_push_all("auto commit by Fallen")
        # time.sleep(random_int(10, 30))
    except Exception:
        git_expection(repo_name, "git push异常", **wt)


@rds_lock_decorator("c4_standard")
def git_sync_from_apps_standard_c4_standard(args):
    # sleep for random seconds, in case of many workorder to git push at same time
    # time.sleep(random_int(1, 30))
    # not need to fix app with env choose
    apps_info = parse_from_formdata(args, False)
    # apps_info like: {"order_creator_email": "xxx@sensetime.com", apps: [{"name": "xxx", "version": "yyy"}, {}, ...]}}
    apps = apps_info.get("apps")
    wt = {"woid": apps_info.get("woid"), "title": apps_info.get("title")}
    # apps like: [{"name": "xx", "version": "xx"}, {"name": "yy", "version": "yy"}, ...]
    repo_path_tmp = CFG["gitinfo"]["git_path_tmp"]
    src_repo_url = CFG["gitinfo"]["apps_repo"]
    src_repo_name = get_repo_name_from_repo_url(src_repo_url)
    # clone apps_standard
    clone_repo(src_repo_url, CFG["gitinfo"]["apps_repo_branch"], repo_path_tmp)
    dst_repo_url = CFG["c4"]["repo_url"]
    dst_repo_name = get_repo_name_from_repo_url(dst_repo_url)
    # clone spring-deploy
    repo = clone_repo(dst_repo_url, CFG["c4"]["repo_branch"], repo_path_tmp)
    src_path = repo_path_tmp + "/" + src_repo_name
    dst_path = repo_path_tmp + "/" + dst_repo_name
    for app in apps:
        name, version = app.get("name"), app.get("version")
        # real_name = name.rsplit("-", 1)[0]
        if find_context_in_file_by_re(
                src_path + "/c4/" + name + "/values.yaml",
                "\s+tag: {}$".format(version)):
            sync_apps_standard_to_c4_standard(src_path, dst_path, name)
        else:
            git_expection(name, "上线版本与[apps-standard]下/var/main.yml中的版本不匹配",
                          **wt)
    try:
        repo.config_set()
        repo.add_push_all("auto commit by Fallen")
        # time.sleep(random_int(10, 30))
    except Exception:
        git_expection(dst_repo_name, "git push异常", **wt)


# direct copy from app to c4-standard
@rds_lock_decorator("c4_standard")
def git_sync_to_c4_standard(args):
    # sleep for random seconds, in case of many workorder to git push at same time
    # time.sleep(random_int(1, 30))
    apps_info = parse_from_formdata(args, False)
    # apps_info like: {"order_creator_email": "xxx@sensetime.com", apps: [{"name": "xxx", "version": "yyy"}, {}, ...]}}
    apps = apps_info.get("apps")
    wt = {"woid": apps_info.get("woid"), "title": apps_info.get("title")}
    # apps like: [{"name": "xx-test", "version": "oo"}, {"name": "xx-dev", "version": "yy"}, ...]
    repo_path_tmp = CFG["c4"]["git_path_tmp"]
    repo_url = CFG["c4"]["repo_url"]
    repo_name = get_repo_name_from_repo_url(repo_url)
    repo = clone_repo(repo_url, CFG["c4"]["repo_branch"], repo_path_tmp)
    for app in apps:
        name, version = app.get("name"), app.get("version")
        # maybe have more cluster, just sync test cluster
        if "test" == name.rsplit("-", 1)[1]:
            real_name = name.rsplit("-", 1)[0]
            src_path = repo_path_tmp + "/" + real_name
            dst_path = repo_path_tmp + "/" + repo_name
            if git_pull_by_app(real_name, version, repo_path_tmp):
                sync_app_deploy_dir_to_c4_standard(src_path, dst_path,
                                                   real_name, version)
            else:
                git_expection(app, "git pull异常", **wt)
    try:
        repo.config_set()
        repo.add_push_all("auto commit by Fallen")
        # sleep for random seconds
        # time.sleep(random_int(10, 30))
    except Exception:
        git_expection(repo_name, "git push异常", **wt)


if __name__ == "__main__":
    git_sync_to_apps_standard(sys.argv[1])
