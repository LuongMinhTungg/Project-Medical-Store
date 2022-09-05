from flask import Flask, jsonify, request, Response, make_response, render_template, session, Blueprint
from manager.token import token_customer_required
from manager.customer.services import ManagementCustomer as MC
MC =MC()

customers = Blueprint('customers',__name__)



@customers.route('/customer/login', methods = ['POST','GET'])
def login_customer():
    return MC.login()

@customers.route('/customer/logout')
def logout_customer():
    return MC.logout()

@customers.route('/customer/register', methods = ['POST','GET'])
def register_customer():
    return MC.register()

@customers.route('/customer/change_password', methods=['POST', 'GET'])
def change_password():
    return MC.change_password()

@customers.route('/customer/reset-password', methods=['POST','GET'])
@token_customer_required
def reset_password_customer(current_customer):
    return MC.reset_password(current_customer, current_customer.username)

@customers.route('/customer/customer-account', methods=['POST','GET'])
@token_customer_required
def customer_account(current_customer):
    return MC.get_customer(current_customer, current_customer.username)

