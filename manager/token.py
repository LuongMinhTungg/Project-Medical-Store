from functools import wraps

import jwt
from flask import request, jsonify, url_for, redirect, render_template

from manager.config import app
from manager.model.model import ManagerUser, Customer


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            bearer = request.headers['Authorization']
            token = bearer.split(' ')[1]
        '''if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']'''
        if request.cookies.get('token'):
            token = request.cookies.get('token')
        if not token:
            if request.headers.get('User-Agent')=='PostmanRuntime/7.29.0':
                return 'not login', 404
            return redirect(url_for('managers.login'))
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = ManagerUser.query.filter_by(username=data['username']).first()
        except Exception:
            if request.headers.get('User-Agent') == 'PostmanRuntime/7.29.0':
                return 'wrong token', 404
            else:
                resp = redirect(url_for('indexs.index'))
                resp.set_cookie('token',value='')
                return resp
        return func(current_user, *args, **kwargs)
    return decorated

def check_permiss(role):
    def f(func):
        @wraps(func)
        def check(current_user, *args, **kwargs):
            try:
                if current_user.role.name in role:
                    return func(current_user, *args, **kwargs)
                if request.headers.get('User-Agent')=='PostmanRuntime/7.29.0':
                    return 'not role', 410
                return render_template('error_not_role.html', current_user=current_user)
            except AttributeError:
                if request.headers.get('User-Agent')=='PostmanRuntime/7.29.0':
                    return 'not login', 404
                return redirect(url_for('managers.login'))
        return check
    return f

def token_customer_required(func):
    @wraps(func)
    def decorated_customer(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            bearer = request.headers['Authorization']
            token = bearer.split(' ')[1]
        if request.cookies.get('token_customer'):
            token = request.cookies.get('token_customer')
        if not token:
            if request.headers.get('User-Agent')=='PostmanRuntime/7.29.0':
                return 'not login', 404
            return redirect(url_for('customers.login_customer'))
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_customer = Customer.query.filter_by(username=data['username']).first()
        except Exception:
            if request.headers.get('User-Agent')=='PostmanRuntime/7.29.0':
                return 'not login', 404
            else:
                resp = redirect(url_for('indexs.index_customer'))
                resp.set_cookie('token_customer', value='')
                return resp

        return func(current_customer, *args, **kwargs)
    return decorated_customer
