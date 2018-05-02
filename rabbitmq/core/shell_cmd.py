#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/26 14:48
# @Author  : WangWei
# @File    : shell_cmd.py
# @Software: PyCharm

import os
import subprocess
import signal
import time

# 超时时间
timeout = 300


class ShellCmd(object):
    """
    执行命令类
    """
    def __init__(self, cmd):
        self.cmd = cmd
        self.ret_code = None
        self.ret_info = None
        self.err_info = None
        self._process = None

    def run_background(self):
        self._process = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 设置轮询时间
        poll_seconds = 2
        deadline = time.time() + timeout
        while time.time() < deadline and self._process.poll() is None:
            time.sleep(poll_seconds)
        if self._process.poll() is None:
            # 中断
            self._process.terminate()
            self.ret_info, self.err_info = "", ""
            self.ret_code = -1
        else:
            self.ret_info, self.err_info = self._process.communicate()
            self.ret_code = self._process.returncode

    def run(self):
        self.run_background()

    def run_cmd(self, cmd):
        self.cmd = cmd
        self.run()

    def get_status(self):
        retcode = self._process.poll()
        status = "RUNNING" if retcode is None else "FINISHED"
        return status

    def send_signal(self, sig):
        os.kill(self._process.pid, sig)

    def terminate(self):
        self.send_signal(signal.SIGTERM)

    def kill(self):
        self.send_signal(signal.SIGKILL)

    def result(self):
        if self.ret_info and self.err_info:
            return self.ret_info + '\n\n' + self.err_info
        elif self.ret_info:
            return self.ret_info
        else:
            return self.err_info