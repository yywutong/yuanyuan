# -*-coding:utf-8-*-


import pytest
from APIAuto.util.api_func import *
from utils.HandleThreadPool import *
from utils.HandleLogging import HandleLogging
from utils.HandleENV import HandleENV
import logging
import baseconfig
import traceback

logger = HandleLogging(file_name="test").getlog()
# 获取proto的全路径
base_proto = baseconfig.grpc_proto
proto_file_path = os.path.join(base_proto, "c4_platform.proto")
# host = os.environ.get("C4_URL")
host = HandleENV().get_env("C4_URL")

checker = 14  # test_user
reviewer = 13  # test_admin
analysis_name = set()
review_name = set()


@pytest.mark.parametrize("login", [{'user': 'test_admin', 'passwd': '123456'}], indirect=True)
def test_create_review_task(login):
    # 创建缺陷审核任务-智能分配
    type = 0  # 缺陷审核
    analysis = list_finished_analysis(login, pcount=100, pno=1)
    for analysis in analysis:
        analysis_id = analysis["id"]
        name = analysis["name"]
        add_filter(login)
        filters = list_filter(login, filter_type=type, pcount=50, pno=1)
        for filter in filters:
            filter_id = filter["id"]
            works = [{"id": 1, "checker": checker, "reviewer": reviewer, "percentage": 100, "image_num": 0}]
            works, filter_hash, _, _ = smart_review_compute(login, analysis_id=analysis_id, filter_id=filter_id,
                                                            works=works, task_type=type, ratio=0, rule=4)  # rule=4智能分配
            if works:
                smart_review_confirm(login, analysis_id, filter_id, task_type=type, works=works, ratio=0, rule=4)
                analysis_name.add(name)  # 将审核任务名称暂存
        time.sleep(3)


@pytest.mark.parametrize("login", [{'user': 'test_user', 'passwd': '123456'}], indirect=True)
def test_check_work(login):
    if analysis_name:
        for name in analysis_name:
            # 等待审核工单派发完成
            wait_review_order(login, name=name, status=10, time_out=1800)
            # 审核工单
            review_work(login, name=name, user_id=checker, status=10, type=1)
            review_name.add(name)
            analysis_name.remove(name)


@pytest.mark.parametrize("login", [{'user': 'test_admin', 'passwd': '123456'}], indirect=True)
def test_review_work(login):
    if review_name:
        for name in review_name:
            # 等待复核工单派发完成
            wait_review_order(login, name=name, status=13, time_out=1800)
            # 复核工单
            review_work(login, name=name, user_id=reviewer, status=13, type=2)
            # 等待缺陷入库完成
            wait_review_order(login, name=name, status=3, time_out=1800)
            # 合并工单
            merge_work(login, name=name, user_id=reviewer)


def review_work_stability_test(login):
    try:
        thread = ThreadPool(timeout=50, workers=3,
                            funcs=[(test_create_review_task, [login]),
                                   (test_check_work, [login]),
                                   (test_review_work, [login])])
        thread.run_tread()
    except:
        logger.error(f"Traceback.format_exc: {traceback.format_exc()}")


if __name__ == '__main__':
    pytest.main(['-s', 'test_ReviewWork.py:review_work_stability_test'])

