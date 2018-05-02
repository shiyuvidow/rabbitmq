#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/11 17:43
# @Author  : WangWei
# @File    : settings.py
# @Software: PyCharm

import os
import sys

# 程序目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# RABBITMQ信息
RABBITMQ_INFO = {
    'host': '10.12.7.1',
    'user': 'admin',
    'passwd': '123456'
}

# 网卡
IFNAME = "eth0"
