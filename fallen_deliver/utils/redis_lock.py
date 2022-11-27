#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Author: zhoushuke
Email: zhoushuke@sensetime.com
Date: 2021-09-10 11:35:42
LastEditors: zhoushuke
LastEditTime: 2021-09-10 12:50:05
FilePath: /fallen_deliver/utils/redis_lock.py
'''
import time
import hashlib
import functools
import redis_lock
from config import cfg as CFG
from redis import StrictRedis


def rds_lock_decorator(rkey='', expired=300):
    """
    When you want to lock a function from more than 1 call at a time.
    """
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            conn = StrictRedis(host=CFG["fallen"]["redis"]["host"],
                               port=CFG["fallen"]["redis"]["port"],
                               password=CFG["fallen"]["redis"]["password"],
                               db=CFG["fallen"]["redis"]["db"],
                               decode_responses=True)
            if not rkey:
                tmp = str(args) + str(kwargs)
                lock_key = hashlib.md5(tmp.encode("utf-8")).hexdigest()
            else:
                lock_key = rkey
            with redis_lock.Lock(conn, lock_key, expired):
                return func(*args, **kwargs)

        return inner

    return decorator


@rds_lock_decorator("xxyy", 60)
def test(x, y):
    print("Got the lock. Doing some work ...")
    time.sleep(40)
    print("released the lock...")


if __name__ == "__main__":
    test(1, 2)
