# -*- coding: utf-8 -*-
from flask_restful import Resource
from demo.utils import permission_required_for_api, login_required_for_api


class AboutPage(Resource):

    def get(self):
        pass

    @login_required_for_api
    @permission_required_for_api(9)
    def put(self):
        pass
