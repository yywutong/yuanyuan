#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2022-02-01 17:53:43
LastEditors: zhoushuke
LastEditTime: 2022-02-02 23:35:55
FilePath: /fallen_deliver/fallendeliver/checker.py
'''

import json
from utils.app_check_in_backend import AppCheckInBackend

# example case.
""""
d = {
    "title":
    "远端数据测试",
    "priority":
    1,
    "process":
    25,
    "classify":
    6,
    "state": [{
        "id": "userTask1613719298299",
        "process_method": "role",
        "processor": [9],
        "label": "QA审批"
    }],
    "source":
    "start1613719113921",
    "source_state":
    "提交",
    "process_method":
    "",
    "tpls": {
        "form_structure": [{
            "list": [{
                "key":
                "1613634917000_53174",
                "icon":
                "icon-grid-",
                "name":
                "栅格布局",
                "type":
                "grid",
                "model":
                "grid_1613634917000_53174",
                "rules": [],
                "columns": [{
                    "list": [{
                        "key":
                        "1619490097000_63289",
                        "icon":
                        "icon-select",
                        "name":
                        "工单类型",
                        "type":
                        "select",
                        "model":
                        "input_wotype_id",
                        "rules": [{
                            "message": "工单类型必须填写",
                            "required": True
                        }],
                        "options": {
                            "props": {
                                "label": "label",
                                "value": "value"
                            },
                            "width":
                            "",
                            "remote":
                            False,
                            "options": [{
                                "value": "修复单"
                            }, {
                                "value": "提测单"
                            }, {
                                "value": "变更单"
                            }],
                            "disabled":
                            True,
                            "multiple":
                            False,
                            "required":
                            True,
                            "clearable":
                            False,
                            "showLabel":
                            False,
                            "filterable":
                            True,
                            "labelWidth":
                            100,
                            "remoteFunc":
                            "func_1619490097000_63289",
                            "placeholder":
                            "",
                            "defaultValue":
                            "修复单",
                            "remoteOptions": [],
                            "labelWidthStatus":
                            True,
                            "labelWidthDisabled":
                            False
                        }
                    }],
                    "span":
                    12
                }, {
                    "list": [{
                        "key":
                        "1619490039000_44506",
                        "icon":
                        "icon-input",
                        "name":
                        "产品版本",
                        "type":
                        "input",
                        "model":
                        "input_product_version_id",
                        "rules": [{
                            "type": "string",
                            "message": "产品版本格式不正确"
                        }, {
                            "message": "产品版本必须填写",
                            "required": True
                        }],
                        "options": {
                            "width": "100%",
                            "pattern": "",
                            "dataType": "string",
                            "disabled": False,
                            "required": True,
                            "labelWidth": 100,
                            "remoteFunc": "func_1619490039000_44506",
                            "placeholder": "产品线大版本",
                            "defaultValue": "",
                            "showPassword": False,
                            "labelWidthStatus": True,
                            "labelWidthDisabled": False
                        }
                    }],
                    "span":
                    12
                }, {
                    "list": [{
                        "key": "1642655261000_97559",
                        "icon": "icon-select",
                        "name": "下拉选择框",
                        "type": "select",
                        "model": "select_1642655261000_97559",
                        "rules": [],
                        "options": {
                            "props": {
                                "label": "name",
                                "value": "name"
                            },
                            "width":
                            "",
                            "remote":
                            True,
                            "options": [],
                            "disabled":
                            False,
                            "multiple":
                            False,
                            "required":
                            False,
                            "clearable":
                            False,
                            "showLabel":
                            False,
                            "filterable":
                            False,
                            "labelWidth":
                            100,
                            "remoteFunc":
                            "FallenGetC4AppNotQATesting",
                            "placeholder":
                            "",
                            "defaultValue":
                            "",
                            "remoteOptions": [{
                                "label":
                                "engine-industry-image-process-service",
                                "value":
                                "engine-industry-image-process-service"
                            }, {
                                "label": "industry-image-server",
                                "value": "industry-image-server"
                            }],
                            "labelWidthStatus":
                            True,
                            "labelWidthDisabled":
                            False
                        }
                    }],
                    "span":
                    12
                }],
                "options": {
                    "align": "top",
                    "gutter": 0,
                    "justify": "start",
                    "remoteFunc": "func_1613634917000_53174"
                }
            }, {
                "key":
                "1618900999000_20188",
                "icon":
                "icon-grid-",
                "name":
                "栅格布局",
                "type":
                "grid",
                "model":
                "grid_1618900999000_20188",
                "rules": [],
                "columns": [{
                    "list": [{
                        "key": "1618901016000_73105",
                        "icon": "icon-wenzishezhi-",
                        "name": "产品版本",
                        "type": "text",
                        "model": "text_1618901016000_73105",
                        "rules": [],
                        "options": {
                            "font_size": "15px",
                            "font_color": "#FF0000",
                            "labelWidth": 100,
                            "remoteFunc": "func_1618901016000_73105",
                            "customClass": "",
                            "font_family": "",
                            "font_weight": "500",
                            "defaultValue": "产品线定义版本",
                            "labelWidthStatus": True,
                            "labelWidthDisabled": False
                        }
                    }],
                    "span":
                    12
                }, {
                    "list": [{
                        "key": "1618901013000_16452",
                        "icon": "icon-wenzishezhi-",
                        "name": "环境",
                        "type": "text",
                        "model": "text_1618901008000_76230",
                        "rules": [],
                        "options": {
                            "font_size": "15px",
                            "font_color": "#FF0000",
                            "labelWidth": 80,
                            "remoteFunc": "func_1618901008000_76230",
                            "customClass": "",
                            "font_family": "",
                            "font_weight": "500",
                            "defaultValue": "开发在上线时环境只能选择【test】否则工单将自动关闭",
                            "labelWidthStatus": True,
                            "labelWidthDisabled": True
                        }
                    }],
                    "span":
                    12
                }],
                "options": {
                    "align": "top",
                    "gutter": 0,
                    "justify": "start",
                    "remoteFunc": "func_1618900999000_20188"
                }
            }, {
                "key":
                "1616053356000_7895",
                "icon":
                "icon-table",
                "name":
                "版本信息",
                "type":
                "subform",
                "model":
                "subform_version_info_id",
                "rules": [],
                "columns": [{
                    "list": [{
                        "key":
                        "1624540888000_65317",
                        "icon":
                        "icon-select",
                        "name":
                        "应用名称",
                        "type":
                        "select",
                        "model":
                        "input_deploy_app_id",
                        "rules": [{
                            "message": "应用名称必须填写",
                            "required": True
                        }],
                        "options": {
                            "props": {
                                "label": "name",
                                "value": "id"
                            },
                            "width":
                            "100%",
                            "remote":
                            False,
                            "options": [{
                                "value": "argo-engine-xxx"
                            }, {
                                "value": "op-service-xxx"
                            }],
                            "disabled":
                            False,
                            "multiple":
                            False,
                            "required":
                            True,
                            "clearable":
                            False,
                            "showLabel":
                            False,
                            "filterable":
                            False,
                            "labelWidth":
                            100,
                            "remoteFunc":
                            "FallenGetSpringAppNotQATesting",
                            "placeholder":
                            "",
                            "defaultValue":
                            "",
                            "remoteOptions": [{
                                "label": "argo-engine",
                                "value": "argo-engine"
                            }, {
                                "label": "op-service",
                                "value": "op-service"
                            }],
                            "labelWidthStatus":
                            True,
                            "labelWidthDisabled":
                            False
                        }
                    }],
                    "span":
                    12
                }, {
                    "list": [{
                        "key":
                        "1616053523000_8325",
                        "icon":
                        "icon-input",
                        "name":
                        "应用版本",
                        "type":
                        "input",
                        "model":
                        "input_deploy_release_version_id",
                        "rules": [{
                            "type": "string",
                            "message": "应用版本格式不正确"
                        }, {
                            "message": "应用版本必须填写",
                            "required": True
                        }, {
                            "message": "应用版本格式不匹配",
                            "pattern": "/^[a-z|A-Z|0-9|\\-|_\\.]{1,8}$/"
                        }],
                        "options": {
                            "width": "100%",
                            "pattern": "/^[a-z|A-Z|0-9|\\-|_\\.]{1,8}$/",
                            "dataType": "string",
                            "disabled": False,
                            "required": True,
                            "labelWidth": 100,
                            "remoteFunc": "func_1616053523000_8325",
                            "placeholder": "",
                            "defaultValue": "",
                            "showPassword": False,
                            "labelWidthStatus": True,
                            "labelWidthDisabled": False
                        }
                    }],
                    "span":
                    12
                }],
                "options": {
                    "align": "top",
                    "gutter": 0,
                    "justify": "start",
                    "labelWidth": 100,
                    "remoteFunc": "func_1616053356000_7895",
                    "labelWidthStatus": True,
                    "labelWidthDisabled": False
                }
            }, {
                "key": "1613635281000_24319",
                "icon": "icon-diy-com-textarea",
                "name": "版本说明",
                "type": "textarea",
                "model": "textarea_1613635281000_24319",
                "rules": [{
                    "message": "版本说明必须填写",
                    "required": True
                }],
                "options": {
                    "width": "100%",
                    "pattern": "",
                    "disabled": False,
                    "required": True,
                    "labelWidth": 100,
                    "remoteFunc": "func_1613635281000_24319",
                    "placeholder": "请详细描述本次提测相关内容",
                    "defaultValue": "",
                    "labelWidthStatus": True,
                    "labelWidthDisabled": False
                }
            }, {
                "key": "1614176282000_71093",
                "icon": "icon-input",
                "name": "分割线",
                "type": "divider",
                "model": "divider_1614176282000_71093",
                "rules": [],
                "options": {
                    "direction": "horizontal",
                    "font_size": "15px",
                    "font_color": "#606266",
                    "remoteFunc": "func_1614176282000_71093",
                    "font_family": "",
                    "font_weight": "500",
                    "defaultValue": "分割线",
                    "content_position": "center"
                }
            }, {
                "key":
                "1614176103000_46651",
                "icon":
                "icon-grid-",
                "name":
                "栅格布局",
                "type":
                "grid",
                "model":
                "grid_1614176103000_46651",
                "rules": [],
                "columns": [{
                    "list": [{
                        "key": "1613639231000_48190",
                        "icon": "icon-radio-active",
                        "name": "有无自测",
                        "type": "radio",
                        "model": "radio_1613639231000_48190",
                        "rules": [],
                        "options": {
                            "props": {
                                "label": "label",
                                "value": "value"
                            },
                            "width":
                            "",
                            "inline":
                            True,
                            "remote":
                            False,
                            "options": [{
                                "label": "Option 1",
                                "value": "是"
                            }, {
                                "label": "Option 2",
                                "value": "否"
                            }],
                            "disabled":
                            True,
                            "required":
                            False,
                            "showLabel":
                            False,
                            "labelWidth":
                            100,
                            "remoteFunc":
                            "func_1613639231000_48190",
                            "defaultValue":
                            "是",
                            "remoteOptions": [],
                            "labelWidthStatus":
                            True,
                            "labelWidthDisabled":
                            False
                        }
                    }],
                    "span":
                    12
                }, {
                    "list": [{
                        "key": "1613639268000_11141",
                        "icon": "icon-radio-active",
                        "name": "有无联调",
                        "type": "radio",
                        "model": "radio_1613639268000_11141",
                        "rules": [],
                        "options": {
                            "props": {
                                "label": "label",
                                "value": "value"
                            },
                            "width":
                            "",
                            "inline":
                            True,
                            "remote":
                            False,
                            "options": [{
                                "label": "Option 1",
                                "value": "否"
                            }, {
                                "label": "Option 2",
                                "value": "是"
                            }],
                            "disabled":
                            False,
                            "required":
                            False,
                            "showLabel":
                            False,
                            "labelWidth":
                            100,
                            "remoteFunc":
                            "func_1613639268000_11141",
                            "defaultValue":
                            "否",
                            "remoteOptions": [],
                            "labelWidthStatus":
                            True,
                            "labelWidthDisabled":
                            False
                        }
                    }],
                    "span":
                    12
                }],
                "options": {
                    "align": "top",
                    "gutter": 0,
                    "justify": "start",
                    "remoteFunc": "func_1614176103000_46651"
                }
            }, {
                "key":
                "1614314894000_46859",
                "icon":
                "icon-grid-",
                "name":
                "栅格布局",
                "type":
                "grid",
                "model":
                "grid_1614314894000_46859",
                "rules": [],
                "columns": [{
                    "list": [{
                        "key":
                        "1614314900000_89037",
                        "icon":
                        "icon-input",
                        "name":
                        "开发者邮箱",
                        "type":
                        "input",
                        "model":
                        "input_order_creator_email_id",
                        "rules": [{
                            "type": "email",
                            "message": "开发者邮箱格式不正确"
                        }, {
                            "message": "开发者邮箱必须填写",
                            "required": True
                        }, {
                            "message": "开发者邮箱格式不匹配",
                            "pattern": "/.*@sensetime.com$/"
                        }],
                        "options": {
                            "width": "100%",
                            "pattern": "/.*@sensetime.com$/",
                            "dataType": "email",
                            "disabled": False,
                            "required": True,
                            "labelWidth": 100,
                            "remoteFunc": "func_1614314900000_89037",
                            "placeholder": "如: 必须是xxx@sensetime.com",
                            "defaultValue": "",
                            "showPassword": False,
                            "labelWidthStatus": True,
                            "labelWidthDisabled": False
                        }
                    }],
                    "span":
                    12
                }, {
                    "list": [{
                        "key":
                        "1618901425000_49605",
                        "icon":
                        "icon-input",
                        "name":
                        "其它通知人",
                        "type":
                        "input",
                        "model":
                        "input_other_senders_emails_id",
                        "rules": [{
                            "type": "string",
                            "message": "其它通知人格式不正确"
                        }, {
                            "message":
                            "其它通知人格式不匹配",
                            "pattern":
                            "/^((([a-z0-9_\\.-]+)@(sensetime)\\.(com,))*(([a-z0-9_\\.-]+)@(sensetime)\\.(com)))$/"
                        }],
                        "options": {
                            "width": "100%",
                            "pattern":
                            "/^((([a-z0-9_\\.-]+)@(sensetime)\\.(com,))*(([a-z0-9_\\.-]+)@(sensetime)\\.(com)))$/",
                            "dataType": "string",
                            "disabled": False,
                            "required": False,
                            "labelWidth": 100,
                            "remoteFunc": "func_1618901425000_49605",
                            "placeholder": "如: 可选择需要通知的其它人邮箱，多个通知人以逗号分隔",
                            "defaultValue": "",
                            "showPassword": False,
                            "labelWidthStatus": True,
                            "labelWidthDisabled": False
                        }
                    }],
                    "span":
                    12
                }],
                "options": {
                    "align": "top",
                    "gutter": 0,
                    "justify": "start",
                    "remoteFunc": "func_1614314894000_46859"
                }
            }, {
                "key":
                "1613636358000_60042",
                "icon":
                "icon-grid-",
                "name":
                "栅格布局",
                "type":
                "grid",
                "model":
                "grid_1613636358000_60042",
                "rules": [],
                "columns": [{
                    "list": [{
                        "key": "1614314860000_75631",
                        "icon": "icon-radio-active",
                        "name": "数据库修改",
                        "type": "radio",
                        "model": "radio_1614314860000_75631",
                        "rules": [],
                        "options": {
                            "props": {
                                "label": "label",
                                "value": "value"
                            },
                            "width":
                            "",
                            "inline":
                            True,
                            "remote":
                            False,
                            "options": [{
                                "label": "Option 1",
                                "value": "否"
                            }, {
                                "label": "Option 2",
                                "value": "是"
                            }],
                            "disabled":
                            False,
                            "required":
                            False,
                            "showLabel":
                            False,
                            "labelWidth":
                            100,
                            "remoteFunc":
                            "func_1614314860000_75631",
                            "defaultValue":
                            "否",
                            "remoteOptions": [],
                            "labelWidthStatus":
                            True,
                            "labelWidthDisabled":
                            False
                        }
                    }],
                    "span":
                    12
                }, {
                    "list": [{
                        "key": "1614176251000_48132",
                        "icon": "icon-radio-active",
                        "name": "配置修改",
                        "type": "radio",
                        "model": "radio_1614176251000_48132",
                        "rules": [],
                        "options": {
                            "props": {
                                "label": "label",
                                "value": "value"
                            },
                            "width":
                            "",
                            "inline":
                            True,
                            "remote":
                            False,
                            "options": [{
                                "label": "Option 1",
                                "value": "否"
                            }, {
                                "label": "Option 2",
                                "value": "是"
                            }],
                            "disabled":
                            False,
                            "required":
                            False,
                            "showLabel":
                            False,
                            "labelWidth":
                            100,
                            "remoteFunc":
                            "func_1614176251000_48132",
                            "defaultValue":
                            "否",
                            "remoteOptions": [],
                            "labelWidthStatus":
                            True,
                            "labelWidthDisabled":
                            False
                        }
                    }],
                    "span":
                    12
                }],
                "options": {
                    "align": "top",
                    "gutter": 0,
                    "justify": "start",
                    "remoteFunc": "func_1613636358000_60042"
                }
            }, {
                "key": "1614176349000_52899",
                "icon": "icon-diy-com-textarea",
                "name": "修改说明",
                "type": "textarea",
                "model": "textarea_1614176349000_52899",
                "rules": [],
                "options": {
                    "width": "100%",
                    "pattern": "",
                    "disabled": False,
                    "required": False,
                    "labelWidth": 100,
                    "remoteFunc": "func_1614176349000_52899",
                    "placeholder":
                    "请描述修改相关内容，如果有数据库表结构的调整，请及时提交数据库修改申请，以免造成上线生产环境后异常",
                    "defaultValue": "",
                    "labelWidthStatus": True,
                    "labelWidthDisabled": False
                }
            }],
            "config": {
                "size": "small",
                "labelWidth": 100,
                "customClass": "",
                "labelPosition": "right"
            },
            "id":
            24
        }],
        "form_data": [{
            "input_wotype_id":
            "修复单",
            "input_product_version_id":
            "1.1",
            "select_1642655261000_97559":
            "engine-industry-image-process-service",
            "text_1618901016000_73105":
            "产品线定义版本",
            "text_1618901008000_76230":
            "开发在上线时环境只能选择【test】否则工单将自动关闭",
            "subform_version_info_id": [{
                "input_deploy_app_id":
                "argo-engine",
                "input_deploy_release_version_id":
                "v2.0"
            }, {
                "input_deploy_app_id":
                "op-service",
                "input_deploy_release_version_id":
                "v1.0"
            }, {
                "input_deploy_app_id":
                "industry-frontend",
                "input_deploy_release_version_id":
                "v3.0"
            }, {
                "input_deploy_app_id":
                "zsk-zsk",
                "input_deploy_release_version_id":
                "v4.0"
            }],
            "textarea_1613635281000_24319":
            "xxxx",
            "divider_1614176282000_71093":
            "分割线",
            "radio_1613639231000_48190":
            "是",
            "radio_1613639268000_11141":
            "否",
            "input_order_creator_email_id":
            "zhoushuke@sensetime.com",
            "input_other_senders_emails_id":
            "",
            "radio_1614314860000_75631":
            "否",
            "radio_1614176251000_48132":
            "否",
            "textarea_1614176349000_52899":
            ""
        }]
    },
    "tasks": ["fallen_pre_check_spring-c747f0218614-zhoushuke.py"],
    "is_exec_task":
    True
}
"""


def checker(data, structure):
    data_json = json.loads(data)
    struct_json = json.loads(structure)
    checker = AppCheckInBackend(data_json, struct_json)
    checker("QATesting")


if __name__ == "__main__":
    # checker = AppCheckInBackend(d["tpls"]["form_data"][0], d["tpls"]["form_structure"][0])
    # checker("QATesting")
    checker()
