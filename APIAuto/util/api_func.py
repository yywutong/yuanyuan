# -*-coding:utf-8-*-

import os, sys, json
import time
from client.GrpcClient import GrpcClient
from utils.HandleGrpcRes import HandleGrpcRes
from utils.HandleLogging import HandleLogging
import baseconfig
import logging

logger = HandleLogging(file_name="test").getlog()
# 获取proto的全路径
base_proto = baseconfig.grpc_proto
proto_file_path = os.path.join(base_proto, "c4_platform.proto")
# host = os.environ.get("C4_URL")
host = "10.4.196.105:30137"


def wait_data_loaded(login, time_out=300):
    """等待数据加载完成"""
    logger.error("--------{}开始等待--------".format(wait_data_loaded.__name__))
    start_time = time.time()
    time.sleep(1)
    client = GrpcClient(host, proto_file_path, login)
    while True:
        res = client.run("ListDirFileInfo", name='接口测试', analysis_status=1, line='接口测试', office='接口测试', pcount=1,
                         pno=1)  # analysis_status=1未分析
        handleGrpcRes = HandleGrpcRes(res)
        data = handleGrpcRes.get_data_item("data")
        print(f"wait_data_loaded data:{data}")
        end_time = time.time()
        load_status = data['dir_file_infos'][0]['status']
        if load_status == 2:  # 1-数据统计中，2-统计完成
            name = data['dir_file_infos'][0]['name']
            data_path = data['dir_file_infos'][0]['data_path']
            direction = data['dir_file_infos'][0]['direction']
            logger.error(f"分析任务：{name},数据加载时长：{end_time - start_time}")
            return name, data_path, direction
        else:
            time.sleep(1)
        if end_time - start_time > time_out:
            return '等待超时'


def wait_task_analysis_complete(login, name, time_out=3600):
    """等待审核任务审核完成"""
    logger.error("--------{}开始等待--------".format(wait_task_analysis_complete.__name__))
    start_time = time.time()
    time.sleep(30)
    client = GrpcClient(host, proto_file_path, login)
    while True:
        res = client.run("ListDirFileInfo", name=name, pcount=1, pno=1)
        handleGrpcRes = HandleGrpcRes(res)
        data = handleGrpcRes.get_data_item("data")
        print(f"analysis res:{data}")
        end_time = time.time()
        analysis_status = data['dir_file_infos'][0]['analysis_status']
        if analysis_status == 5:  # 1-未分析，2-等待分析，3-分析中，4-失败，5-分析完成
            logger.error(f"分析任务：{name}，分析时长：{end_time - start_time}")
            return "分析完成"
        elif analysis_status == 4:
            logger.error(f"任务：{name}，分析失败")
            return "分析失败"
        else:
            time.sleep(120)
        if end_time - start_time > time_out:
            logger.error(f"任务：{name}，等待超时")
            return '等待超时'


def wait_review_order(login, name, status=10, time_out=1800):
    """
    等待审核、复核工单派发完成
    :param login:
    :param name: 任务名称
    :param status: 10-审核中-审核工单派发完成，13-复核中-复核工单派发完成， 3-完成-缺陷入库完成。
    :param time_out:
    :return:
    """
    logger.error("--------{}开始等待--------".format(wait_review_order.__name__))
    start_time = time.time()
    time.sleep(2)
    client = GrpcClient(host, proto_file_path, login)
    while True:
        res = client.run("ListReview", name=name, pcount=5, pno=1)
        handleGrpcRes = HandleGrpcRes(res)
        data = handleGrpcRes.get_data_item("data")
        end_time = time.time()

        review_status = data['reviews'][0]['status']
        if review_status == status:  # 审核中，代表审核工单派发完成
            logger.error(f"任务：{name}，状态扭转时长：{end_time - start_time}")
            return "审核工单派发完成"
        else:
            time.sleep(2)
        if end_time - start_time > time_out:
            logger.error(f"任务：{name}，等待超时review_status：{review_status}")
            return '等待超时'


# ----------------------------------------------------------------------------------------------审核工单

def list_analysis(login, name):
    """工作台列表，获取analyses_id"""
    logger.error(f"获取analyses_id, 任务名称：{name}")
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("ListAnalysis", name=name, analysis_status=10, pcount=7, pno=1)
    handleGrpcRes = HandleGrpcRes(res)
    analyses_id = handleGrpcRes.get_data_item("data")['analyses'][0]['id']
    return analyses_id


def list_review(login, name):
    """审核任务列表，获取reviews_id"""
    """
    filter_type: 1-零部件审核任务列表，不传-缺陷审核任务列表
    """
    logger.error(f"获取reviews_id")
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("ListReview", name=name, pcount=7, pno=1)
    handleGrpcRes = HandleGrpcRes(res)
    reviews_id = handleGrpcRes.get_data_item("data")['reviews'][0]['id']
    return reviews_id


def list_work(login, name, user_id):
    """工作台列表，获取work_id"""
    logger.error(f"获取work_id")
    # logger.error("--------{}测试开始--------".format(sys._getframe().f_code.co_name))
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("ListWork", user_id=user_id, pcount=10, pno=1, analysis_name=name,
                     task_status=1)  # 参数增加task_status
    handleGrpcRes = HandleGrpcRes(res)
    works = handleGrpcRes.get_data_item("data")['works']
    return works


def start_work(login, work_id, review_id):
    """开始审核"""
    logger.error(f"work_id: {work_id}")
    # logger.error("--------{}测试开始--------".format(sys._getframe().f_code.co_name))
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("StartWork", work_id=work_id, review_id=review_id)  # 参数增加review_id
    handleGrpcRes = HandleGrpcRes(res)
    data = handleGrpcRes.get_data_item("data")
    return data


def list_pole(login, work_id, type, analysis_id):
    """杆号列表，获取杆号id"""
    # logger.error("--------{}测试开始--------".format(sys._getframe().f_code.co_name))
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("ListPole", type=type, work_id=work_id, analysis_id=analysis_id)  # 增加analysis_id
    handleGrpcRes = HandleGrpcRes(res)
    data = handleGrpcRes.get_data_item("data")
    return data


def list_unit(login, analysis_id, review_id, pole_id, work_id, type):
    """图片列表，获取图片id"""
    # logger.error("--------{}测试开始--------".format(sys._getframe().f_code.co_name))
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("ListUnit", analysis_id=analysis_id, review_id=review_id, type=type, pole_id=pole_id,
                     work_id=work_id)  # 增加review_id，analysis_id
    handleGrpcRes = HandleGrpcRes(res)
    units = handleGrpcRes.get_data_item("data")['units']
    return units


def get_unit(login, analysis_id, image_id, pole_id, review_id, unit_id, type):
    """获取图片信息"""
    # logger.error("--------{}测试开始--------".format(sys._getframe().f_code.co_name))
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("GetUnit", analysis_id=analysis_id, image_id=image_id, pole_id=pole_id, review_id=review_id,
                     type=type, unit_id=unit_id)  # 增加review_id，pole_id，image_id，analysis_id
    handleGrpcRes = HandleGrpcRes(res)
    analysis = handleGrpcRes.get_data_item("data")['analysis']
    return analysis


def update_unit(login, analysis_id, image_id, pole_id, review_id, analysis, unit_id, type):
    """审核图片"""
    # logger.error("--------{}测试开始--------".format(sys._getframe().f_code.co_name))
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("UpdateUnit", analysis_id=analysis_id, image_id=image_id, pole_id=pole_id, review_id=review_id,
                     type=type, defect=analysis, unit_id=unit_id)  # review_id，pole_id，image_id，analysis_id
    handleGrpcRes = HandleGrpcRes(res)
    msg = handleGrpcRes.get_data_item("msg")
    return msg


def submit_work(login, work_id, type):
    """提交审核"""
    # logger.error("--------{}测试开始--------".format(sys._getframe().f_code.co_name))
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("SubmitWork", work_id=work_id, type=type)
    handleGrpcRes = HandleGrpcRes(res)
    data = handleGrpcRes.get_data_item("msg")
    assert data == 'success'


def review_work(login, name, user_id=14, status=10, type=1):
    """
    审核、复核 工单流程
    :param login:
    :param user_id: test_user id=14, test_admin id=13
    :param name: 任务名称
    :param status: 10-审核中，13-复核中
    :param type: 1-审核，2-复核
    :return:
    """
    analysis_id = list_analysis(login, name)
    review_id = list_review(login, name)
    # 工作台列表，获取work id
    works = list_work(login, name, user_id)
    count = 0
    for work in works:
        if work['status'] == status:
            work_id = work['id']
            # 开始审核
            start_work(login, work_id, review_id)
            # 获取杆号id
            data = list_pole(login, work_id, type, analysis_id)
            if data:  # 如果poles非空进行审核图片；poles=[]则直接提交工单
                poles = data['poles']
                for pole in poles:
                    pole_id = pole['id']
                    # 获取图片id
                    units = list_unit(login, analysis_id, review_id, pole_id, work_id, type)

                    for unit in units:
                        if unit.get('id', 0) != 0:  # id==0是隐藏的图片
                            unit_id = unit['id']
                            image_id = unit['image_id']
                            # 获取图片信息
                            analysis = get_unit(login, analysis_id, image_id, pole_id, review_id, unit_id, type)
                            # 提交审核单张图片
                            update_unit(login, analysis_id, image_id, pole_id, review_id, analysis, unit_id, type)
                            count = count + 1
                            print(f"count: {count}")
            # 提交审核工单
            submit_work(login, work_id, type)


# -------------------------------------------------------------------------------------------合并工单

def list_defect_business_pole(login, review_id):
    """获取业务缺陷库杆号列表, /v1/defect_business/list_pole"""
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("ListDefectBusinessPole", review_id=review_id)  # analysis_id
    handleGrpcRes = HandleGrpcRes(res)
    poles = handleGrpcRes.get_data_item("data")["poles"]
    return poles


def get_business_pole_defect(login, review_id, pole_id, pno, pcount):
    """v1/defect_business/list_pole_defect"""
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("GetBusinessPoleDefect", review_id=review_id, pole_id=pole_id, pno=pno,
                     pcount=pcount)  # analysis_id
    handleGrpcRes = HandleGrpcRes(res)
    defects = handleGrpcRes.get_data_item("data")["defects"]
    return defects


def submit_defect_business_data(login, defects):
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("SubmitDefectBusinessData", defects=defects)
    handleGrpcRes = HandleGrpcRes(res)
    data = handleGrpcRes.get_data_item("msg")
    assert data == 'success'


def merge_work(login, name, user_id):
    """
    合并工单审核流程
    :param login:
    :param name: 数据档案名称
    :param user_id:
    :return:
    """
    start_time = time.time()
    while 1:
        works = list_work(login, name, user_id)
        if not len(works):
            work_id = works[0]['id']
            review_id = list_review(login, name)
            poles = list_defect_business_pole(login, review_id)
            for pole in poles:
                pole_id = pole['id']
                defects = get_business_pole_defect(login, review_id, pole_id, 1, 100)
                submit_defect_business_data(login, defects)
            submit_work(login, work_id, 3)  # type=3
        else:
            time.sleep(5)
            if time.time() - start_time > 600:
                logging.info(f'任务：{name}，合并工单未生成。')


# -------------------------------------------------------------------------------------------------------创建审核任务


def list_finished_analysis(login, pcount=5, pno=1, name=None):
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("ListFinishedAnalysis", name=name, pcount=pcount, pno=pno)
    handleGrpcRes = HandleGrpcRes(res)
    analyses = handleGrpcRes.get_data_item("data")["analyses"]
    return analyses


def add_filter(login, filter_type=0, filter=None):
    # filter_type=0
    if filter:
        filters = filter
    else:  # 209全部缺陷
        filter_name = f"stability全部缺陷{time.strftime('%Y%m%d')}"
        structure_value = [["chenglisuo","chenglisuo"],["chenglisuo","chenglisuojietouxianjia"],["chenglisuo","yujiaosi"],["chenglisuo","zhongduanmaoguxianjia"],["chenglisuo","yujiaoshinaizhangxianjia"],["jiechuxian","jiechuxian"],["jiechuxian","jiechuxianjietouxianjia"],["jiechuxian","jiechuxiandiaoxianxianjia"],["jiechuxian","zhongduanmaoguxianjia"],["zhengtidiaoxian（rouxing）","chenglisuodiaoxianxianjia"],["zhengtidiaoxian（rouxing）","jiechuxiandiaoxianxianjia"],["zhengtidiaoxian（rouxing）","diaoxian"],["zhengtidiaoxian（rouxing）","zailiuhuan"],["zhengtidiaoxian（rouxing）","qianyaguan"],["zhengtidiaoxian（rouxing）","shangxinxinghuan"],["zhengtidiaoxian（rouxing）","xiaxinxinghuan"],["zhengtidiaoxian（rouxing）","yajieduanzi"],["zhengtidiaoxian（rouxing）","zhidongkakuai"],["dingweiguandiaoxian","shangxinxinghuan"],["dingweiguandiaoxian","xiaxinxinghuan"],["jiechuxianzhongxinmaojie","shangxinxinghuan"],["jiechuxianzhongxinmaojie","xiaxinxinghuan"],["jiechuxianzhongxinmaojie","zhongxinmaojiesheng"],["jiechuxianzhongxinmaojie","qianyaguan"],["jiechuxianzhongxinmaojie","jiechuxianzhongxinmaojiexianjia"],["gudingshengxielaxian","shangxinxinghuan"],["gudingshengxielaxian","xiaxinxinghuan"],["zhengtidiaoxian（gangxing）","rishidiaoxian"],["chenglisuozhongxinmaojie","zhongxinmaojiesheng"],["chenglisuozhongxinmaojie","chenglisuozhongxinmaojiexianjia"],["dianlianjie","dianlianjie"],["dianlianjiexianjia","dianlianjiexianjia"],["dianlianjiexianjia","binggouxianjia"],["xiancha","xiancha"],["fenduanjueyuanqi","zhongduanmaoguxianjia"],["fenduanjueyuanqi","fenduanjueyuanqi"],["jueyuanzi","bangshijueyuanzi"],["jueyuanzi","jueyuanzijinju"],["jueyuanzi","jieditiaoxian"],["jueyuanzi","jieditiaoxianzhen"],["jueyuanzi","jueyuanzitiemoyaban"],["luomaozhuangzhi","buchangsheng"],["luomaozhuangzhi","shuangerxiexingxianjia"],["luomaozhuangzhi","luomao-jihecanshu"],["luomaozhuangzhi","zhuituo"],["luomaozhuangzhi","zhuituobaogu"],["luomaozhuangzhi","zhuituoxianzhijia"],["luomaozhuangzhi","pinghenglun"],["luomaozhuangzhi","jilun"],["luomaozhuangzhi","zhidongkakuai"],["luomaozhuangzhi","jilundizuo"],["luomaozhuangzhi","jilunquniaozhao"],["luomaozhuangzhi","buchanglun"],["luomaozhuangzhi","chuhuangan"],["luomaozhuangzhi","shuangerlianjieqi"],["luomaozhuangzhi","luomaojiaogang"],["luomaozhuangzhi","xiamaodizuo"],["luomaozhuangzhi","fujiaxuanguadiaozhu"],["luomaozhuangzhi","diaozhudizuo"],["dengdianweixian","dengdianweixian"],["tanxingdiaosuo","tanxingdiaosuo"],["wanbi","wanbi"],["wanbi","jieditiaoxian"],["wanbi","jieditiaoxianzhen"],["wanbi","jieditiaoxianjianjia"],["wanbi","binggouxianjia"],["pingwanbi-dizuo","wanbidizuo"],["pingwanbi-dizuo","shuangwanbihengchengdizuo"],["pingwanbi-dizuo","daxianjiekuangjia"],["xiewanbi-dizuo","wanbidizuo"],["xiewanbi-dizuo","shuangwanbihengchengdizuo"],["jueyuanzijinju","jueyuanzijinju"],["jueyuanzifangtuojian","jueyuanzijinju"],["ruansuoshiyinghengkua(liang）","jieditiaoxian"],["ruansuoshiyinghengkua(liang）","jieditiaoxianzhen"],["ruansuoshiyinghengkua(liang）","jieditiaoxianjianjia"],["ruansuoshiyinghengkua(liang）","binggouxianjia"],["zhenshijueyuanzi","zhenshijueyuanzi"],["wanbi-L","taoguandaner"],["wanbi-L","taoguanzuo"],["wanbi-L","chenglisuozuo"],["wanbi-L","yujiaosi"],["wanbi-L","xiewanbiguan"],["wanbi-L","wanbizhicheng"],["wanbi-L","dingweiguanzhicheng"],["wanbizhicheng-L","taotongshuanger"],["wanbizhicheng-L","wanbizhicheng"],["dingweizhuangzhi-L","taotongshuanger"],["dingweizhuangzhi-L","wanbizhicheng"],["dingweizhuangzhi-L","taoguandaner"],["dingweizhuangzhi-L","dingweiguan"],["dingweizhuangzhi-L","dingweiguandiaoxian"],["dingweizhuangzhi-L","dingweizhizuo"],["dingweizhuangzhi-L","Pxingsuidaodingweizhizuo"],["dingweizhuangzhi-L","zhangdingweizhizuo"],["dingweizhuangzhi-L","rishidingweizhizuo"],["dingweizhuangzhi-L","dianqilianjietiaoxian"],["dingweizhuangzhi-L","dingweiqi"],["dingweizhuangzhi-L","dingweiqixianjia"],["dingweizhuangzhi-L","maozhidingweiqiazi"],["dingweizhuangzhi-L","pingwanbiguan"],["dingweizhuangzhi-L","guanmao"],["dingweizhuangzhi-L","dingweiguanzhicheng"],["dingweizhuangzhi-L","zhichiqi"],["dingweizhuangzhi-L","zhichiqidingweiqi"],["dingweizhuangzhi-L","fangfenglaxian"],["dingweizhuangzhi-G","dingweiguan"],["dingweizhuangzhi-G","dingweiguandiaoxian"],["dingweizhuangzhi-G","dianqilianjietiaoxian"],["dingweizhuangzhi-G","dingweiqi"],["dingweizhuangzhi-G","dingweiqixianjia"],["dingweizhuangzhi-G","maozhidingweiqiazi"],["dingweizhuangzhi-G","pingwanbiguan"],["dingweizhuangzhi-G","guanmao"],["dingweizhuangzhi-G","qiazi"],["dingweizhuangzhi-G","dingweihuan"],["dingweizhuangzhi-G","zhichiqi"],["dingweizhuangzhi-G","zhichiqidingweiqi"],["dingweizhuangzhi-G","fangfenglaxian"],["lvhejindingweihuan","taotongshuanger"],["ruansuoshiyinghengkua（liang）","dianqilianjietiaoxian"],["ruansuoshiyinghengkua（liang）","dingweiqi"],["ruansuoshiyinghengkua（liang）","dingweiqixianjia"],["ruansuoshiyinghengkua（liang）","maozhidingweiqiazi"],["ruansuoshiyinghengkua（liang）","pingwanbiguan"],["ruansuoshiyinghengkua（liang）","guanmao"],["ruansuoshiyinghengkua（liang）","zhichiqi"],["ruansuoshiyinghengkua（liang）","zhichiqidingweiqi"],["ruansuoshiyinghengkua（liang）","yinghengliang"],["ruansuoshiyinghengkua（liang）","xuandiaodizuo"],["ruansuoshiyinghengkua（liang）","gudingshengjiaogang"],["ruansuoshiyinghengkua（liang）","tiaojieluoshuan"],["ruansuoshiyinghengkua（liang）","shuangerlianjieqi"],["ruansuoshiyinghengkua（liang）","shuangerxiexingxianjia"],["ruansuoshiyinghengkua（liang）","chuzuoxiexingxianjia"],["ruansuoshiyinghengkua（liang）","tanhuangbuchangqi"],["ruansuoshiyinghengkua（liang）","gudingsheng"],["ruansuoshiyinghengkua（liang）","gudingshengdengdianweixian"],["ruansuoshiyinghengkua（liang）","xiediaoxian"],["ruansuoshiyinghengkua（liang）","fangfenglaxian"],["ruansuoshiyinghengkua（liang）","dingweihuanxianjia"],["ruansuoshiyinghengkua（liang）","tiaojielizhu"],["ruansuoshiyinghengkua（liang）","xuandiaohualun"],["ruansuoshiyinghengkua（liang）","dingweiqidingweihuan"],["ruansuoshiyinghengkua（liang）","dingweijiahuan"],["wanbizhicheng-G","qiazi"],["wanbi-G","chenglisuozuo"],["wanbi-G","xiewanbiguan"],["quniaozhuangzhi","quniaozhao"],["zhengkuixian（AF）","fujiaxian"],["zhengkuixian（AF）","zhengkuixianyujiaoshinaizhangjiexutiao"],["zhengkuixian（AF）","xiamaodizuo"],["zhengkuixian（AF）","chuhuangan"],["zhengkuixian（AF）","yujiaoshinaizhangxianjia"],["zhengkuixian（AF）","naizhangxianjia"],["zhengkuixian（AF）","duimaoxian"],["zhengkuixian（AF）","binggouxianjia"],["zhengkuixian（AF）","jianjia"],["zhengkuixian（AF）","jianjiadizuo"],["zhengkuixian（AF）","xuanchuixianjia"],["zhengkuixian（AF）","qiutouguahuan"],["zhengkuixian（AF）","xuanshijueyuanzi"],["zhengkuixian（AF）","xuanshijueyuanzijinju"],["zhengkuixian（AF）","zhichijueyuanzigaiban"],["zhengkuixian（AF）","chuzuoanzi"],["zhengkuixian（AF）","shuangeranzi"],["zhengkuixian（AF）","zhizuo"],["zhengkuixian（AF）","zhudinggaiban"],["zhengkuixian（AF）","zhudingdizuo"],["gongdianxian","fujiaxian"],["gongdianxian","zhengkuixianyujiaoshinaizhangjiexutiao"],["gongdianxian","xiamaodizuo"],["gongdianxian","chuhuangan"],["gongdianxian","yujiaoshinaizhangxianjia"],["gongdianxian","naizhangxianjia"],["gongdianxian","duimaoxian"],["gongdianxian","binggouxianjia"],["gongdianxian","jianjia"],["gongdianxian","jianjiadizuo"],["gongdianxian","xuanchuixianjia"],["gongdianxian","qiutouguahuan"],["gongdianxian","xuanshijueyuanzi"],["gongdianxian","xuanshijueyuanzijinju"],["gongdianxian","zhichijueyuanzigaiban"],["gongdianxian","chuzuoanzi"],["gongdianxian","shuangeranzi"],["gongdianxian","zhizuo"],["gongdianxian","zhudinggaiban"],["gongdianxian","zhudingdizuo"],["huiliuxian（NF）","fujiaxian"],["huiliuxian（NF）","zhengkuixianyujiaoshinaizhangjiexutiao"],["huiliuxian（NF）","xiamaodizuo"],["huiliuxian（NF）","chuhuangan"],["huiliuxian（NF）","yujiaoshinaizhangxianjia"],["huiliuxian（NF）","naizhangxianjia"],["huiliuxian（NF）","duimaoxian"],["huiliuxian（NF）","binggouxianjia"],["huiliuxian（NF）","jianjia"],["huiliuxian（NF）","jianjiadizuo"],["huiliuxian（NF）","xuanchuixianjia"],["huiliuxian（NF）","qiutouguahuan"],["huiliuxian（NF）","xuanshijueyuanzi"],["huiliuxian（NF）","xuanshijueyuanzijinju"],["huiliuxian（NF）","zhichijueyuanzigaiban"],["huiliuxian（NF）","chuzuoanzi"],["huiliuxian（NF）","shuangeranzi"],["huiliuxian（NF）","zhizuo"],["huiliuxian（NF）","zhudinggaiban"],["huiliuxian（NF）","zhudingdizuo"],["fangleixian（GW）","fujiaxian"],["fangleixian（GW）","zhengkuixianyujiaoshinaizhangjiexutiao"],["fangleixian（GW）","xiamaodizuo"],["fangleixian（GW）","chuhuangan"],["fangleixian（GW）","yujiaoshinaizhangxianjia"],["fangleixian（GW）","naizhangxianjia"],["fangleixian（GW）","duimaoxian"],["fangleixian（GW）","binggouxianjia"],["fangleixian（GW）","jianjia"],["fangleixian（GW）","jianjiadizuo"],["fangleixian（GW）","xuanchuixianjia"],["fangleixian（GW）","qiutouguahuan"],["fangleixian（GW）","xuanshijueyuanzi"],["fangleixian（GW）","xuanshijueyuanzijinju"],["fangleixian（GW）","zhichijueyuanzigaiban"],["fangleixian（GW）","chuzuoanzi"],["fangleixian（GW）","shuangeranzi"],["fangleixian（GW）","zhizuo"],["fangleixian（GW）","zhudinggaiban"],["fangleixian（GW）","zhudingdizuo"],["baohuxian（PW）","fujiaxian"],["baohuxian（PW）","zhengkuixianyujiaoshinaizhangjiexutiao"],["baohuxian（PW）","xiamaodizuo"],["baohuxian（PW）","chuhuangan"],["baohuxian（PW）","yujiaoshinaizhangxianjia"],["baohuxian（PW）","naizhangxianjia"],["baohuxian（PW）","duimaoxian"],["baohuxian（PW）","binggouxianjia"],["baohuxian（PW）","jianjia"],["baohuxian（PW）","jianjiadizuo"],["baohuxian（PW）","xuanchuixianjia"],["baohuxian（PW）","qiutouguahuan"],["baohuxian（PW）","xuanshijueyuanzi"],["baohuxian（PW）","xuanshijueyuanzijinju"],["baohuxian（PW）","zhichijueyuanzigaiban"],["baohuxian（PW）","chuzuoanzi"],["baohuxian（PW）","shuangeranzi"],["baohuxian（PW）","zhizuo"],["baohuxian（PW）","zhudinggaiban"],["baohuxian（PW）","zhudingdizuo"],["zhizhu","zhizhu"],["laxian","shuangerxiexingxianjia"],["suidaobi","suidaobi"],["diaozhu","diaozhudizuo"],["diaozhu","dingweizhichengdiaozhu"],["diaozhu","fujiaxuanguadiaozhu"],["27.5Kvdianlan","shebeiyinxian"],["27.5Kvdianlan","shebeiyinxianxianjia（yajieshi）"],["27.5Kvdianlan","shebeiyinxianduimaolianjiebujian"],["27.5Kvdianlan","binggouxianjia"],["27.5Kvdianlan","gaoyadianlanzhongduantoutuojia"],["27.5Kvdianlan","gaoyadianlangudingjia"],["27.5Kvdianlan","gaoyadianlan"],["27.5Kvdianlan","mupai"],["gelikaiguan","shebeiyinxian"],["gelikaiguan","shebeiyinxianxianjia（yajieshi）"],["gelikaiguan","shebeiyinxianduimaolianjiebujian"],["gelikaiguan","binggouxianjia"],["gelikaiguan","gelikaiguan"],["gelikaiguan","gelikaiguancaozuogan"],["bileiqi","shebeiyinxian"],["bileiqi","shebeiyinxianxianjia（yajieshi）"],["bileiqi","shebeiyinxianduimaolianjiebujian"],["bileiqi","binggouxianjia"],["bileiqi","bileiqi"],["bileiqi","jishuqi"],["bileiqi","jishuqilianjiexian"],["27.5Kvdianlanzhongduantou","gaoyadianlan"],["27.5Kvdianlanzhongduantou","mupai"],["xishangxian","xishangxian"],["jiedixian","jiedixian"],["ganhaopai","ganhaopai"],["gudingbiaozhi","biaozhipai"],["xuanguabiaozhi","biaozhipai"],["gaoyaweixianbiao","biaozhipai"]]
        structure_value_json = json.dumps(structure_value)
        parts = ["接地跳线针","固定绳等电位线","斜吊线","计数器连接线","调节立柱","设备引线线夹（压接式）","高压电缆终端头托架","线岔","悬吊底座","调节螺栓","固定绳等电位线线夹","定位器定位环","设备引线对锚连接部件","隔离开关","避雷器","母排","承力索接头线夹","接地跳线肩架","支持器定位器","悬吊滑轮","隔离开关操作杆","高压电缆固定架","高压电缆","标识牌","接地跳线","硬横梁","固定绳角钢","杵座楔形线夹","分段绝缘器","计数器","大限界框架","接地线","等电位线线夹","支持器","固定绳","定位环线夹","接线端子","弹簧补偿器","正馈线预绞式耐张接续条","设备引线","吸上线","接触线接头线夹","等电位线","定位夹环"]
        parts_json = json.dumps(parts, ensure_ascii=False)
        filters = {
                    "components": [{"id":"chenglisuo","name":"承力索"},{"id":"jiechuxian","name":"接触线"},{"id":"zhengtidiaoxian（rouxing）","name":"整体吊弦（柔性）"},{"id":"dingweiguandiaoxian","name":"定位管吊线"},{"id":"jiechuxianzhongxinmaojie","name":"接触线中心锚结"},{"id":"gudingshengxielaxian","name":"固定绳斜拉线"},{"id":"zhengtidiaoxian（gangxing）","name":"整体吊弦（刚性）"},{"id":"chenglisuozhongxinmaojie","name":"承力索中心锚结"},{"id":"dianlianjie","name":"电连接"},{"id":"dianlianjiexianjia","name":"电连接线夹"},{"id":"xiancha","name":"线岔"},{"id":"fenduanjueyuanqi","name":"分段绝缘器"},{"id":"jueyuanzi","name":"绝缘子"},{"id":"luomaozhuangzhi","name":"落锚装置"},{"id":"dengdianweixian","name":"等电位线"},{"id":"tanxingdiaosuo","name":"弹性吊索"},{"id":"wanbi","name":"腕臂"},{"id":"pingwanbi-dizuo","name":"平腕臂-底座"},{"id":"xiewanbi-dizuo","name":"斜腕臂-底座"},{"id":"jueyuanzijinju","name":"绝缘子金具"},{"id":"jueyuanzifangtuojian","name":"绝缘子防脱件"},{"id":"ruansuoshiyinghengkua(liang）","name":"软索式硬横跨(梁）"},{"id":"zhenshijueyuanzi","name":"针式绝缘子"},{"id":"wanbi-L","name":"腕臂-L"},{"id":"wanbizhicheng-L","name":"腕臂支撑-L"},{"id":"dingweizhuangzhi-L","name":"定位装置-L"},{"id":"dingweizhuangzhi-G","name":"定位装置-G"},{"id":"lvhejindingweihuan","name":"铝合金定位环"},{"id":"ruansuoshiyinghengkua（liang）","name":"软索式硬横跨（梁）"},{"id":"wanbizhicheng-G","name":"腕臂支撑-G"},{"id":"wanbi-G","name":"腕臂-G"},{"id":"quniaozhuangzhi","name":"驱鸟装置"},{"id":"zhengkuixian（AF）","name":"正馈线（AF）"},{"id":"gongdianxian","name":"供电线"},{"id":"huiliuxian（NF）","name":"回流线（NF）"},{"id":"fangleixian（GW）","name":"防雷线（GW）"},{"id":"baohuxian（PW）","name":"保护线（PW）"},{"id":"zhizhu","name":"支柱"},{"id":"laxian","name":"拉线"},{"id":"suidaobi","name":"隧道壁"},{"id":"diaozhu","name":"吊柱"},{"id":"27.5Kvdianlan","name":"27.5Kv电缆"},{"id":"gelikaiguan","name":"隔离开关"},{"id":"bileiqi","name":"避雷器"},{"id":"27.5Kvdianlanzhongduantou","name":"27.5Kv电缆终端头"},{"id":"xishangxian","name":"吸上线"},{"id":"jiedixian","name":"接地线"},{"id":"ganhaopai","name":"杆号牌"},{"id":"gudingbiaozhi","name":"固定标识"},{"id":"xuanguabiaozhi","name":"悬挂标识"},{"id":"gaoyaweixianbiao","name":"高压危险标"}],
                    "structure_value": structure_value_json,
                    "defects": [{"name":"线索损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"线-线互磨","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"线-管互磨","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"距离不足","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"异物","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"开口销缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"开口销未掰","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"开口销掰开不足120度","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"裂纹","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"预绞丝非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"预绞丝损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"滑移","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"承力索终端锚固线夹变形","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"线夹留头外漏不足或过长","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"磨损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"螺母缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"螺母松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"未入槽","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"螺栓松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"接触线扭面","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"变形","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"U型插销缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"U型插销插入不足","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"锁片缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"锁片未锁死","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"U型环缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"线夹未入槽","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"线夹烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"偏斜","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"锁片折断","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"锁片非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"吊弦损伤或异物","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"吊弦断裂或不受力","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"吊弦硬弯","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"吊弦缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"压接端子缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"载流环断股","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"载流环散股","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"吊弦载流环方向反","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"载流环折断","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"钳压管非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"钳压管破损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"心形环损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"心形环缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"压接端子裂纹","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"压接端子非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"压接端子偏扭","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"中心锚结绳松弛","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"钳压管损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"日式吊弦折断","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"日式吊弦损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"螺栓缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"中心锚结线夹缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"线夹非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"锈蚀","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"树枝异物","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"电连接非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"电连接松弛","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"电连接紧","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"电连接断裂","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"电连接断股","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"电连接损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"电连接扭绞","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"U型插销折断","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"电连接线夹损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"弯曲","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"卡滞","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"接头线夹未入槽","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"接头线夹抽动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"接头线夹裂纹","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"接头线夹其他","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"并沟线夹未入槽","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"垫片缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"并沟线夹裂纹","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"并沟线夹其他","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"吊弦支撑裂纹","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"吊弦支撑缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"吊弦支撑折断","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"花篮螺丝心形环偏斜","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"花篮螺丝心形环脱出","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"花篮螺丝心形环变形","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"花篮螺丝心形环缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"调节吊弦松","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"调节吊弦偏斜","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"绝缘滑道裂纹","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"绝缘滑道异常磨耗","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"绝缘滑道烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"绝缘滑道连接松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"金属滑道裂纹","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"金属滑道异常磨耗","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"金属滑道烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"金属滑道连接松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"消弧棒折断","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"消弧棒缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"消弧棒裂纹","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"消弧棒撞击伤害","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"分段绝缘器驰度偏差","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"绝缘子破损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"绝缘子裂纹","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"绝缘子脏污","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"绝缘子闪络","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"M销缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"M销松脱","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"弛度松","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"弛度紧","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"铁模压板非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"铁模压板缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"副螺母缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"副螺母松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"补偿绳扭绞","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"补偿绳非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"回头卡环缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"a值小","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"a值大","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"b值小","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"b值大","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"L值小","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"L值大","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"坠砣非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"坠砣抱箍卡滞","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"坠砣抱箍松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"坠砣限制架变形","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"坠砣限制架弯曲","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"坠砣限制架管抽出","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"平衡轮偏斜","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"平衡轮损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"平衡轮卡滞","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"开口销损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"棘轮偏斜","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"棘轮损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"棘轮卡滞","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"制动卡块缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"制动卡块松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"制动卡块卡滞","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"棘轮驱鸟装置松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"棘轮驱鸟罩破损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"补偿轮损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"补偿轮偏斜","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"补偿轮卡滞","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"杵环杆弯曲","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"落锚角钢下滑","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"落锚角钢松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"顶紧螺栓缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"落锚角钢顶紧螺栓松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"零件偏斜","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"开口销非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"散股","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"腕臂偏移","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"腕臂和定位装置不同垂面","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"不水平","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"管弯曲","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"断股","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"脱落","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"绑扎不规范","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"安装不水平","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"安装松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"线夹松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"鸟巢异物","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"垫圈磨损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"螺栓磨损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"绝缘子金具烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"针式绝缘子非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"套管单耳损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"套管单耳非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"U螺栓松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"套管单耳破损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"套管座破损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"顶紧螺栓松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"顶紧螺栓薄螺母松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"套管座非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"承力索座破损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"承力索座非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"套筒双耳破损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"套筒双耳非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"销钉缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"顶紧螺栓非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"支撑管脱出","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"吊线固定钩折断","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"定位管吊线损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"定位管吊线松弛","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"U型环扭转","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"定位支座非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"定位支座损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"定位支座磨损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"电气连接跳线缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"日式定位支座磨损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"电气连接跳线损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"电气连接跳线断股","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"电气连接跳线非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"电气连接跳线脱落","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"端子扭转","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"定位器不受力","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"定位器弯曲","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"铆钉缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"铆钉松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"定位器烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"铜柱磨损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"定位器线夹烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"U型销非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"U型销缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"定位器线夹U型销折断","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"U型销损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"U型销不密贴","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"锚支定位卡子受力面反","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"衬垫缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"衬垫非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"销钉非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"管帽缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"管帽松脱","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"顶紧螺栓薄螺母缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"防风拉线缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"防风拉线断裂","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"防风拉线松弛","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"防风拉线损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"防风拉线非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"管帽破损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"卡子损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"卡子偏斜","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"卡子非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"螺栓非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"定位环损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"垫片非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"挠度偏差","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"不规范","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"双耳楔形线夹回头受力面反","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"双耳楔形线夹非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"受力面反","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"M销脱出","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"未受拉力","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"断股≥3股","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"损伤≥3股","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"断股＜3股","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"损伤＜3股","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"腐蚀","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"交叉处所","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"异常硬弯","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"异物（＜0.3㎡）","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"规格错误","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"不受力","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"回头外漏不够","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"安装不规范","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"折断","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"型号错误","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"托槽","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"受力面错误","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"垫片安装不规范","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"环裂纹","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"套管双耳非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"压线夹板松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"压线夹板缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"承力索座鞍形支座烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"承力索座副线缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"驱鸟罩损坏","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"线线交叉","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"不密贴","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"对锚线跨度驰度偏差","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"对锚线非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"球头挂环烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"支持绝缘子盖板非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"双耳鞍子非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"支座螺栓松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"支柱偏扭","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"支柱弯曲","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"坠物","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"隧道滴水","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"隧道结冰","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"隧道异物","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"有接头","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"扭绞","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"压接缺陷","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"U型插销端头外漏不足","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"U型插销端头外漏过长","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"电气烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"固定架抱箍损伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"破损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"无保护措施","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"上部转动杆连接弯曲","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"上部转动杆连接折断","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"上部转动杆连接裂纹","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"静触头锈蚀","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"静触头烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"静触头异常磨损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"静触头电气腐蚀","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"动触头触头锈蚀","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"动触头烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"动触头异常磨损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"动触头卡滞","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"动触头电气腐蚀","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"动触头弹簧调节螺栓卡簧松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"动触头弹簧调节螺栓卡簧缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"设备线夹烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"设备线夹引线抽出","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"设备线夹引线非标安装","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"脱离器折断","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"脱离器破损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"脱离器松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"脱离器缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"避雷器破损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"避雷器闪络","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"避雷器脏污","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"避雷器金具锈蚀","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"避雷器金具电气烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"避雷器老化","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"避雷器偏斜","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"计数器锈蚀","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"计数器破损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"计数器异常","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"计数器连接线破损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"计数器连接线磨损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"计数器连接线折断","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"计数器连接线脱落","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"计数器连接线连接松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"闪络","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"脏污","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"金具锈蚀","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"金具电气烧伤","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"老化","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"与母排连接断开","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"母排受拉力","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"连接松动","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"抽脱","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"杆号牌破损","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"杆号牌缺失","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"无法辨识","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"连接线锈蚀","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]},{"name":"连接线折断","prob":0.98,"prob1":1,"checked":True,"range":[0.98,1]}],
                    "name": filter_name,
                    "comment": "",
                    "filter_type": filter_type,
                    "parts": parts_json
                }
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("AddFilter", filter=filters)
    handleGrpcRes = HandleGrpcRes(res)
    msg = handleGrpcRes.get_data_item("msg")
    assert msg=="success"


def list_filter(login, filter_type, pcount, pno, fname=None):
    """
    :param filter_type 0.缺陷审核任务 1.零部件专项审核任务
    :return:
    """
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("ListFilter", fname=fname, pcount=pcount, pno=pno, filter_type=filter_type)
    handleGrpcRes = HandleGrpcRes(res)
    filters = handleGrpcRes.get_data_item("data")["filters"]
    return filters


def smart_review_compute(login, analysis_id, filter_id, task_type, works, ratio=0, rule=4):
    """
    智能分配【计算】
    :param login:
    :param analysis_id:
    :param filter_id: 审核任务类型id
    :param task_type: 审核任务类型 0缺陷审核任务 1零部件审核任务
    :param works: [{"id":1,"checker":3,"reviewer":4,"percentage":100,"image_num":0}]
    # works,一个{}代表一个子任务，id从1开始，checker、reviewer=user_id , percentage-百分比，image_num=0
    :param ratio: 互检比例, 百分比：0 <= ratio <= 100
    :param rule: 审核任务分配规则: 1-按公里标 2-按支柱号 3-按站区 4-智能分配
    :return: smart_review_data
    """
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("AddSmartReviewCompute", analysis_id=analysis_id, filter_id=filter_id, rule=rule, ratio=ratio,
                     filter_hash="", task_type=task_type, works=works)
    handleGrpcRes = HandleGrpcRes(res)
    code = handleGrpcRes.get_data_item("code")
    if code in (70007, 70001):
        logging.info(f"analysis_id:{analysis_id},filter_id:{filter_id},任务已存在或此类型下无缺陷")
        return None
    elif code == 0:
        data = handleGrpcRes.get_data_item("data")
        works = data["works"]
        filter_hash = data["filter_hash"]
        analysis_id = data["analysis_id"]
        filter_id = data["filter_id"]
        return works, filter_hash, analysis_id, filter_id
    else:
        logging.error(
            f"analysis_id:{analysis_id},filter_id:{filter_id}智能分配【计算】失败，msg：{handleGrpcRes.get_data_item('msg')}，data：{handleGrpcRes.get_data_item('data')}")
        return None


def smart_review_confirm(login, analysis_id, filter_id, task_type, works, ratio=0, rule=4):
    """
    智能分配【提交】
    :param ：请求参数是 智能分配【计算】的接口返回
    :return:
    """
    client = GrpcClient(host, proto_file_path, login)
    res = client.run("AddSmartReviewConfirm", analysis_id=analysis_id, filter_id=filter_id, rule=rule, ratio=ratio,
                     filter_hash="", task_type=task_type, works=works)
    handleGrpcRes = HandleGrpcRes(res)
    data = handleGrpcRes.get_data_item("msg")
    assert data == 'success'
