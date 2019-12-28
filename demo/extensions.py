# -*- coding: utf-8 -*-
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_uploads import UploadSet
from flask_pymongo import PyMongo

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
moment = Moment()
migrate = Migrate()
sqls = UploadSet('sqls')
mongodb = PyMongo()


@login_manager.user_loader
def load_user(user_id):
    from demo.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
