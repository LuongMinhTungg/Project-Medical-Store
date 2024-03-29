import datetime

import jwt

from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, IntegerField, SubmitField, BooleanField, DateField, Field
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, ValidationError
from wtforms_components import read_only

from manager.config import app
from manager.extension import db
from manager.model.model import Bill, BillDetail, Medical, Customer
from flask import request, jsonify, session, url_for, render_template, flash
from manager.customer.backend import BackEndCustomer
BC = BackEndCustomer()

class ManagementCustomer:
    def login(self):
        form = LoginForm(request.form)
        try:
            if request.method == 'POST':
                if form.validate_on_submit():
                    token = BC.login_customer()
                    resp = redirect(url_for('indexs.index_customer'))
                    resp.set_cookie('token_customer', value=token)
                    return resp
            return render_template('login_customer.html', title='login_customer', form=form)
        except TypeError:
            return render_template('login_customer.html', title='login_customer', form=form)


    def register(self):
        register_form = RegistrationForm(request.form)
        if request.method == 'POST':
            if register_form.validate_on_submit():
                if BC.register_customer() == ('add', 202):
                    return redirect(url_for('customers.login_customer'))
                return render_template('register_customer.html', title='register', form=register_form)
        return render_template('register_customer.html', title='register', form=register_form)

    def logout(self):
        resp = redirect(url_for('indexs.index_customer'))
        resp.set_cookie('token_customer', value='')
        return resp

    def reset_password(self,current_customer,username):
        reset_password_form = ResetPasswordForm(request.form)
        if request.method == 'POST':
            if reset_password_form.validate_on_submit():
                if BC.reset_password_customer(username) == ('reset', 202):
                    return redirect(url_for('indexs.index_customer'))
                return render_template('reset_password_customer.html', title='reset_password',
                                   form=reset_password_form, current_customer=current_customer)

        return render_template('reset_password_customer.html', title='reset_password', form=reset_password_form,
                               current_customer=current_customer)


    def change_password(self):
        change_password_form = ChangePasswordForm(request.form)
        if request.method == 'POST':
            if change_password_form.validate_on_submit():
                if BC.change_password() == ('reset', 202):
                    flash('success')
                    return redirect(url_for('indexs.index_customer'))
                flash(BC.change_password())
                return render_template('change_password_customer.html', title='change_password', form=change_password_form)
            flash('fail')
            return render_template('change_password_customer.html', title='change_password', form=change_password_form)
        return render_template('change_password_customer.html', title = 'change_password', form=change_password_form)

    def get_customer(self,current_customer,username):
        try:
            customer_form = CustomerForm(request.form)
            customer = BC.get_account_customer(username)
            customer_form.username.data = customer['username']
            customer_form.join_date.data = customer['join_date']
            if customer:
                if request.method == 'GET':
                    customer_form.name.data = customer['name']
                    customer_form.username.data = customer['username']
                    customer_form.phone.data = customer['phone']
                    customer_form.address.data = customer['address']
                    customer_form.join_date.data = customer['join_date']
                    return render_template('customer_account.html', title = 'account', form = customer_form, current_customer=current_customer)
                else:
                    if customer_form.validate_on_submit():
                        BC.update_customer_account(customer['username'])
                        customer_form.name.data = customer['name']
                        customer_form.address.data = customer['address']
                        customer_form.phone.data = customer['phone']
                        return render_template('customer_account.html', title = 'account', form = customer_form, current_customer=current_customer)
                    return render_template('customer_account.html', title='account', form=customer_form,
                                           current_customer=current_customer)
            return render_template('error_not_found_customer.html', current_customer=current_customer)
        except AttributeError:
            return redirect(url_for('customers.login_customer'))
        except:
            return render_template('error_not_found_customer.html', current_customer=current_customer)


class RegistrationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=1, max=45)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=1, max=45)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    address = StringField('address',validators=[DataRequired(), Length(min=1, max=45)])
    phone = StringField('phone', validators=[DataRequired(),Length(min=11,max=11)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Customer.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Length(min=1, max=45)])
    password = PasswordField('password', validators=[DataRequired(),Length(min=1, max=45)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_user(self,username):
        user = Customer.query.filter_by(username =username.data).first()
        if not user:
            raise ValidationError('Wrong password or username')

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('old_password',validators=[DataRequired()])
    new_password = PasswordField('new_password',validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password',validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change')


class ChangePasswordForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=1, max=45)])
    old_password = PasswordField('old_password',validators=[DataRequired()])
    new_password = PasswordField('new_password',validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password',validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change')
    def validate_username(self, username):
        user = Customer.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('wrong username or password')
        elif not check_password_hash(user.password, self.old_password.data):
            raise ValidationError('wrong password')
        elif check_password_hash(user.password, self.new_password.data):
            raise ValidationError('old password = new password')


class CustomerForm(FlaskForm):
    name = StringField('name',validators=[DataRequired(),Length(min=1, max=45)])
    username = StringField('username')
    address = StringField('address',validators=[DataRequired(),Length(min=1, max=45)])
    phone = StringField('phone',validators=[DataRequired(),Length(min=11, max=11)])
    join_date = DateField('join date')
    submit = SubmitField('Change',validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        read_only(self.username)
        read_only(self.join_date)

    def validate_username(self, username):
        user = Customer.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')