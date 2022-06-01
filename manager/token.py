from functools import wraps

import jwt
from flask import request, jsonify, url_for, redirect, render_template

from manager.config import app
from manager.model.model import ManagerUser, Customer


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if request.cookies.get('token'):
            token = request.cookies.get('token')
        if not token:
            return redirect(url_for('managers.login'))
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = ManagerUser.query.filter_by(username=data['username']).first()
        except:
            if 'x-access-token' in request.headers:
                return 'not login'
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
                try:
                    return render_template('error_not_role.html', current_user=current_user)
                except:
                    return 'not role'
            except AttributeError:
                return redirect(url_for('managers.login'))
        return check
    return f

def token_customer_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if request.cookies.get('token'):
            token = request.cookies.get('token')
        if not token:
            return redirect(url_for('customers.login_customer'))
        try:

            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_customer = Customer.query.filter_by(username=data['username']).first()
        except:
            if 'x-access-token' in request.headers:
                return 'not login'
            else:
                resp = redirect(url_for('indexs.index'))
                resp.set_cookie('token', value='')
                return resp

        return func(current_customer, *args, **kwargs)
    return decorated