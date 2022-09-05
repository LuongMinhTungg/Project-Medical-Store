from flask import Flask, jsonify, request, Response, make_response, render_template, session, Blueprint, url_for, redirect
from manager.token import token_required, check_permiss
from manager.manager_user.services import ManagementUser

MU = ManagementUser()

managers = Blueprint('managers', __name__)


@managers.route('/insert-user',methods = ['GET','POST'])
@token_required
@check_permiss(['admin','manager'])
def insert_user(current_user):
    return MU.insert_user(current_user)

@managers.route('/register', methods = ['POST','GET'])
def register():
    return MU.register()

@managers.route('/del-user/<username>',methods = ['GET'])
@token_required
@check_permiss(['admin', 'manager'])
def del_user(current_user,username):
    return MU.del_user(current_user, username)

@managers.route('/change-user-password', methods=['GET','POST'])
def change_password():
    return MU.change_password()

@managers.route('/logout')
def logout():
    return MU.logout()

@managers.route('/login',methods = ['POST', 'GET'])
def login():
    return MU.login()

@managers.route('/get-account',methods = ['GET','POST'])
@token_required
def get_account(current_user):
    return MU.get_user(current_user,current_user.username)

@managers.route('/update-user/<username>', methods = ['POST','GET'])
@token_required
@check_permiss(['admin','manager'])
def update_user(current_user, username):
    return MU.update_user(current_user,username)

@managers.route('/get-all-user/<page_num>',methods = ['GET','POST'])
@token_required
@check_permiss(['admin', 'manager', 'staff'])
def get_all_user(current_user,page_num):
    return MU.get_all_user(current_user, page_num)

@managers.route('/search-user/<page_num>', methods=['GET','POST'])
@token_required
def search_user(current_user, page_num):
    return MU.search_user(current_user, page_num)

@managers.route('/get-user/<username>',methods = ['GET','POST'])
@token_required
def get_user(current_user,username):
    return MU.get_user(current_user,username)

@managers.route('/reset-password',methods = ['GET','POST'])
@token_required
def reset_password(current_user):
    return MU.reset_password(current_user,current_user.username)

@managers.route('/get-all-role')
@token_required
@check_permiss(['admin'])
def get_all_role(current_user):
    try:
        return MU.get_all_role(current_user)
    except AttributeError:
        return redirect(url_for('managers.login'))

@managers.route('/insert-role', methods=['POST','GET'])
@token_required
@check_permiss(['admin'])
def insert_role(current_user):
    return MU.insert_role(current_user)

@managers.route('/update-role/<role_id>', methods=['POST','GET'])
@token_required
@check_permiss(['admin'])
def update_role(current_user,role_id):
    return MU.update_role(current_user,role_id)


@managers.route('/delete-role/<role_id>', methods=['POST','GET'])
@token_required
@check_permiss(['admin'])
def delete_role(current_user,role_id):
    return MU.delete_role(current_user,role_id)


