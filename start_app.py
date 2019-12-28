import gevent.monkey
import multiprocessing
import os
path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]

_file_name = os.path.basename(__file__)
"""
gunicorn的配置文件
"""
# gevent的猴子魔法 变成非阻塞
gevent.monkey.patch_all()
debug = True
loglevel = 'info'
bind = '0.0.0.0:5000'
pidfile = '%s/logs/gunicorn.pid' % (path_of_current_dir,)
errorlog = '%s/logs/info.log' % (path_of_current_dir,)
accesslog = '%s/logs/access.log' % (path_of_current_dir,)
# 启动的进程数
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'
preload_app = False
daemon = True
x_forwarded_for_header = 'X-FORWARDED-FOR'
