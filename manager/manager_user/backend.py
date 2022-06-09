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
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        if V.vali_login(data) == True:
            username = data['username']
            password = data['password']
            user = ManagerUser.query.filter_by(username=username).first()
            if not user:
                flash('not username')
                return 'none', 404
            if check_password_hash(user.password, password):
                session['logged_in'] = True
                token = jwt.encode(
                    {'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                    app.config['SECRET_KEY'])
                return token
            flash('wrong password')
            return 'wrong password', 404
        return V.vali_login(data), 404

    def register(self):
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        if V.vali_register_user(data) == True:
            role = Role.query.filter_by(name=data['role']).first()
            if not role:
                return 'none role', 410
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
                    flash('add')
                    return 'add', 201
                return 'wrong cf_pw', 404
            flash('username is existed')
            return 'username existed', 409
        flash(V.vali_register_user(data))
        return V.vali_register_user(data)

    def reset_password(self,username):
        user = ManagerUser.query.filter_by(username=username).first()
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        if V.vali_reset_password_user(data) == True:
            if user:
                if check_password_hash(user.password,data['old_password']):
                    if check_password_hash(user.password, data['new_password']):
                        flash('old password = new password')
                        return 'old password = new password', 404
                    hashed_pw = generate_password_hash(data['new_password'], method='sha256')
                    if check_password_hash(hashed_pw,data['confirm_password']):
                        user.password = hashed_pw
                        db.session.commit()
                        flash('success')
                        return 'reset', 202
                    return 'wrong cf_pw', 404
                flash('wrong password')
                return 'wrong password', 404
            flash('user not existed')
            return 'user not existed', 404
        return V.vali_reset_password_user(data)

    def change_password(self):
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        username = data['username']
        user = ManagerUser.query.filter_by(username=username).first()
        data = request.form
        if V.vali_change_password_user(data) == True:
            if user:
                if check_password_hash(user.password, data['old_password']):
                    if check_password_hash(user.password, data['new_password']):
                        flash('old password = new password')
                        return 'old password = new password', 404
                    hashed_pw = generate_password_hash(data['new_password'], method='sha256')
                    if check_password_hash(hashed_pw, data['confirm_password']):
                        user.password = hashed_pw
                        db.session.commit()
                        flash('success')
                        return 'reset', 202
                    return 'wrong cf_pw', 404
                flash('wrong password')
                return 'wrong password', 404
            flash('user not existed')
            return 'user not existed', 404
        return V.vali_change_password_user(data)


    def get_user(self,current_user, username):
        user = ManagerUser.query.filter_by(username=username).first()
        if current_user.role.name == 'manager' and username.role.name == 'admin':
            return 'not role', 404
        elif current_user.role.name == 'staff' and user.role.name in ['admin', 'manager']:
            return 'not role', 404
        else:
            if user:
                item = {'name':user.name,'username':user.username,'role':user.role.name,'phone':user.phone,'join_date':user.join_date}
                return item
            return user

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

    def del_user(self,current_user, username):
        user = ManagerUser.query.filter_by(username=username).first()
        if user:
            try:
                if current_user.role.name == 'manager' and user.role.name == 'admin':
                    return 'not role', 404
                else:
                    db.session.delete(user)
                    db.session.commit()
                    flash('delete')
                    return 'delete', 204
            except IndentationError:
                db.session.rollback()
                flash('cant delete')
                return jsonify({"message": "Can not delete user!"}), 400
        flash('not found user')
        return 'not found user', 404

    def update_user_admin(self,username):
        user = ManagerUser.query.filter_by(username=username).first()
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        role = Role.query.filter_by(name=data['role']).first()
        if not role:
            return 'none role', 410
        if V.vali_update_user_admin(data):
            if user:
                user.name = data['name']
                user.role_id = role.id
                user.phone = data['phone']
                db.session.commit()
                flash('update')
                return 'update', 202
            flash('none')
            return 'none', 404
        return V.vali_update_user_admin(data)

    def update_user(self,current_user,username):
        user = ManagerUser.query.filter_by(username=username).first()
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        role = Role.query.filter_by(name=data['role']).first()
        if not role:
            return 'none role', 404
        if user:
            if current_user.role.name == 'manager' and user.role.name != 'admin':
                if role.name == 'admin':
                    return 'not role', 404
                if V.vali_update_user(data):
                    user.name = data['name']
                    user.role_id = role.id
                    user.phone = data['phone']
                    db.session.commit()
                    return 'update', 202
                return V.vali_update_user(data)
            if current_user.role.name == 'admin':
                return self.update_user_admin(username)
            return 'not role', 404
        return 'not found', 404

    def insert_user(self,current_user):
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        if current_user.role.name == 'admin':
            return self.register()
        else:
            if V.vali_register_user_manager(data):
                username = data['username']
                user = ManagerUser.query.filter_by(username=username).first()
                role = Role.query.filter_by(name=data['role']).first()
                if not role:
                    flash('none role')
                    return 'none role', 404
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
                        flash('add')
                        return 'add', 201
                    return 'wrong cf_pw', 404
                flash('username is existed')
                return 'username is existed', 409
            flash(V.vali_register_user(data))
            return V.vali_register_user(data)


    def search_user_by_username(self):
        user = self.get_all_user()
        output = {}
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        search_data = data['search']
        c=1
        if user:
            for i in user.values():
                if search_data in i['name']:
                    item = {'name': i['name'], 'username': i['username'], 'role': i['role'], 'phone': i['phone'],
                            'join_date': i['join_date']}
                    output[c] = item
                    c = c+1
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
        c = request.headers.get('Content-Type')
        if c == 'application/json':
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
                flash('add')
                return 'add', 201
            flash('role is existed')
            return 'role is existed', 409
        return V.vali_insert_role(data)

    def update_role(self,role_id):
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        role = Role.query.filter_by(id=role_id).first()
        if role:
            if role_id == '1':
                return 'cant update role admin', 404
            if V.vali_insert_role(data) == True:
                role.name = data['name']
                db.session.commit()
                flash('update')
                return 'update', 202
            return V.vali_insert_role(data)
        flash('not found')
        return 'not found', 404


    def delete_role(self, role_id):
        role = Role.query.filter_by(id=role_id).first()
        if role:
            try:
                if role_id == '1':
                    flash('cant delete role admin')
                    return 'cant delete role admin', 404
                db.session.delete(role)
                db.session.commit()
                flash('delete')
                return 'delete', 204
            except:
                db.session.rollback()
                flash('role is used, cant delete')
                return 'role is used, cant delete', 404
        flash('not found')
        return 'not found', 404

