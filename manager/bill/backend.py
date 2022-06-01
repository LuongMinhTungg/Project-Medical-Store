import datetime

import pm as pm

from requests import Session

from manager.config import app
from manager.extension import db
from manager.model.model import Medical,MedicalType, Bill, BillDetail, Customer
from flask import Flask, jsonify, request, Response, make_response, render_template, session, Blueprint, flash, redirect, url_for
from manager.bill.validate import Validate as V
V = V()

cart_session = session

class BackEndBill():
    def create_bill(self, customer_id):
        customer = Customer.query.filter_by(id=customer_id).first()
        if customer:
            new_bill = Bill(customer_id=customer_id)
            db.session.add(new_bill)
            db.session.commit()
            item = {'id':new_bill.id, 'customer_name': new_bill.customer.name, 'customer_username': new_bill.customer.username,
                    'status': new_bill.status, 'added_on': new_bill.added_on}
            return item
        return 'none'

    def order_medical(self,current_customer):
        cart_name = current_customer.username
        cart = session[cart_name]
        if not cart:
            return 'cart is empty'
        else:
            new_bill = self.create_bill(current_customer.id)
            for i,j in cart.items():
                medical_id, count = i, j['count']
                self.add_on_bill_detail(new_bill['id'],medical_id,int(count))
            session[cart_name] = {}
            return 'add', 201


    def add_on_bill_detail(self,bill_id,medical_id,count):
        medical = Medical.query.get(medical_id)
        bill_detail = BillDetail.query.filter_by(bill_id=bill_id,medical_id=medical_id).first()
        if medical.count >= int(count):
            if not bill_detail:
                new_bill_detail = BillDetail(bill_id=bill_id, medical_id=medical_id,count=count)
                db.session.add(new_bill_detail)
                self.decrease_count(medical_id,count)
                db.session.commit()
            else:
                self.increase_count(bill_id, medical_id, count)
                self.decrease_count(medical_id, count)
            return 'add', 201
        return 'none'

    def del_medical_billdetail(self, medical_id):
        medical = BillDetail.query.get(medical_id)
        if medical:
            try:
                BillDetail.remove(medical)
                db.session.commit()
                return "User Deleted"
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not delete medical!"}), 400
        else:
            return "Not found medical"

    def decrease_count(self, medical_id,count):
        medical = Medical.query.filter_by(id=medical_id).first()
        medical.count = medical.count - count
        db.session.commit()
        return 'decrease'

    def increase_count(self, bill_id, medical_id, count):
        bill_detail = BillDetail.query.filter_by(bill_id=bill_id, medical_id=medical_id).first()
        bill_detail.count = bill_detail.count + count
        db.session.commit()
        return 'increase'

    def show_bill(self):
        all_bill = Bill.query.all()
        output = {}
        if all_bill:
            for i in all_bill:
                item = {'id': i.id, 'customer': i.customer.username, 'status': i.status,
                        'added_on': i.added_on}
                output[i.id] = item
            return output
        return output

    def show_bill_customer(self, customer_id):
        bill = Bill.query.filter_by(customer_id=customer_id).all()
        output = {}
        c = 1
        if bill:
            for i in bill:
                item = {'id': i.id, 'customer': i.customer.username, 'status': i.status,
                        'added_on': i.added_on}
                output[c] = item
                c = c+1
            return output
        return output

    def show_bill_detail(self, bill_id):
        bill_detail = BillDetail.query.filter_by(bill_id=bill_id).all()
        output = {}
        c = 1
        if bill_detail:
            for i in bill_detail:
                item = {'id': i.bill_id, 'medical': i.medical.name, 'count': i.count,
                        'added_on': i.added_on}
                output[c] = item
                c = c+1
            return output
        return output

    def check_info(self, medical_id):
        medical = Medical.query.filter_by(id=medical_id).first()
        if medical:
            item = {'id': medical.id, 'name': medical.name, 'count':1}
            return item
        return 'none'


    def add_to_cart(self,current_customer):
        try:
            cart_name = current_customer.username
            if 'x-access-token' in request.headers:
                data = request.json
            else:
                data = request.form
            if V.vali_add_to_cart(data) == True:
                medical_id = str(data['medical_id'])
                count = int(data['count'])
                medical = Medical.query.filter_by(id=medical_id).first()
                cart = session.get(cart_name)

                if medical:
                    if not cart:
                        cart = {}
                    if count <= medical.count:
                        if medical_id in cart.keys():
                            cart[medical_id]['count'] = cart[medical_id]['count'] + count
                            cart[medical_id]['total_price'] = self.total_price(current_customer, medical_id)
                        else:
                            cart[medical_id] = {'id':medical.id, 'name':medical.name, 'price':medical.sell_price, 'count':count, 'total_price':count*medical.sell_price}
                        session[cart_name] = cart
                        return session[cart_name], 201
                    return {}
                return {}
            return V.vali_add_to_cart(data)
        except AttributeError:
            return 'none'

    def show_count(self, current_customer, medical_id):
        cart_name = current_customer.username
        if cart_name in session.keys():
            cart = session[cart_name]
            if medical_id in cart.keys():
                item = {'id': cart[medical_id]['id'], 'name':cart[medical_id]['name'], 'count': cart[medical_id]['count']}
                return item
            return {}
        return {}

    def total_price(self, current_customer, medical_id):
        medical_in_cart = self.show_count(current_customer,medical_id)
        medical = Medical.query.filter_by(id=medical_id).first()
        count = medical_in_cart['count']
        return count*medical.sell_price

    def show_cart(self,current_customer):
        cart_name = current_customer.username
        if cart_name in session.keys():
            cart = session[cart_name]
            return cart
        else:
            session.get(cart_name)
            session[cart_name] = {}
            cart = session[cart_name]
            return cart

    def clear_cart(self,current_customer):
        cart_name = current_customer.username
        cart = {}
        session[cart_name] = cart
        return session[cart_name]

    def update_cart(self, current_customer, medical_id):
        cart_name = current_customer.username
        cart = self.show_cart(current_customer)
        if 'x-access-token' in request.headers:
            data = request.json
        else:
            data = request.form
        count = int(data['count'])
        medical = Medical.query.filter_by(id=medical_id).first()
        if medical_id in cart.keys():
            if V.vali_update_cart(data) == True:
                if count <= medical.count:
                    cart[medical_id]['count'] = count
                    cart[medical_id]['total_price'] = count*medical.sell_price
                    session[cart_name] = cart
                    return session[cart_name]
                return {}
            return V.vali_update_cart(data)
        return {}



    def delete_one_in_cart(self,current_customer,medical_id):
        cart_name = current_customer.username
        medical = Medical.query.filter_by(id=medical_id).first()
        cart = session[cart_name]
        if medical:
            if medical_id in cart.keys():
                cart.pop(str(medical_id))
                session[cart_name] = cart
                return 'delete'
            return {}
        return {}



