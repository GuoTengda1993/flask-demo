# -*- coding: utf-8 -*-
import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

import click
from flask import Flask, request
from flask_uploads import configure_uploads
from flask_restful import Api

from demo.extensions import db, login_manager, csrf, mail, moment, migrate, sqls, mongodb
from demo.models import *
from demo.settings import config, TaskConfig

from demo.api.user import UserList, UserManage, UserOperation
from demo.api.auth import Login, Logout
from demo.api.about import AboutPage

# import atexit
# if sys.platform == 'linux':
#     import fcntl

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
scheduler = TaskConfig().scheduler


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('demo')
    app.config.from_object(config[config_name])
    api = Api(app)

    register_logging(app)
    register_extensions(app)
    register_commands(app)
    register_apis(api)
    # if sys.platform == 'linux':
    #     f = open("scheduler.lock", "wb")
    #     try:
    #         fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    #         scheduler.start()
    #     except:
    #         pass
    #
    #     def unlock():
    #         fcntl.flock(f, fcntl.LOCK_UN)
    #         f.close()
    #     atexit.register(unlock)
    # else:
    scheduler.start()
    # atexit.register(tear_down)
    return app


def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/demo.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject='Bluelog Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)


def register_extensions(app):
    db.init_app(app)
    db.app = app
    db.metadata.clear()
    db.create_all()
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    configure_uploads(app, sqls)
    mongodb.init_app(app)


# def register_shell_context(app):
#     @app.shell_context_processor
#     def make_shell_context():
#         return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


# def register_errors(app):
#     @app.errorhandler(400)
#     def bad_request(e):
#         return render_template('errors/400.html'), 400
#
#     @app.errorhandler(404)
#     def page_not_found(e):
#         return render_template('errors/404.html'), 404
#
#     @app.errorhandler(500)
#     def internal_server_error(e):
#         return render_template('errors/500.html'), 500
#
#     @app.errorhandler(CSRFError)
#     def handle_csrf_error(e):
#         return render_template('errors/400.html', description=e.description), 400


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building Bluelog, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username,
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')


# def register_request_handlers(app):
#     @app.after_request
#     def query_profiler(response):
#         for q in get_debug_queries():
#             if q.duration >= app.config['BLUELOG_SLOW_QUERY_THRESHOLD']:
#                 app.logger.warning(
#                     'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
#                     % (q.duration, q.context, q.statement)
#                 )
#         return response


def register_apis(api):
    api.add_resource(UserList, '/api/users')
    api.add_resource(UserManage, '/api/user/<id>', '/api/user')
    api.add_resource(UserOperation, '/api/userOperation/<operation>/<id>')
    api.add_resource(Login, '/api/login')
    api.add_resource(Logout, '/api/logout')
    api.add_resource(AboutPage, '/api/about')
