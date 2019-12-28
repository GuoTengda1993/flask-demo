# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource
from flask_login import login_user, logout_user
from demo.models import Admin


class Login(Resource):

    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        msg = None
        if username is None or password is None:
            msg, code = '请输入用户名及密码', 210
        user = Admin.query.filter_by(username=username).first()
        if user is None or not user.validate_password(password):
            msg, code = '账号不存在或密码错误', 210
        if msg:
            _response = {
                'code': code,
                'res': '',
                'msg': msg
            }
            return _response, code
        else:
            login_user(user, True)
            token = user.generate_reset_token()
            token = bytes.decode(token)
            _response = {
                'code': 200,
                'res': {'username': username, 'name': user.name, 'user_id': user.id, 'token': token,},
                'msg': '登陆成功'
            }
            return _response, 200


class Logout(Resource):

    def get(self):
        logout_user()
        _response = {
            'code': 200,
            'res': '',
            'msg': '登出成功'
        }
        return _response, 200
