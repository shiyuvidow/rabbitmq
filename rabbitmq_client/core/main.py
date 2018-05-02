#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/26 10:01
# @Author  : WangWei
# @File    : main.py
# @Software: PyCharm

tmp_dict = {}

import re
from rpc_module import RpcCmdClient


class RPC(object):
    def __init__(self):
        self.exec_module_dict = {
            'run': 'run_cmd',
            'check_task': 'check_task'}
        self.hosts_list = []
        self.module = ''
        self.module_args = ''

    def interactive(self):
        print "start interactive with you"
        self.print_help()
        while 1:
            choice = raw_input('>>:').strip()
            if choice == "exit":
                exit("exit")
            if len(choice) == 0:
                continue
            if not self.verify_args(choice):
                continue
            self.exec_rpc()

    def verify_args(self, choice):
        req_cmd = re.split("run|--hosts", choice)
        if len(req_cmd) > 1:
            x1, args_str, hosts_str = req_cmd
            self.module_args = args_str.strip()
            self.hosts_list = hosts_str.strip().split()
            if not self.hosts_list:
                print("no hosts")
                return 0
            self.module = 'run'
            return 1

        req_check = re.split("check_task", choice)
        if len(req_check) > 1:
            x1, args_str = req_check
            self.module_args = args_str.strip()
            self.module = 'check_task'
            return 1

        print("invalid cmd")
        return

    def print_help(self):
        print("""
        Usage: run "df -h" --hosts 192.168.3.55 10.4.3.4
               check_task 950f6ae6-603d-4c5a-baf7-a8e01b817bcc
        """)

    def exec_rpc(self):
        func_args = self.exec_module_dict[self.module]
        if hasattr(self, func_args):
            func = getattr(self, func_args)
            func()
        else:
            self.print_help()

    def run_cmd(self):
        for host in self.hosts_list:
            rpc_object = RpcCmdClient(host, self.module_args)
            print(" [x] Requesting hosts:{}, cmd:{}".format(host, self.module_args))
            response = rpc_object.call()
            tmp_dict[response[0]] = response[1]
            print(" [.] Please check_task {}".format(response[0]))

    def check_task(self):
        try:
            print(tmp_dict[self.module_args])
            del tmp_dict[self.module_args]
        except IndexError:
            self.print_help()