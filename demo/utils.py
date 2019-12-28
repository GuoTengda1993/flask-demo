# -*- coding: utf-8 -*-
from functools import wraps
try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, current_app
from flask_login import current_user


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def permission_required_for_api(role):
    def decorator(func):
        @wraps(func)
        def decorator_function(*args, **kwargs):
            if not current_user.can(role):
                _response = {
                    'code': 401,
                    'res': '',
                    'msg': '账户没有权限'
                }
                return _response, 401
            return func(*args, **kwargs)
        return decorator_function
    return decorator


def login_required_for_api(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            _response = {
                'code': 211,
                'msg': '登录超时，请重新登录',
                'res': ''
            }
            return _response, 211
        return func(*args, **kwargs)
    return decorated_view
