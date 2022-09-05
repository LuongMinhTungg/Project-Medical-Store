import datetime
from manager.config import app
from manager.extension import db
from manager.model.model import ManagerUser
from flask import Flask, jsonify, request, Response, make_response, render_template, session, Blueprint, flash, redirect, url_for
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from manager.manager_user.backend import BackEndManagerUser
from manager.customer.backend import BackEndCustomer
from manager.medical.backend import BackEndMedical
from manager.bill.backend import BackEndBill
from manager.token import token_required, token_customer_required, check_permiss
from manager.manager_user.validate import Validate as V

V = V()
postmans = Blueprint('postmans', __name__)


@postmans.route('/backend/user/login',methods = ['POST'])
def login_user():
    return BackEndManagerUser().login()

@postmans.route('/backend/user/register',methods = ['POST'])
def register_user():
    return BackEndManagerUser().register()

@postmans.route('/backend/user/change-password', methods=['POST'])
def change_password():
    return BackEndManagerUser().change_password()


@postmans.route('/backend/user/update-account', methods=['PUT'])
@token_required
def update_account_user(current_user):
    return BackEndManagerUser().update_user(current_user, current_user.username)

@postmans.route('/backend/user/reset-password/<username>', methods=['PUT'])
@token_required
def reset_password_user(current_user, username):
    return BackEndManagerUser().reset_password(username)

@postmans.route('/backend/user/get/<username>',methods = ['GET'])
@token_required
def get_user(current_user,username):
    return BackEndManagerUser().get_user(current_user,username)

@postmans.route('/backend/user/get-all',methods = ['GET'])
@token_required
@check_permiss(['admin','manager'])
def get_all_user(current_user):
    return BackEndManagerUser().get_all_user()

@postmans.route('/backend/user/get-page/<page_num>', methods=['GET'])
@token_required
@check_permiss(['admin', 'manager'])
def get_user_by_page(current_user, page_num):
    return BackEndManagerUser().get_user_by_page(page_num)


@postmans.route('/backend/user/get-account', methods=['GET'])
@token_required
def get_account_user(current_user):
    return BackEndManagerUser().get_user(current_user,current_user.username)

@postmans.route('/backend/user/insert', methods=['POST'])
@token_required
@check_permiss(['admin', 'manager'])
def insert_user(current_user):
    return BackEndManagerUser().insert_user(current_user)

@postmans.route('/backend/user/delete/<username>', methods=['DELETE'])
@token_required
@check_permiss(['admin', 'manager'])
def delete_user(current_user, username):
    return BackEndManagerUser().del_user(current_user, username)

@postmans.route('/backend/user/update/<username>', methods=['PUT'])
@token_required
@check_permiss(['admin','manager'])
def update_user(current_user,username):
    return BackEndManagerUser().update_user(current_user,username)

@postmans.route('/backend/user/search/<page_num>',methods=['POST', 'GET'])
@token_required
def search_user(current_user, page_num):
    return BackEndManagerUser().search_user_by_username(page_num)

@postmans.route('/backend/user/insert-role',methods=['POST'])
@token_required
@check_permiss(['admin'])
def insert_role(current_user):
    return BackEndManagerUser().insert_role()


@postmans.route('/backend/user/delete-role/<role_id>', methods=['DELETE'])
@token_required
@check_permiss(['admin'])
def delete_role(current_user, role_id):
    return BackEndManagerUser().delete_role(role_id)

@postmans.route('/backend/user/update-role/<role_id>', methods=['PUT'])
@token_required
@check_permiss(['admin'])
def update_role(current_user,role_id):
    return BackEndManagerUser().update_role(role_id)


@postmans.route('/backend/user/get=all-role', methods=['GET'])
@token_required
@check_permiss(['admin'])
def get_all_role(current_user):
    return BackEndManagerUser().get_all_role()

@postmans.route('/backend/customer/login', methods=['POST'])
def login_customer():
    return BackEndCustomer().login_customer()

@postmans.route('/backend/customer/register',methods=['POST'])
def register_customer():
    return BackEndCustomer().register_customer()

@postmans.route('/backend/customer/reset-password/<username>', methods=['PUT'])
@token_customer_required
def reset_password_customer(current_customer,username):
    return BackEndCustomer().reset_password_customer(username)

@postmans.route('/backend/customer/change-password', methods=['POST'])
def change_password_customer():
    return BackEndCustomer().change_password()

@postmans.route('/backend/customer/update-account', methods=['PUT'])
@token_customer_required
def update_customer_account(current_customer):
    return BackEndCustomer().update_customer_account(current_customer.username)

@postmans.route('/backend/customer/get-account',methods=['GET'])
@token_customer_required
def get_customer_account(current_customer):
    return BackEndCustomer().get_account_customer(current_customer.username)

@postmans.route('/backend/medical/show-all')
def show_all_medical():
    return BackEndMedical().show_all_medical()

@postmans.route('/backend/medical/show-all/<page_num>')
def show_all_medical_page(page_num):
    return BackEndMedical().show_all_medical_page(page_num)

@postmans.route('/backend/medical/show/<medical_id>')
def show_medical(medical_id):
    return BackEndMedical().show_medical(medical_id)

@postmans.route('/backend/medical/insert',methods=['POST'])
@token_required
def insert_medical(current_user):
    return BackEndMedical().insert_medical()

@postmans.route('/backend/medical/delete/<medical_id>',methods=['DELETE'])
@token_required
def delete_medical(current_user,medical_id):
    return BackEndMedical().delete_medical(medical_id)

@postmans.route('/backend/medical/update/<medical_id>',methods=['PUT'])
@token_required
def update_medical(current_user,medical_id):
    return BackEndMedical().update_medical(medical_id)

@postmans.route('/backend/medical/search', methods=['POST'])
@token_required
def search_medical(current_user):
    return BackEndMedical().search_medical_by_name()

@postmans.route('/backend/medical-type/show-all')
@token_required
def show_all_medical_type(current_user):
    return BackEndMedical().show_all_medical_type()

@postmans.route('/backend/medical-type/show-all/<page_num>')
@token_required
def show_all_medical_type_page(current_user, page_num):
    return BackEndMedical().show_medical_type_page(page_num)

@postmans.route('/backend/medical-type/show/<medical_type_id>')
@token_required
def show_medical_type(current_user,medical_type_id):
    return BackEndMedical().show_medical_type(medical_type_id)

@postmans.route('/backend/medical-type/insert',methods=['POST'])
@token_required
def insert_medical_type(current_user):
    return BackEndMedical().insert_medical_type()

@postmans.route('/backend/medical-type/update/<medical_type_id>',methods=['PUT'])
@token_required
def update_medical_type(current_user, medical_type_id):
    return BackEndMedical().update_medical_type(medical_type_id)

@postmans.route('/backend/medical-type/delete/<medical_type>',methods=['DELETE'])
@token_required
def del_medical_type(current_user, medical_type):
    return BackEndMedical().delete_medical_type(medical_type)

@postmans.route('/backend/medical-type/search', methods=['POST'])
@token_required
def search_medical_type(current_user):
    return BackEndMedical().search_medical_type_by_name()


@postmans.route('/backend/bill/order-medical',methods=['POST'])
@token_customer_required
def order_medical(current_customer):
    return BackEndBill().order_medical(current_customer)

@postmans.route('/backend/cart/add',methods=['POST'])
@token_customer_required
def add_to_cart(current_customer):
    return BackEndBill().add_to_cart(current_customer)

@postmans.route('/backend/cart/show',methods=['GET'])
@token_customer_required
def show_cart(current_customer):
    return BackEndBill().show_cart(current_customer)

@postmans.route('/backend/cart/delete-one/<medical_id>',methods=['DELETE'])
@token_customer_required
def delete_one_in_cart(current_customer,medical_id):
    return BackEndBill().delete_one_in_cart(current_customer, medical_id)

@postmans.route('/backend/cart/update/<medical_id>', methods=['PUT'])
@token_customer_required
def update_cart(current_customer, medical_id):
    return BackEndBill().update_cart(current_customer,medical_id)

@postmans.route('/backend/bill/show-all/<page_num>', methods=['GET'])
@token_required
def show_all_bill(current_user, page_num):
    return BackEndBill().show_bill(page_num)

@postmans.route('/backend/bill/show-bill-detail/<bill_id>', methods=['GET'])
@token_required
def show_bill_detail(current_user,bill_id):
    return BackEndBill().show_bill_detail(bill_id)

@postmans.route('/backend/customer/bill/show/<page_num>', methods=['GET'])
@token_customer_required
def show_bill_customer(current_customer,page_num):
    return BackEndBill().show_bill_customer(current_customer.id,page_num)
