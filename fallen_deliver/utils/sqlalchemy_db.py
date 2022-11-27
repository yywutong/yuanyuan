#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2021-08-17 11:16:46
LastEditors: zhoushuke
LastEditTime: 2022-02-01 13:30:55
FilePath: /fallen_deliver/utils/sqlalchemy_db.py
'''

from functools import wraps
from config import cfg as CFG
from collections.abc import Iterable
from sqlalchemy import create_engine, Column, Integer, VARCHAR, JSON
from contextlib import contextmanager
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def init_engines(db):
    """初始化数据库连接"""
    mysql = {
        '{}'.format(db): {
            'user': CFG["fallen"]["mysql"]["username"],
            'passwd': CFG["fallen"]["mysql"]["password"],
            'host': CFG["fallen"]["mysql"]["host"],
            'port': CFG["fallen"]["mysql"]["port"],
            'db': db,
        }
    }
    for k, v in mysql.items():
        mysql_url = ("mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}"
                     "?charset=utf8".format(**v))
        engine = create_engine(mysql_url,
                               pool_size=10,
                               max_overflow=-1,
                               pool_recycle=1000,
                               echo=False)
    return engine


def get_session(db):
    """获取session"""
    return scoped_session(
        sessionmaker(bind=init_engines(db), expire_on_commit=False))()


@contextmanager
def Db_session(db='ferry', commit=True):
    """db session封装.

    :params db:数据库名称
    :params commit:进行数据库操作后是否进行commit操作的标志
                   True：commit, False:不commit
    """
    session = get_session(db)
    try:
        yield session
        if commit:
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        if session:
            session.close()


def class_dbsession(commit=True):
    """用于BaseModel中进行数据库操作前获取dbsession操作.

    :param commit:进行数据库操作后是否进行commit操作的标志，True：commit, False:不commit
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            # cls为对象或类
            cls = args[0]
            # 实际传入的参数
            new_args = args[1:]
            with Db_session(cls._db_name, commit) as session:
                return func(cls, session, *new_args, **kwargs)

        return inner

    return wrapper


class BaseModel(object):
    u"""基础模型.自动commit"""

    _db_name = "ferry"

    @class_dbsession(True)
    def add(self, session):
        u"""增.

        eg: a = MerchantBillDetail(id=1)
            a.add()
        """
        session.add(self)

    @classmethod
    @class_dbsession(True)
    def batch_add(cls, session, objs):
        """批量增加.

        eg: a = [MerchantBillDetail(id=1), MerchantBillDetail(id=2)]
            MerchantBillDetail.batch_add(a)
        """
        return session.add_all(objs)

    @classmethod
    @class_dbsession(True)
    def delete(cls, session, where_conds=[]):
        u"""删.

        eg: BaseModel.delete([BaseModel.a>1, BaseModel.b==2])
        """
        session.query(cls).filter(*where_conds).delete(
            synchronize_session='fetch')

    @classmethod
    @class_dbsession(True)
    def update(cls, session, update_dict, where_conds=[]):
        u"""更新.

        eg: BaseModel.update({'name': 'jack'}, [BaseModel.id>=1])
        """
        return session.query(cls).filter(*where_conds).update(
            update_dict, synchronize_session='fetch')

    @classmethod
    @class_dbsession(True)
    def join(cls, session, other_model, rnt_keys, join_condition,
             filter_condition):
        u"""
        两表连接查询
        """
        return session.query(cls, *rnt_keys).join(
            other_model, *join_condition).filter(*filter_condition).all()

    @classmethod
    @class_dbsession(False)
    def query(cls, session, params, **where_conds):
        u"""查询.

        eg: BaseModel.query([BaseModel.id, BaseModel.name],
                filter=[BaseModel.id>=1],
                group_by=[BaseModel.id, BaseModel.name]
                order_by=BaseModel.id.desc(), limit=10, offset=0)
        """
        if where_conds:
            if not set(where_conds.keys()).issubset({
                    'filter', 'group_by', 'order_by', 'limit', 'offset',
                    'query_first'
            }):
                raise Exception('input para error!')
        cfilter = where_conds.pop('filter', None)
        group_para = where_conds.pop('group_by', None)
        order_para = where_conds.pop('order_by', None)
        limit = where_conds.pop('limit', None)
        offset = where_conds.pop('offset', None)
        query_first = where_conds.get('query_first', False)

        if not isinstance(params, Iterable):
            params = [params]
        squery = session.query(*params)
        if cfilter is not None:
            squery = squery.filter(*cfilter)
        if group_para is not None:
            squery = squery.group_by(*group_para)
        if order_para is not None:
            squery = squery.order_by(order_para)
        if limit is not None:
            squery = squery.limit(limit)
        if offset is not None:
            squery = squery.offset(offset)
        if query_first:
            return squery.first()
        return squery.all()

    # @classmethod
    # @class_dbsession(False)
    # def __aggregate(cls, session, aggr_fun, params, where_conds=[]):
    #     u"""对参数进行聚合函数(sum, avg, max, min)计算.
    #
    #     BaseModel.__aggregate(func.sum,
    #                         [BaseModel.id, BaseModel.num], [BaseModel.id==1])
    #     """
    #     if not isinstance(params, Iterable):
    #         params = [params]
    #     aggr_list = [aggr_fun(param) for param in params]
    #     re = session.query(*aggr_list).filter(*where_conds).one()
    #     if len(re) == 1:
    #         return re[0] or 0
    #     return [i or 0 for i in re]
    #
    # @classmethod
    # def sum(cls, params, where_conds=[]):
    #     u"""求和.
    #
    #     eg: BaseModel.sum([BaseModel.id], [BaseModel.id==1])
    #     """
    #     return cls.__aggregate(func.sum, params, where_conds)
    #
    # @classmethod
    # def max(cls, params, where_conds=[]):
    #     u"""求最大值.
    #
    #     eg: BaseModel.max([BaseModel.num], [BaseModel.id==2])
    #     """
    #     return cls.__aggregate(func.max, params, where_conds)
    #
    # @classmethod
    # @class_dbsession(False)
    # def count(cls, session, params, where_conds=[], distinct=False):
    #     u"""计数.
    #
    #     eg: BaseModel.count([BaseModel.id, BaseModel.XXX], [BaseModel.id==2])
    #         BaseModel.count(BaseModel.id, [BaseModel.id==2], True)
    #     """
    #     if distinct:
    #         if isinstance(params, Iterable) and len(params) >= 2:
    #             re = session.query(func.count(
    #                 func.distinct(func.concat(*params))))\
    #                 .filter(*where_conds).one()[0]
    #         elif isinstance(params, Iterable):
    #             qp = params[0]
    #             re = session.query(func.count(
    #                 func.distinct(qp))).filter(*where_conds).one()[0]
    #         else:
    #             re = session.query(func.count(
    #                 func.distinct(params))).filter(*where_conds).one()[0]
    #     else:
    #         if not isinstance(params, Iterable):
    #             params = [params]
    #         re = session.query(*params).filter(*where_conds).count()
    #     return re

    @classmethod
    @class_dbsession(False)
    def simple_paging_query(cls, session, params, where_conds, page_size=100):
        """简单分页查询
        """
        total_count = cls.count([cls.id], where_conds)
        rv = []
        for offset in range(0, total_count, page_size):
            rv.extend(
                cls.query(params,
                          filter=where_conds,
                          offset=offset,
                          limit=page_size))
        return rv

    @classmethod
    def execute(cls, sql_str):
        with Db_session(cls._db_name, commit=True) as session:
            return session.execute(sql_str)


def get_oncall_info_by_role(role):
    Base = declarative_base()

    class SysUser(Base, BaseModel):
        __tablename__ = "sys_user"
        _db_name = "ferry"
        user_id = Column(Integer, primary_key=True)
        role_id = Column(Integer)
        email = Column(VARCHAR(128))
        phone = Column(VARCHAR(11))

    class SysRole(Base, BaseModel):
        __tablename__ = "sys_role"
        _db_name = "ferry"
        role_id = Column(Integer, primary_key=True)
        role_key = Column(VARCHAR(128))
        role_name = Column(VARCHAR(128))

    x = SysUser.join(
        SysRole,
        rnt_keys=[SysUser.phone, SysUser.email, SysRole.role_name],
        join_condition=[SysUser.role_id == SysRole.role_id],
        filter_condition=[SysRole.role_key == role])
    return x


def get_iphone_role_by_email(email):
    Base = declarative_base()

    class SysUser(Base, BaseModel):
        __tablename__ = "sys_user"
        _db_name = "ferry"
        user_id = Column(Integer, primary_key=True)
        role_id = Column(Integer)
        email = Column(VARCHAR(128))
        remark = Column(VARCHAR(255))
        phone = Column(VARCHAR(11))

    class SysRole(Base, BaseModel):
        __tablename__ = "sys_role"
        _db_name = "ferry"
        role_id = Column(Integer, primary_key=True)
        role_name = Column(VARCHAR(128))

    # single query, reture list: [(xxxx),(yyyy)] query_first return a (xxxx,)
    # rnt = SysUser.query([SysUser.phone],
    #                     filter=[SysUser.email == email],
    #                     query_first=True)
    # return rnt

    if email in CFG["wchook"]["extend_role"]:
        x = SysUser.join(SysRole,
                         rnt_keys=[SysUser.remark, SysRole.role_name],
                         join_condition=[SysUser.role_id == SysRole.role_id],
                         filter_condition=[SysUser.email == email])
    else:
        x = SysUser.join(SysRole,
                         rnt_keys=[SysUser.phone, SysRole.role_name],
                         join_condition=[SysUser.role_id == SysRole.role_id],
                         filter_condition=[SysUser.email == email])
    return x


def get_apps_list_by_status_include_ops(product, status):

    Base = declarative_base()

    class AppsList(Base, BaseModel):
        __tablename__ = "apps_list"
        _db_name = "ferry"
        product = Column(Integer)
        name = Column(Integer, primary_key=True)
        enable = Column(Integer)
        ckkey = Column(VARCHAR(20))

    rnt = AppsList.query([AppsList.name],
                         filter=[
                             AppsList.enable == 1, AppsList.ckkey == status,
                             AppsList.product == product
                         ])
    return rnt


# 根据子表单中的应用名去更新apps_list中对应应用的ckkey设置为QATesting
# 等QA验证完成之后再将其ckkey设置为空
def update_apps_status_by_fallen_subform(apps=[], set_key={}):

    Base = declarative_base()

    class AppsList(Base, BaseModel):
        __tablename__ = "apps_list"
        _db_name = "ferry"
        product = Column(Integer)
        name = Column(VARCHAR(128), primary_key=True)
        version = Column(VARCHAR(20))
        ckkey = Column(VARCHAR(20))
        enable = Column(Integer)

    # filter的in 需要使用field.in_(xxx)形式, filter中多个条件是and关系
    # 参考: https://blog.csdn.net/chenmixuexi_/article/details/109010082?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_paycolumn_v3&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_paycolumn_v3&utm_relevant_index=1
    # AppsList.query([AppsList.name],
    #                filter=[AppsList.name.in_(apps), AppsList.enable == 1])
    # 根据应用名及enable进行过滤
    AppsList.update(set_key, [AppsList.name.in_(apps), AppsList.enable == 1])


def get_db_structure_by_tpl_id(tpl_id):
    Base = declarative_base()

    class TpLFromStruct(Base, BaseModel):
        __tablename__ = "p_tpl_info"
        _db_name = "ferry"
        id = Column(Integer, primary_key=True)
        form_structure = Column(JSON)

    return TpLFromStruct.query([TpLFromStruct.form_structure],
                               filter=[TpLFromStruct.id == tpl_id],
                               query_first=True)


def update_db_form_structure(tpl_id, json):
    Base = declarative_base()

    class TpLFromStruct(Base, BaseModel):
        __tablename__ = "p_tpl_info"
        _db_name = "ferry"
        id = Column(Integer, primary_key=True)
        form_structure = Column(JSON)

    return TpLFromStruct.update({"form_structure": json},
                                [TpLFromStruct.id == tpl_id])


def get_apps_list_by_status(product):

    Base = declarative_base()

    class AppsList(Base, BaseModel):
        __tablename__ = "apps_list"
        _db_name = "ferry"
        product = Column(Integer)
        name = Column(Integer, primary_key=True)
        enable = Column(Integer)
        ckkey = Column(VARCHAR(20))

    tc = AppsList.query([AppsList.name],
                        filter=[
                            AppsList.enable == 1,
                            AppsList.ckkey == "QATesting",
                            AppsList.product == product
                        ])

    sx = AppsList.query([AppsList.name],
                        filter=[
                            AppsList.enable == 1,
                            AppsList.ckkey != "QATesting",
                            AppsList.product == product
                        ])
    # apps 原始的格式 ['argo-engine', 'op-service']
    return [x[0] for x in tc], [x[0] for x in sx]


if __name__ == "__main__":
    printx = get_iphone_role_by_email("zhoushuke@sensetime.com")
    print(printx)
    if printx:
        print(len(printx), printx[0][1], printx[0][2])

    # for example:
    # from sqlalchemy.ext.declarative import declarative_base
    # Base = declarative_base()

    # class Test(Base， BaseModel):
    #     __tablename__ == 'test'
    #     _db_name = 'db_name'
    #     id = Column(BigInteger, primary_key=True)
    #     name = Column(String(128))

    # # 新增
    # t = Test(id=1, name='test')
    # t.add()

    # # 删除
    # Test.delete([Test.id == 1])

    # # 修改
    # Test.update({'name': 'haha'}, [Test.id == 1])

    # # 查找
    # Test.query([Test.name], filter=[Test.id == 1])
