# -*- coding: utf-8 -*-
import os
import sys
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    MAIL_SERVER = ''  # os.getenv('MAIL_SERVER')
    MAIL_PORT = 25  # 465
    MAIL_USERNAME = ''  # os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = ''  # os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('', MAIL_USERNAME)

    MONGO_DBNAME = 'data'
    MONGO_URI = 'mongodb://root:password@10.X.X.X:27017/data?authSource=admin'


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data.sqlite')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


class TaskConfig:
    jobstores = {'default': SQLAlchemyJobStore(url="sqlite:///" + os.path.join(basedir, "data.sqlite"))}
    executors = {'default': ThreadPoolExecutor(10), 'processpool': ProcessPoolExecutor(3)}
    job_defaults = {'coalesce': True, 'max_instances': 3}

    def __init__(self):
        self.scheduler = BackgroundScheduler(jobstores=self.jobstores, executors=self.executors,
                                             job_defaults=self.job_defaults, timezone=timezone('Asia/Shanghai'))


config = {
    'development': TestingConfig,
    'testing': TestingConfig,
    'production': TestingConfig
}
