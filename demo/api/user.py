# -*- coding: utf-8 -*-
from flask_restful import Resource
from demo.utils import permission_required_for_api, login_required_for_api


class UserList(Resource):

    def get(self):
        pass


class UserManage(Resource):

    def get(self, id):
        pass

    def post(self):
        pass

    @login_required_for_api
    def put(self, id):
        pass

    @login_required_for_api
    @permission_required_for_api(9)
    def delete(self, id):
        pass


class UserOperation(Resource):
    @login_required_for_api
    @permission_required_for_api(9)
    def get(self, operation, id):
        pass
