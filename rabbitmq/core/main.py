#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/26 14:22
# @Author  : WangWei
# @File    : main.py
# @Software: PyCharm

import pika
from shell_cmd import ShellCmd
from conf import settings
from core import func

class RPC(object):
    """
    rpc命令端
    """
    def __init__(self):
         # 建立连接
        self.queue = func.get_ip()
        creds = pika.PlainCredentials(settings.RABBITMQ_INFO['user'], settings.RABBITMQ_INFO['passwd'])
        self.connection = pika.BlockingConnection(pika.ConnectionParameters
                                                  (host=settings.RABBITMQ_INFO['host'], credentials=creds))
        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def exec_cmd(self, cmd):
        cmd_obj = ShellCmd(cmd)
        cmd_obj.run()
        return cmd_obj.result()

    def on_request(self, ch, method, props, body):
        print(" [x] exec cmd: {}".format(body))
        response = self.exec_cmd(body)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))
        # 确认消息已被消费
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        # 限制消费数，当前消息正在处理不接收消息
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue=self.queue)
        print(" [x] Awaiting RPC requests")
        # 阻塞
        self.channel.start_consuming()