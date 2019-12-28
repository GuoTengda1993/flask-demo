# -*- coding: utf-8 -*-
import os
import re


def get_pid_and_kill():
    all_pid_info = os.popen('ps -ef | grep wsgi:app')
    pid_list = all_pid_info.readlines()
    pids = []
    for each in pid_list:
        if 'wsgi' in each and 'grep' not in each:
            wsgi_pid_info = each.strip()
            wsgi_pid = re.split('\s+', wsgi_pid_info)[1]
            pids.append(wsgi_pid)
    for p in pids:
        kill_command = 'kill {pid}'.format(pid=p)
        print(kill_command)
        os.popen(kill_command)


if __name__ == '__main__':
    get_pid_and_kill()
