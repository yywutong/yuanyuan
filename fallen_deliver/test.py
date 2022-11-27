#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2021-04-28 21:09:00
LastEditors: zhoushuke
LastEditTime: 2022-02-08 11:15:36
FilePath: /fallen_deliver/test.py
'''

# from utils.app_check_in_backend import AppCheckInBackend
# from utils.sqlalchemy_db import update_apps_list_by_fallen_subform
# from fallendeliver.git_sync import git_sync_to_apps_standard  # git_sync_to_spring_deploy
# from fallendeliver.deliver import deliver
from fallendeliver.update import update
# from fallendeliver.git_sync import git_sync_c4_app_to_apps_standard, git_sync_from_apps_standard_c4_standard
# from utils.func_ops import transfer_from_emails_to_mobiles

if __name__ == "__main__":
    pass

    # checker = AppCheckInBackend(d["tpls"]["form_data"][0],
    #                             d["tpls"]["form_structure"][0])
    # checker("QATesting")

    # data = "{\"id\":266,\"title\":\"更新op-service\",\"priority\":3,\"form_data\":[{\"divider_1614176282000_71093\":\"分割线\",\"input_order_creator_email_id\":\"zhoushuke@sensetime.com\",\"input_other_senders_emails_id\":\"\",\"input_product_version_id\":\"v3.2\",\"input_wotype_id\":\"提测单\",\"radio_1613639231000_48190\":\"是\",\"radio_1613639268000_11141\":\"否\",\"radio_1614176251000_48132\":\"是\",\"radio_1614314860000_75631\":\"否\",\"select_deploy_cluster_id\":[\"test\"],\"subform_version_info_id\":[{\"input_deploy_app_id\":\"resource-manager-backend\",\"input_deploy_release_version_id\":\"3c68e21b\"}],\"text_1618901008000_76230\":\"开发在提测时提测环境只能选择【test】\",\"text_1618901016000_73105\":\"产品线定义版本\",\"textarea_1613635281000_24319\":\"修复vid为空的问题\",\"textarea_1614176349000_52899\":\"更新 配置文件  op-procession版本为 0.1.18\"}]}"
    # precheck(data)
    # data = "{\"id\":895,\"title\":\"修改盒子调度方式@龙贤兵\",\"priority\":1,\"form_data\":[{\"date_1618901410000_45646\":\"\",\"divider_1614176282000_71093\":\"分割线\",\"input_1614314798000_68210\":\"\",\"input_1614314818000_16911\":\"\",\"input_order_creator_email_id\":\"longxianbing_vendor@sensetime.com\",\"input_other_senders_emails_id\":\"\",\"input_product_version_id\":\"v3.4\",\"input_sep_address\":\"https://sep.sensetime.com/\",\"input_wotype_id\":\"提测单\",\"radio_1613639231000_48190\":\"是\",\"radio_1613639268000_11141\":\"否\",\"radio_1614176251000_48132\":\"否\",\"radio_1614314860000_75631\":\"否\",\"select_deploy_cluster_id\":[\"test\"],\"subform_version_info_id\":[{\"file_1618901245000_38047\":[],\"input_deploy_app_id\":\"op-service\",\"input_deploy_release_version_id\":\"853774ff\",\"input_deploy_version_id\":\"853774ff\"}],\"text_1618901008000_76230\":\"开发在提测时环境只能选择【test】否则工单将自动关闭\",\"text_1618901016000_73105\":\"产品线定义版本\",\"text_1624540674000_38632\":\"应用名称列表由统一发布平台维护，新上应用需要由OP事先导入到发布平台中\",\"text_1624540678000_71596\":\" 由QA确认该次提测最终的验收版本，开发在提测时请保持与提测版本相同即可\",\"textarea_1613635281000_24319\":\"贤兵忘记提单了，补一个提测单，修改盒子调度方式，3s已经测试通过。\",\"textarea_1614176349000_52899\":\"\",\"textarea_remark_id\":\"\"}]}"
    # git_sync_to_apps_standard(data, "spring")
    # git_sync_to_spring_deploy(data)

    # data = "{\"id\":945,\"title\":\"工业训练平台-四期功能提测\",\"priority\":1,\"form_data\":[{\"date_1618901410000_45646\":\"\",\"divider_1614176282000_71093\":\"分割线\",\"input_1614314798000_68210\":\"\",\"input_1614314818000_16911\":\"\",\"input_order_creator_email_id\":\"wudean.vendor@sensetime.com\",\"input_other_senders_emails_id\":\"\",\"input_product_version_id\":\"3.4.2\",\"input_sep_address\":\"https://sepd.sensetime.com/\",\"input_wotype_id\":\"提测单\",\"radio_1613639231000_48190\":\"是\",\"radio_1613639268000_11141\":\"否\",\"radio_1614176251000_48132\":\"否\",\"radio_1614314860000_75631\":\"是\",\"select_deploy_cluster_id\":[\"test\"],\"subform_version_info_id\":[{\"file_1618901245000_38047\":[],\"input_deploy_app_id\":\"panorama-v2-industry-frontend\",\"input_deploy_release_version_id\":\"247dbe2e\",\"input_deploy_version_id\":\"ea3959c0\"},{\"file_1618901245000_38047\":[],\"input_deploy_app_id\":\"evaluate-frontend\",\"input_deploy_release_version_id\":\"c562a93d\",\"input_deploy_version_id\":\"c562a93d\"},{\"file_1618901245000_38047\":[],\"input_deploy_app_id\":\"panorama-v2-frontend\",\"input_deploy_release_version_id\":\"33b0f544\",\"input_deploy_version_id\":\"33b0f544\"},{\"file_1618901245000_38047\":[],\"input_deploy_app_id\":\"sensebee-lite-frontend\",\"input_deploy_release_version_id\":\"f9f59522\",\"input_deploy_version_id\":\"f9f59522\"},{\"file_1618901245000_38047\":[],\"input_deploy_app_id\":\"sensebee-lite-backend\",\"input_deploy_release_version_id\":\"0f3e5967\",\"input_deploy_version_id\":\"0f3e5967\"},{\"file_1618901245000_38047\":[],\"input_deploy_app_id\":\"panorama-v2-backend\",\"input_deploy_release_version_id\":\"0ffbc9ca\",\"input_deploy_version_id\":\"0ffbc9ca\"},{\"file_1618901245000_38047\":[],\"input_deploy_app_id\":\"uums-backend\",\"input_deploy_release_version_id\":\"09e34bff\",\"input_deploy_version_id\":\"09e34bff\"}],\"text_1618901008000_76230\":\"开发在提测时环境只能选择【test】否则工单将自动关闭\",\"text_1618901016000_73105\":\"产品线定义版本\",\"text_1624540674000_38632\":\"应用名称列表由统一发布平台维护，新上应用需要由OP事先导入到发布平台中\",\"text_1624540678000_71596\":\" 由QA确认该次提测最终的验收版本，开发在提测时请保持与提测版本相同即可\",\"textarea_1613635281000_24319\":\"本次工业训练四期全部功能提测\\n本次四期PRD文档：https://confluence.sensetime.com/pages/viewpage.action?pageId=349306882\",\"textarea_1614176349000_52899\":\"sensebee-lite-backend 模块需要更新sql\\nhttps://gitlab.bj.sensetime.com/spring-ee/sense-spring-3.x/product/sensebee/sensebee-lite-backend/-/tree/spring_industry_4/deploy/files/sqls\\n\",\"textarea_remark_id\":\"\"}]}"
    data = "{\"id\":1060,\"title\":\" C4-缺陷数量曲线统计和审核工作量统计调整\",\"priority\":1,\"form_data\":[{\"input_order_creator_email_id\":\"zhoushuke@sensetime.com\",\"input_other_senders_emails_id\":\"\",\"input_product_version_id\":\"v2.0.9\",\"input_wotype_id\":\"修复单\",\"radio_1613639300000_48237\":\"否\",\"radio_1614176251000_48132\":\"否\",\"radio_1614516809000_72198\":\"是\",\"radio_1626063672000_8275\":\"是\",\"select_deploy_cluster_id\":[\"test\"],\"subform_version_info_id\":[{\"input_deploy_app_id\":\"industry-platform\",\"input_deploy_release_version_id\":\"f6d3ab47\"}],\"textarea_1613635281000_24319\":\"C4-缺陷数量曲线统计和审核工作量统计调整\",\"textarea_1614176349000_52899\":\"\"}]}"
    update(data)

    # data = "{\"id\":282,\"title\":\"C4产品2.0.3版本安全合规修改-3-修复\",\"priority\":1,\"form_data\":[{\"input_git_addr_id\":\"https://gitlab.bj.sensetime.com/spring-ee/sense-spring-3.x/devops/deploy/c4-standard\",\"input_order_creator_email_id\":\"zhoushuke@sensetime.com\",\"input_product_version_id\":\"v2.0.3\",\"input_project_gitname_id\":\"c4-standard\",\"input_wotype_id\":\"修复单\",\"radio_1613639300000_48237\":\"否\",\"radio_1614176251000_48132\":\"否\",\"radio_1614516809000_72198\":\"是\",\"select_deploy_cluster_id\":[\"test\"],\"subform_version_info_id\":[{\"input_deploy_app_id\":\"platform\",\"input_deploy_branch_id\":\"f_anquan630\",\"input_deploy_release_version_id\":\"v2.0.3-84-2\"},{\"input_deploy_app_id\":\"frontend\",\"input_deploy_branch_id\":\"f_anquan630-2\",\"input_deploy_release_version_id\":\"v2.0.3-84\"}],\"textarea_1613635281000_24319\":\"修复用户编辑时提示邮箱已存在的问题\",\"textarea_1614176349000_52899\":\"\"}]}"
    # update(data)

    # data = "{\"id\":408,\"title\":\"高铁C4 模型升级v1.5.0\",\"priority\":1,\"form_data\":[{\"date_1626063298000_68143\":\"2021-07-16\",\"divider_1614176282000_71093\":\"分割线\",\"input_1614314798000_68210\":\"liurenhui\",\"input_1614314818000_16911\":\"暴天鹏\",\"input_order_creator_email_id\":\"zhoushuke@sensetime.com\",\"input_other_senders_emails_id\":\"zhoushuke@sensetime.com\",\"input_product_version_id\":\"2.0.5\",\"input_sep_address\":\"https://sepd.sensetime.com/#/require/requireManage\",\"input_wotype_id\":\"提测单\",\"radio_1613639231000_48190\":\"是\",\"radio_1613639268000_11141\":\"否\",\"radio_1614176251000_48132\":\"否\",\"radio_1614314860000_75631\":\"否\",\"select_deploy_cluster_id\":[\"test\"],\"subform_version_info_id\":[{\"file_1626063260000_73703\":[],\"input_deploy_app_id\":\"platform\",\"input_deploy_release_version_id\":\"model_v1.5.0-01\",\"input_deploy_version_id\":\"model_v1.5.0-01\"},{\"file_1626063260000_73703\":[],\"input_deploy_app_id\":\"async\",\"input_deploy_release_version_id\":\"model-v1.5.0\",\"input_deploy_version_id\":\"model-v1.5.0\"},{\"file_1626063260000_73703\":[],\"input_deploy_app_id\":\"crontab\",\"input_deploy_release_version_id\":\"model_v1.5.0-01\",\"input_deploy_version_id\":\"model_v1.5.0-01\"},{\"file_1626063260000_73703\":[],\"input_deploy_app_id\":\"crh\",\"input_deploy_release_version_id\":\"v2.0.1-c4-v1.5.0-b43c1c3-cuda10-nolic\",\"input_deploy_version_id\":\"v2.0.1-c4-v1.5.0-b43c1c3-cuda10-nolic\"}],\"text_1614515214000_50854\":\" 由QA确认该次提测最终的验收版本开发在提测时请保持与提测版本相同即可\",\"textarea_1613635281000_24319\":\"1、算法升级 sdk 版本1.4.0          模型版本1.5.0，新增14个缺陷项点\\n2、数据回流bugfix\\n3、差异库导出excel问题修复\\n\",\"textarea_1614176349000_52899\":\"\",\"textarea_remark_id\":\"\"}]}"
    # c4_precheck(data)

    # data = "{\"id\":427,\"title\":\"fix_2918_2920\",\"priority\":1,\"form_data\":[{\"input_order_creator_email_id\":\"zhoushuke@sensetime.com\",\"input_other_senders_emails_id\":\"\",\"input_product_version_id\":\"v2.0.5\",\"input_wotype_id\":\"修复单\",\"radio_1613639300000_48237\":\"否\",\"radio_1614176251000_48132\":\"否\",\"radio_1614516809000_72198\":\"是\",\"radio_1626063672000_8275\":\"是\",\"select_deploy_cluster_id\":[\"dev\", \"test\"],\"subform_version_info_id\":[{\"input_deploy_app_id\":\"industry-image-server\",\"input_deploy_release_version_id\":\"554f0a51\"},{\"input_deploy_app_id\":\"industry-frontend\",\"input_deploy_release_version_id\":\"ad019629\"}],\"textarea_1613635281000_24319\":\"fix_2918_2920\",\"textarea_1614176349000_52899\":\"\"}]}"
    # deliver(data)
    # git_sync_c4_app_to_apps_standard(data)
    # git_sync_from_apps_standard_c4_standard(data)
    # transfer_from_emails_to_mobiles([
    #     'liurenhui@sensetime.com', 'devops.sensespring@sensetime.com',
    #     'qa.sensespring@sensetime.com'
    # ])
