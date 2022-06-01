import datetime
from manager.config import app
from manager.extension import db
from manager.model.model import ManagerUser, Role
from flask import Flask, jsonify, request, Response, make_response, render_template, session, Blueprint, flash, redirect, url_for
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from manager.manager_user.validate import Validate as V

V=V()
class BackEndManagerUser:
    def login(self):
        if 'x-access-token' in request.headers:
            data = request.json
        else:
            data = request.form
        username = data['username']
        password = data['password']
        user = ManagerUser.query.filter_by(username=username).first()
        if V.vali_login(data) == True:
            if not user:
                flash('none')
                return 'none'
            if check_password_hash(user.password, password):
                session['logged_in'] = True
                token = jwt.encode(
                    {'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                    app.config['SECRET_KEY'])
                return token
            return 'wrong password'
        return V.vali_login(data)

    def register(self):
        if 'x-access-token' in request.headers:
            data = request.json
        else:
            data = request.form
        if V.vali_register_user(data) == True:
            role = Role.query.filter_by(name=data['role']).first()
            if not role:
                return 'none role'
            hashed_pw = generate_password_hash(data['password'], method='sha256')
            cf_pw = data['confirm_password']
            username = data['username']
            user = ManagerUser.query.filter_by(username=username).first()
            if not user:
                if check_password_hash(hashed_pw,cf_pw):
                    new_user = ManagerUser(name=data['name'], username=data['username'],
                                           password=hashed_pw, role_id=role.id,
                                           phone=data['phone'])
                    db.session.add(new_user)
                    db.session.commit()
                    return 'add', 201
                return 'wrong cf_pw'
            return 'username existed'
        return V.vali_register_user(data)

    def reset_password(self,username):
        user = ManagerUser.query.filter_by(username=username).first()
        if 'x-access-token' in request.headers:
            data = request.json
        else:
            data = request.form
        if V.vali_reset_password_user(data) == True:
            if user:
                if check_password_hash(user.password,data['old_password']):
                    hashed_pw = generate_password_hash(data['new_password'], method='sha256')
                    if check_password_hash(hashed_pw,data['confirm_password']):
                        user.password = hashed_pw
                        db.session.commit()
                        return 'reset', 202
                    return 'wrong cf_pw'
                return 'wrong password'
            return 'user not existed'
        return V.vali_reset_password_user(data)

    def change_password(self):
        if 'x-access-token' in request.headers:
            data = request.json
        else:
            data = request.form
        username = data['username']
        user = ManagerUser.query.filter_by(username=username).first()
        data = request.form
        if V.vali_change_password_user(data) == True:
            if user:
                if check_password_hash(user.password, data['old_password']):
                    hashed_pw = generate_password_hash(data['new_password'], method='sha256')
                    if check_password_hash(hashed_pw, data['confirm_password']):
                        user.password = hashed_pw
                        db.session.commit()
                        return 'reset', 202
                    return 'wrong cf_pw'
                return 'wrong password'
            return 'user not existed'
        return V.vali_change_password_user(data)


    def get_user(self, username):
        user = ManagerUser.query.filter_by(username=username).first()
        if user:
            item = {'name':user.name,'username':user.username,'role':user.role.name,'phone':user.phone,'join_date':user.join_date}
            return item
        return 'none'

    def get_all_user(self):
        user = ManagerUser.query.all()
        output = {}
        if user:
            for i in user:
                item = {'name': i.name, 'username': i.username, 'role': i.role.name, 'phone': i.phone,
                        'join_date': i.join_date}
                output[i.id] = item
            return output
        return output

    def del_user(self,username):
        user = ManagerUser.query.filter_by(username=username).first()
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                return 'delete'
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not delete user!"}), 400

    def update_user_admin(self,username):
        user = ManagerUser.query.filter_by(username=username).first()
        if 'x-access-token' in request.headers:
            data = request.json
        else:
            data = request.form
        role = Role.query.filter_by(name=data['role']).first()
        if not role:
            return 'none role'
        if V.vali_update_user_admin(data):
            if user:
                user.name = data['name']
                user.role_id = role.id
                user.phone = data['phone']
                db.session.commit()
                return 'update', 202
            return 'none'
        return V.vali_update_user_admin(data)

    def update_user(self,current_user,username):
        user = ManagerUser.query.filter_by(username=username).first()
        if 'x-access-token' in request.headers:
            data = request.json
        else:
            data = request.form
        role = Role.query.filter_by(name=data['role']).first()
        if not role:
            return 'none role'
        if user:
            if current_user.role.name == 'manager' and user.role.name != 'admin':
                if V.vali_update_user(data):
                    user.name = data['name']
                    user.role_id = role.id
                    user.phone = data['phone']
                    db.session.commit()
                    return 'update', 202
                return V.vali_update_user(data)
            if current_user.role.name == 'admin':
                return self.update_user_admin(username)
        return user

    def insert_user(self,current_user):
        if 'x-access-token' in request.headers:
            data = request.json
        else:
            data = request.form
        if current_user.role.name == 'admin':
            self.register()
        else:
            if V.vali_register_user_manager(data):
                username = data['username']
                user = ManagerUser.query.filter_by(username=username).first()
                role = Role.query.filter_by(name=data['role']).first()
                if not role:
                    return 'none role'
                hashed_pw = generate_password_hash(data['password'], method='sha256')
                cf_pw = data['confirm_password']
                username = data['username']
                user = ManagerUser.query.filter_by(username=username).first()
                if not user:
                    if check_password_hash(hashed_pw, cf_pw):
                        new_user = ManagerUser(name=data['name'], username=data['username'],
                                               password=hashed_pw, role_id=role.id,
                                               phone=data['phone'])
                        db.session.add(new_user)
                        db.session.commit()
                        return 'add', 201
                    return 'wrong cf_pw'
                return 'username existed'
            return V.vali_register_user(data)


    def search_user_by_username(self):
        user = self.get_all_user()
        output = {}
        if 'x-access-token' in request.headers:
            data = request.json
        else:
            data = request.form
        search_data = data['search']
        if user:
            for i in user.values():
                if search_data in i['name']:
                    item = {'name': i['name'], 'username': i['username'], 'role': i['role'], 'phone': i['phone'],
                            'join_date': i['join_date']}
                    output[i['id']] = item
            return output
        return output

    def get_all_role(self):
        role = Role.query.all()
        output = {}
        if role:
            for i in role:
                item = {'id':i.id, 'name': i.name}
                output[i.id] = item
            return output
        return output

    def insert_role(self):
        if 'x-access-token' in request.headers:
            data = request.json
        else:
            data = request.form
        if V.vali_insert_role(data) == True:
            name = data['name']
            role = Role.query.filter_by(name=name).first()
            if not role:
                new_role = Role(name=name)
                db.session.add(new_role)
                db.session.commit()
                return 'add', 201
            return 'role is existed'
        return V.vali_insert_role(data)

    def update_role(self,role_id):
        if 'x-access-token' in request.headers:
            data = request.json
        else:
            data = request.form
        role = Role.query.filter_by(id=role_id).first()
        if role:
            if V.vali_insert_role(data) == True:
                role.name = data['name']
                db.session.commit()
            return V.vali_insert_role(data)
        return role



