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

@customers.route('/customer/reset-password/<username>', methods=['POST','GET'])
@token_customer_required
def reset_password_customer(current_customer,username):
    return MC.reset_password(current_customer, username)

@customers.route('/customer/customer-account/<username>', methods=['POST','GET'])
@token_customer_required
def customer_account(current_customer,username):
    return MC.get_customer(current_customer, username)

@customers.route('/create_bill/<int:customer_id>', methods = ['Get'])
def create_bill(customer_id):
    return MC.create_bill(customer_id)

@customers.route('/delete_medical_billdetail/<int:medical_id>', methods = ['DELETE'])
def delete_medical_billdetail(medical_id):
    return MC.del_medical_billdetail(medical_id)