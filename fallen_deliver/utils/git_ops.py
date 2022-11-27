#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2021-04-30 09:02:22
LastEditors: zhoushuke
LastEditTime: 2021-04-30 09:26:13
FilePath: /fallen_deliver/utils/git_ops.py
"""

import os
import shutil
from config import cfg as CFG
from loguru import logger as LOGGER
from git.repo import Repo
from git.repo.fun import is_git_dir
from utils.argocd_deploy import Argocd_Deploy_By_App
from utils.func_ops import send_alert, files_not_endwith, replace_string_under_dir, change_main_yaml_version, change_values_yaml_version, get_repo_name_from_repo_url, update_values_yaml_of_helm_by_app


def git_expection(repo, err="GIT ERROR", **kwargs):
    # sendto need to be a list
    LOGGER.error("git ops error: {}".format(err))
    content = {"repo名称": repo, "失败原因": err[0:60]}
    if "woid" in kwargs.keys():
        content["工单ID"] = kwargs.get("woid")
    if "title" in kwargs.keys():
        content["工单标题"] = kwargs.get("title")
    event = {
        "ifsendalert": True,
        "alerter": ["mail", "wchook"],
        "subject": "[Fallen] 同步失败",
        "summary": "Fallen Alert",
        "content": content,
        "sendto": CFG["emailhtml"]["email_to"]
    }
    send_alert(event)


def git_pull_by_app(app, version, repo_tmp="/tmp"):
    # app like 'xxx'
    adba = Argocd_Deploy_By_App()
    # get git repo url, use test env
    repo_url = adba.get_app_obj(app + "-test")["spec"]["source"]["repoURL"]
    # "repoURL": "https://gitlab.bj.sensetime.com/zhoushuke/argocd-kustomize-frontend.git"
    # add username and password
    repo_url = repo_url.split(
        "://")[0] + "://" + CFG["gitinfo"]["git_username"] + ":" + CFG[
            "gitinfo"]["git_password"] + "@" + repo_url.split("://")[1]
    try:
        local_path = os.path.join(repo_tmp, app)
        repo = GitRepository(local_path, repo_url)
        # can't checkout directly, because may in a detached head
        # repo.pull()
        # so, can still in master branch, but checkout head hard to commit
        repo.checkout(version)
        return True
    except Exception:
        return False


def clone_repo(url, branch="master", repo_tmp="/tmp"):
    repo_name = get_repo_name_from_repo_url(url)
    local_path = os.path.join(repo_tmp, repo_name)
    try:
        # delete first if local path exists
        # if os.path.exists(local_path):
        #     shutil.rmtree(local_path)
        repo = GitRepository(local_path, url, branch)
        # checkout is ok ,becease current status is in a branch
        repo.change_to_branch(branch)
        repo.pull()
        return repo
    except Exception:
        git_expection(repo_name, "git clone异常")


# from app to apps-standard
def sync_app_deploy_dir_to_apps_standard(src_path, dst_path, app, version,
                                         productline):
    try:
        p = dst_path + "/{}/".format(productline) + app
        if not os.path.exists(p):
            os.makedirs(p)
        # cp deploy dir, dirs_exist_ok need python 3.8+
        if os.path.exists(src_path + "/deploy"):
            shutil.copytree(src_path + "/deploy",
                            dst_path + "/{}/{}".format(productline, app),
                            ignore=shutil.ignore_patterns("overlay"),
                            dirs_exist_ok=True)
        # overwrite overlay dir if dst_path overlay not exists
        # todo, make a better template tool like cookiecutter
        if not os.path.exists(
                dst_path + "/{}/{}/overlay".format(productline, app)
        ) and os.path.exists(CFG["gitinfo"]["kustomize_overlay"] + "/overlay"):
            shutil.copytree(CFG["gitinfo"]["kustomize_overlay"] + "/overlay",
                            dst_path +
                            "/{}/{}/overlay".format(productline, app),
                            dirs_exist_ok=True)
            # replace MODULENAME in overlay dir
            replace_string_under_dir(
                dst_path + "/{}/{}/overlay".format(productline, app),
                "MODULEXNAME", app)
        # update version in main.yaml
        if os.path.exists(dst_path +
                          "/{}/{}/vars/main.yml".format(productline, app)):
            change_main_yaml_version(
                dst_path + "/{}/{}/vars/main.yml".format(productline, app),
                app, version)
        # todo, add argo-rollout canary cd
        # change deployment to rollout
    except Exception:
        git_expection(app, "同步git路径异常,请确认应用[deploy]目录是否符合要求")


def sync_c4_app_deploy_dir_to_apps_standard(src_path, dst_path, app, version):
    try:
        p = dst_path + "/c4/" + app
        if not os.path.exists(p):
            os.makedirs(p)
        # cp deploy dir, dirs_exist_ok need python 3.8+
        if os.path.exists(src_path + "/deploy"):
            shutil.copytree(src_path + "/deploy",
                            dst_path + "/c4/{}".format(app),
                            dirs_exist_ok=True)
        # update version in values.yaml
        if os.path.exists(dst_path + "/c4/{}/values.yaml".format(app)):
            change_values_yaml_version(
                dst_path + "/c4/{}/values.yaml".format(app), app, version)
        # todo, add argo-rollout canary cd
        # change deployment to rollout
    except Exception:
        git_expection(app, "同步git路径异常,请确认应用[deploy]目录是否符合要求")


# direct copy from app to c4-standard
def sync_app_deploy_dir_to_c4_standard(src_path, dst_path, app, version):
    try:
        p = dst_path + "/templates/" + app
        if not os.path.exists(p):
            os.makedirs(p)
        # cp deploy dir, dirs_exist_ok need python 3.8+
        if os.path.exists(src_path + "/deploy"):
            shutil.copytree(src_path + "/deploy/templates",
                            dst_path + "/templates/{}".format(app),
                            dirs_exist_ok=True)
        # update version in values.yaml
        update_values_yaml_of_helm_by_app(src_path + "/deploy/values.yaml",
                                          dst_path + "/values.yaml", app,
                                          version)
    except Exception:
        git_expection(app, "同步git路径异常,请确认应用[deploy]目录是否符合要求")


def sync_apps_standard_to_c4_standard(src_path, dst_path, app):
    try:
        p = dst_path + "/templates/" + app
        if not os.path.exists(p):
            os.makedirs(p)
        # cp deploy dir, dirs_exist_ok need python 3.8+
        if os.path.exists(src_path + "/templates"):
            shutil.copytree(src_path + "/templates",
                            dst_path + "/templates/{}".format(app),
                            dirs_exist_ok=True)
        # update version in values.yaml
        update_values_yaml_of_helm_by_app(
            src_path + "/c4/{}/values.yaml".format(app),
            dst_path + "/values.yaml", app)
    except Exception:
        git_expection(app, "同步git路径异常,请确认应用[deploy]目录是否符合要求")


# from apps-standard to spring-deploy
def sync_apps_standard_to_spring_deploy(src_path, dst_path, app):
    try:
        for d in ["/files", "/tasks", "/templates", "/vars"]:
            p = dst_path + "/ansible/roles/" + app + d
            if not os.path.exists(p):
                os.makedirs(p)
                if "/tasks" == d:
                    # touch tasks/main.yml
                    shutil.copyfile(
                        CFG["gitinfo"]["kustomize_overlay"] +
                        "/ansible-tasks-main.yml", dst_path +
                        "/ansible/roles/{}/tasks/main.yml".format(app))
        # if have files dir
        if os.path.exists(src_path + "/spring/{}/files".format(app)):
            shutil.copytree(src_path + "/spring/{}/files".format(app),
                            dst_path + "/ansible/roles/{}/files".format(app),
                            dirs_exist_ok=True)
        # if have sql files, need to cp to infra-db dir
        if os.path.exists(src_path + "/spring/{}/files/sqls".format(app)):
            db_dir = dst_path + "/ansible/roles/infra-db/files/{}".format(app)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
            not_sqls = files_not_endwith(".sql")
            shutil.copytree(src_path + "/spring/{}/files/sqls".format(app),
                            db_dir,
                            ignore=not_sqls,
                            dirs_exist_ok=True)
        # cp base/*.j2 to ansible role/templates
        if os.path.exists(src_path + "/spring/{}/base".format(app)):
            not_j2 = files_not_endwith(".j2")
            shutil.copytree(src_path + "/spring/{}/base".format(app),
                            dst_path +
                            "/ansible/roles/{}/templates".format(app),
                            ignore=not_j2,
                            dirs_exist_ok=True)
        # cp main.yml
        if os.path.exists(src_path + "/spring/{}/vars/main.yml".format(app)):
            shutil.copyfile(
                src_path + "/spring/{}/vars/main.yml".format(app),
                dst_path + "/ansible/roles/{}/vars/main.yml".format(app))
    except Exception:
        git_expection(app, "同步git路径异常,请确认[apps-standard]下的目录是否符合要求")


class GitRepository(object):
    """
    git仓库管理
    """
    def __init__(self, local_path, repo_url, branch="master"):
        self.local_path = local_path
        self.repo_url = repo_url
        self.repo = None
        self.initial(repo_url, branch)

    def initial(self, repo_url, branch):
        """
        初始化git仓库
        :param repo_url:
        :param branch:
        :return:
        """
        # delete first if local path exists
        if os.path.exists(self.local_path):
            shutil.rmtree(self.local_path)
        # recreate
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)

        git_local_path = os.path.join(self.local_path, ".git")
        if not is_git_dir(git_local_path):
            self.repo = Repo.clone_from(repo_url,
                                        to_path=self.local_path,
                                        branch=branch)
        else:
            self.repo = Repo(self.local_path)

    def pull(self):
        """
        从线上拉最新代码
        :return:
        """
        self.repo.git.pull()

    def branches(self):
        """
        获取所有分支
        :return:
        """
        branches = self.repo.remote().refs
        return [
            item.remote_head for item in branches if item.remote_head not in [
                "HEAD",
            ]
        ]

    def commits(self):
        """
        获取所有提交记录
        :return:
        """
        commit_log = self.repo.git.log(
            "--pretty={\"commit\":\"%h\",\"author\":\"%an\",\"summary\":\"%s\",\"date\":\"%cd\"}",
            max_count=50,
            date="format:%Y-%m-%d %H:%M")
        log_list = commit_log.split("\n")
        return [eval(item) for item in log_list]

    def tags(self):
        """
        获取所有tag
        :return:
        """
        return [tag.name for tag in self.repo.tags]

    def change_to_branch(self, branch):
        """
        切换分支
        :param branch:
        :return:
        """
        self.repo.git.checkout(branch)

    def change_to_commit(self, commit, branch="master"):
        """
        切换commit
        :param branch:
        :param commit:
        :return:
        """
        self.change_to_branch(branch=branch)
        self.repo.git.reset("--hard", commit)

    def checkout(self, version):
        """
        切换tag or tag
        :param version:
        :return:
        """
        self.repo.git.checkout(version)

    def config_set(self):
        self.repo.config_writer().set_value("user", "email",
                                            "Fallen@sensetime.com").release()
        self.repo.config_writer().set_value("user", "name", "Fallen").release()

    def add_push_all(self, msg):
        """
        提交所有更新
        :param tag:
        :return:
        """
        self.repo.git.add(".")
        self.repo.git.commit("-m", msg, "--allow-empty")
        self.repo.git.push()


if __name__ == "__main__":
    local_path = os.path.join("codes", "t1")
    repo = GitRepository(local_path, "https://xxx.git")
    repo.change_to_branch("dev")
    repo.pull()
