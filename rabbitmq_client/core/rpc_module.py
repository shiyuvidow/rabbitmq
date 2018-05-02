#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/26 11:13
# @Author  : WangWei
# @File    : rpc_module.py
# @Software: PyCharm

import pika
import uuid
import time
from conf import settings


class RpcCmdClient(object):
    """执行命令rpc客户端"""

    def __init__(self, host, cmd):
        self.response = None
        self.queue = host
        self.cmd = cmd
        self.corr_id = None
        self.try_count = 0
        # 建立连接
        creds = pika.PlainCredentials(settings.RABBITMQ_INFO['user'], settings.RABBITMQ_INFO['passwd'])
        self.connection = pika.BlockingConnection(pika.ConnectionParameters
                                                  (host=settings.RABBITMQ_INFO['host'], credentials=creds))
        # 声明管道
        self.channel = self.connection.channel()
        # 生成随机队列
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response,
                                   no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        # print("---->", method, props)
        # 检测uuid，保持数据一致
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self):
        # 生成uuid
        self.corr_id = str(uuid.uuid4())
        self.channel.publish(exchange="",
                             routing_key=self.queue,
                             properties=pika.BasicProperties(
                                 reply_to=self.callback_queue,
                                 correlation_id=self.corr_id),
                             body=str(self.cmd))

        while self.response is None:
            # 非阻塞版的start_consumer()
            self.connection.process_data_events()
        return self.corr_id, self.response