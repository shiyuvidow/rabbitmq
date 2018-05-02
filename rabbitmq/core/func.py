#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 16:14
# @Author  : WangWei
# @File    : func.py
# @Software: PyCharm

import socket
import fcntl
import struct
from conf import settings

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', settings.IFNAME[:15]))[20:24])