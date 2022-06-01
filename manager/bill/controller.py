from flask import Flask, jsonify, request, Response, make_response, render_template, session, Blueprint
from manager.token import token_customer_required, token_required
from manager.bill.services import ManagementBill as MB
MB = MB()

bills = Blueprint('bills',__name__)

@bills.route('/cart/show', methods = ['POST', 'GET'])
@token_customer_required
def show_cart(current_customer):
    return MB.show_cart(current_customer)

@bills.route('/cart/add/', methods = ['POST','GET'])
@token_customer_required
def add_to_cart(current_customer):
    return MB.add_to_cart(current_customer)

@bills.route('/cart/check-info/<medical_id>', methods=['GET','POST'])
@token_customer_required
def check_info(current_customer, medical_id):
    return MB.check_form(current_customer, medical_id)

@bills.route('/cart/order-medical', methods= ['POST','GET'])
@token_customer_required
def order_medical(current_customer):
    return MB.order_medical(current_customer)

@bills.route('/bill/show-all', methods=['POST','GET'])
@token_required
def show_all_bill(current_customer):
    return MB.show_all_bill(current_customer)


@bills.route('/bill/show-bill-detail/<bill_id>', methods=['POST','GET'])
@token_required
def show_bill_detail(current_user, bill_id):
    return MB.show_bill_detail(current_user,bill_id)


@bills.route('/customer/bill/show', methods=['POST','GET'])
@token_customer_required
def show_bill_customer(current_customer):
    return MB.show_bill_customer(current_customer, current_customer.id)


@bills.route('/customer/bill/show-bill-detail/<bill_id>', methods=['POST','GET'])
@token_customer_required
def show_bill_detail_customer(current_customer,bill_id):
    return MB.show_bill_detail_customer(current_customer,bill_id)


@bills.route('/cart/delete/<medical_id>', methods=['POST','GET'])
@token_customer_required
def delete_one_cart(current_customer, medical_id):
    return MB.delete_one_cart(current_customer,medical_id)


@bills.route('/cart/clear', methods=['POST','GET'])
@token_customer_required
def clear_cart(current_customer):
    return MB.clear_cart(current_customer)


@bills.route('/cart/update/<medical_id>', methods=['POST','GET'])
@token_customer_required
def update_cart(current_customer, medical_id):
    return MB.update_cart(current_customer, medical_id)
