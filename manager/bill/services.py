import datetime

import jwt
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, IntegerField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, ValidationError
from wtforms_components import read_only

from manager.config import app
from manager.extension import db
from manager.model.model import Bill, BillDetail, Medical, Customer
from flask import request, jsonify, session, url_for, render_template, flash, redirect
from manager.bill.backend import BackEndBill
BB = BackEndBill()

class ManagementBill:
    def show_cart(self, current_customer):
        try:
            cart = BB.show_cart(current_customer)
            output_1 = []
            headers = ('id', 'name', 'price', 'count', 'total_price')
            if request.method == 'GET':
                item = []
                if cart:
                    for i in cart.values():
                        item = [i['id'], i['name'], i['price'], i['count'], i['total_price']]
                        output_1.append(item)
                    return render_template('list_cart.html', title='Cart', headers=headers, data=output_1,
                                           current_customer=current_customer, row=item)
                return render_template('list_cart.html', title='Cart', headers=headers, data=output_1,
                                           current_customer=current_customer, row=item)
            return self.order_medical(current_customer)
        except AttributeError:
            return redirect(url_for('customers.login_customer'))


    def add_to_cart(self,current_customer):
        try:
            if request.method == 'POST':
                if not BB.add_to_cart(current_customer):
                    flash('fail')
                    return redirect(url_for('medicals.show_all_medical_customer'))
                flash('update')
                return redirect(url_for('medicals.show_all_medical_customer'))
            else:
                return redirect(url_for('medicals.show_all_medical_customer'))
        except AttributeError:
            return redirect(url_for('customers.login_customer'))

    def check_form(self,current_customer, medical_id):
        try:
            check_form = CheckForm(request.form)
            medical_in_cart = BB.check_info(medical_id)
            check_form.medical_id.data = medical_in_cart['id']
            check_form.name.data = medical_in_cart['name']
            check_form.count.data = medical_in_cart['count']
            if request.method == 'GET':
                return render_template('check_form.html', title='Check', form=check_form, current_customer=current_customer)
            else:
                if check_form.validate_on_submit() == True:
                    return self.add_to_cart(current_customer)
                return render_template('check_form.html', title='Check', form=check_form,
                                       current_customer=current_customer)
        except AttributeError:
            return redirect(url_for('customers.login_customer'))

    def order_medical(self, current_customer):
        try:

            if request.method == 'GET':
                BB.order_medical(current_customer)
                flash('order')
                return redirect(url_for('bills.show_cart'))
            return redirect(url_for('medicals.show_all_medical_customer'))
        except AttributeError:
            return redirect(url_for('customers.login_customer'))

    def show_all_bill(self,current_user):
        try:
            all_bill = BB.show_bill()
            output_1 = []
            headers = ('id','customer name', 'status', 'added on')
            if request.method == 'GET':
                item = []
                for i in all_bill.values():
                    item = [i['id'],i['customer'], i['status'], i['added_on']]
                    output_1.append(item)
                return render_template('list_bill.html', title='All Medical Type', headers=headers, data=output_1,
                                       current_user=current_user, row=item)
        except AttributeError:
            return redirect(url_for('customers.login_customer'))

    def show_bill_customer(self,current_customer, customer_id):
        try:
            bill = BB.show_bill_customer(customer_id)
            output_1 = []
            headers = ('id', 'customer name', 'status', 'added on')
            if request.method == 'GET':
                item = []
                for i in bill.values():
                    item = [i['id'], i['customer'], i['status'], i['added_on']]
                    output_1.append(item)
                return render_template('list_bill_customer.html', title='All Medical Type', headers=headers, data=output_1,
                                       current_customer=current_customer, row=item)
        except AttributeError:
            return redirect(url_for('customers.login_customer'))



    def show_bill_detail(self, current_user,bill_id):
        try:
            bill_detail = BB.show_bill_detail(bill_id)
            output_1 = []
            headers = ('id', 'medical name', 'count', 'added on')
            if request.method == 'GET':
                item = []
                for i in bill_detail.values():
                    item = [i['id'], i['medical'], i['count'], i['added_on']]
                    output_1.append(item)
                return render_template('bill_detail.html', title='Bill Detail', headers=headers, data=output_1,
                                       current_user=current_user, row=item)
        except AttributeError:
            return redirect(url_for('customers.login_customer'))

    def show_bill_detail_customer(self, current_customer,bill_id):
        try:
            bill_detail = BB.show_bill_detail(bill_id)
            output_1 = []
            headers = ('id', 'medical name', 'count', 'added on')
            if request.method == 'GET':
                item = []
                for i in bill_detail.values():
                    item = [i['id'], i['medical'], i['count'], i['added_on']]
                    output_1.append(item)
                return render_template('bill_detail_customer.html', title='Bill Detail', headers=headers, data=output_1,
                                       current_customer=current_customer, row=item)
        except AttributeError:
            return redirect(url_for('customers.login_customer'))

    def delete_one_cart(self, current_customer,medical_id):
        try:
            medical = Medical.query.filter_by(id=medical_id).first()
            if medical:
                if request.method == 'GET':
                    BB.delete_one_in_cart(current_customer,medical_id)
                    flash('delete')
                    return redirect(url_for('bills.show_cart'))
                else:
                    return redirect(url_for('bills.show_cart'))
            else:
                return "Not found user"
        except AttributeError:
            return redirect(url_for('customers.login_customer'))

    def update_cart(self, current_customer, medical_id):
        try:
            update_form = UpdateForm(request.form)
            medical_in_cart = BB.show_count(current_customer,medical_id)
            update_form.medical_id.data = medical_in_cart['id']
            update_form.name.data = medical_in_cart['name']
            update_form.count.data = medical_in_cart['count']
            if request.method == 'GET':
                return render_template('check_form.html', title='Check', form=update_form, current_customer=current_customer)
            else:
                if update_form.validate_on_submit() == True:
                    if not BB.update_cart(current_customer,medical_id):
                        flash('fail')
                        return redirect(url_for('bills.show_cart'))
                    return redirect(url_for('bills.show_cart'))
                return render_template('check_form.html', title='Check', form=update_form,
                                       current_customer=current_customer)
        except AttributeError:
            return redirect(url_for('customers.login_customer'))

    def clear_cart(self, current_customer):
        try:

            if request.method == 'GET':
                BB.clear_cart(current_customer)
                flash('delete')
                return redirect(url_for('bills.show_cart'))
            else:
                return redirect(url_for('bills.show_cart'))
        except AttributeError:
            return redirect(url_for('customers.login_customer'))


class CheckForm(FlaskForm):
    medical_id = StringField('medical_id', validators=[DataRequired()])
    name = StringField('name')
    count = IntegerField('count',validators=[DataRequired()])
    submit = SubmitField('Add', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(CheckForm, self).__init__(*args, **kwargs)
        read_only(self.name)

    def validate_medical_count(self, medical_id):
        medical = Medical.query.filter_by(id=medical_id.data).first()
        if self.count.data > medical.count:
            raise ValidationError('none')

class UpdateForm(FlaskForm):
    medical_id = StringField('medical_id', validators=[DataRequired()])
    name = StringField('name')
    count = IntegerField('count', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Update', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        read_only(self.name)
        read_only(self.medical_id)

    def validate_medical_count(self, medical_id):
        medical = Medical.query.filter_by(id=medical_id.data).first()
        if self.count.data > medical.count:
            raise ValidationError('none')

