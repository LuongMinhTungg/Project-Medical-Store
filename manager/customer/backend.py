import datetime
from manager.config import app
from manager.extension import db
from manager.model.model import Customer
from flask import Flask, jsonify, request, Response, make_response, render_template, session, Blueprint, flash, redirect, url_for
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from manager.customer.validate import Validate as V

V=V()
class BackEndCustomer:
    def login_customer(self):
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        username = data['username']
        password = data['password']
        if V.vali_login_customer(data):
            customer = Customer.query.filter_by(username=username).first()
            if not customer:
                flash('none')
                return 'none', 404
            if check_password_hash(customer.password, password):
                session['logged_in'] = True
                token = jwt.encode(
                    {'username': customer.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                    app.config['SECRET_KEY'])
                return token
            flash('wrong password or username')
            return 'wrong password or username'
        return V.vali_login_customer(data)

    def register_customer(self):
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        if V.vali_register_customer(data) == True:
            password = data['password']
            hashed_pw = generate_password_hash(password, method='sha256')
            username = data['username']
            customer = Customer.query.filter_by(username=username).first()
            if not customer:
                if check_password_hash(hashed_pw,data['confirm_password']):
                    new_customer = Customer(name=data['name'], username=username,
                                            password=hashed_pw, address=data['address'],
                                            phone=data['phone'])
                    db.session.add(new_customer)
                    db.session.commit()
                    flash('add')
                    return 'add', 201
                return 'wrong cf_pw', 404
            flash('username existed')
            return 'username existed', 409
        return V.vali_register_customer(data)

    def change_password(self):
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        username = data['username']
        user = Customer.query.filter_by(username=username).first()
        data = request.form
        if V.vali_change_password_customer(data) == True:
            if user:
                if check_password_hash(user.password, data['old_password']):
                    if check_password_hash(user.password, data['new_password']):
                        return 'old password = new password', 404
                    hashed_pw = generate_password_hash(data['new_password'], method='sha256')
                    if check_password_hash(hashed_pw, data['confirm_password']):
                        user.password = hashed_pw
                        db.session.commit()
                        return 'reset', 202
                    return 'wrong cf_pw', 404
                return 'wrong password', 404
            return 'user not existed', 404
        return V.vali_change_password_customer(data)

    def reset_password_customer(self, username):
        customer = Customer.query.filter_by(username=username).first()
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        if customer:
            if check_password_hash(customer.password,data['old_password']):
                if check_password_hash(customer.password, data['new_password']):
                    flash('old password = new password')
                    return 'old password = new password', 404
                hashed_pw = generate_password_hash(data['new_password'], method='sha256')
                if check_password_hash(hashed_pw,data['confirm_password']):
                    customer.password = hashed_pw
                    db.session.commit()
                    flash('success')
                    return 'reset', 202
                return 'wrong cf_pw', 404
            flash('wrong password')
            return 'wrong password', 404
        flash('customer not existed')
        return 'customer not existed', 404

    def update_customer_account(self, username):
        customer = Customer.query.filter_by(username=username).first()
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        if customer:
            customer.name = data['name']
            customer.phone = data['phone']
            customer.address = data['address']
            db.session.commit()
            flash('update')
            return 'update', 202
        flash('none')
        return 'none', 404

    def get_account_customer(self, username):
        customer = Customer.query.filter_by(username=username).first()
        if customer:
            item = {'name':customer.name, 'username':customer.username, 'address':customer.address, 'phone':customer.phone, 'join_date':customer.join_date}
            return item
        return {}