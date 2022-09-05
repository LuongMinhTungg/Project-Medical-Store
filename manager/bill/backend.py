from manager.extension import db, check_data
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
        flash('not found user')
        return 'not found user', 404

    def order_medical(self,current_customer):
        cart_name = current_customer.username
        cart = session[cart_name]
        check = ''
        if not cart:
            flash('cart is empty')
            return 'cart is empty', 404
        else:
            new_bill = self.create_bill(current_customer.id)
            for i,j in cart.items():
                medical_id, count = i, j['count']
                check = self.add_on_bill_detail(new_bill['id'],medical_id,int(count))
                if check == ('none', 404):
                    self.delete_one_in_cart(current_customer, medical_id)
            session[cart_name] = {}
            flash('add')
            return 'add', 201


    def add_on_bill_detail(self,bill_id,medical_id,count):
        medical = Medical.query.get(medical_id)
        bill_detail = BillDetail.query.filter_by(bill_id=bill_id,medical_id=medical_id).first()
        if medical:
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
            return 'none', 404
        return 'none', 404

    def del_medical_billdetail(self, medical_id):
        medical = BillDetail.query.get(medical_id)
        if medical:
            try:
                BillDetail.remove(medical)
                db.session.commit()
                flash('delete')
                return "Deleted", 204
            except IndentationError:
                db.session.rollback()
                flash('cant deleete')
                return jsonify({"message": "Can not delete medical!"}), 400
        else:
            flash('not found')
            return "Not found medical", 404

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

    def get_pages_bill(self,page_num):
        bill = Bill.query.order_by(Bill.id.desc()).paginate(int(page_num), 5, False)
        return bill

    def get_pages_number(self, medical_id):
        page = self.get_pages_bill(1)
        medical = Medical.query.filter_by(id=medical_id).first()
        c=1
        for i in range(1, page.pages+1):
            page = self.get_pages_bill(i)
            if medical in page.items:
                c = page.page
                return c
        return c

    def get_page_bill_customer(self, customer_id, page_num):
        bill = Bill.query.filter_by(customer_id=customer_id).order_by(Bill.id.desc()).paginate(int(page_num), 5, False)
        return bill

    def show_bill(self, page_num):
        all_bill = self.get_pages_bill(page_num)
        output = {}
        if all_bill:
            for i in all_bill.items:
                item = {'id': i.id, 'customer': i.customer.username, 'status': i.status,
                        'added_on': i.added_on}
                output[i.id] = item
            return output
        return output

    def show_bill_customer(self, customer_id, page_num):
        bill = self.get_page_bill_customer(customer_id, page_num)
        output = {}
        c = 1
        if bill:
            for i in bill.items:
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
                item = {'id': i.medical.id, 'medical': i.medical.name, 'count': i.count,
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
            data = check_data()
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
                        flash('add')
                        return 'add', 201
                    flash('fail! count > medical.count')
                    return 'count > medical.count', 404
                flash('not found')
                return 'not found'
            flash(V.vali_add_to_cart(data))
            return V.vali_add_to_cart(data)
        except AttributeError:
            flash('none')
            return 'none', 404

    def show_count(self, current_customer, medical_id):
        cart_name = current_customer.username
        if cart_name in session.keys():
            cart = session[cart_name]
            if medical_id in cart.keys():
                item = {'id': cart[medical_id]['id'], 'name':cart[medical_id]['name'], 'count': cart[medical_id]['count']}
                return item
            return 'none', 404
        return 'none', 404

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
        flash('clear')
        return 'clear', 204

    def update_cart(self, current_customer, medical_id):
        cart_name = current_customer.username
        cart = self.show_cart(current_customer)
        data = check_data()
        count = int(data['count'])
        medical = Medical.query.filter_by(id=medical_id).first()
        if medical_id in cart.keys():
            if V.vali_update_cart(data) == True:
                if count <= medical.count:
                    cart[medical_id]['count'] = count
                    cart[medical_id]['total_price'] = count*medical.sell_price
                    session[cart_name] = cart
                    flash('update')
                    return 'update', 202
                flash('count > medical.count')
                return 'count > medical.count', 404
            flash(V.vali_update_cart(data))
            return V.vali_update_cart(data)
        flash('none')
        return 'none', 404



    def delete_one_in_cart(self,current_customer,medical_id):

        cart_name = current_customer.username
        medical = Medical.query.filter_by(id=medical_id).first()
        cart = session[cart_name]
        if medical:
            if medical_id not in cart.keys():
                flash('none')
                return 'none', 404
            else:
                cart.pop(str(medical_id))
                session[cart_name] = cart
                flash('delete')
                return 'delete', 204
        flash(medical_id+' none')
        return 'none', 404



