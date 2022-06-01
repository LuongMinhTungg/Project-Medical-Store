import datetime


from manager.extension import app
from manager.static.user import ManagementCustomer as MC
from flask import Flask, jsonify, request, Response, make_response, render_template, session, Blueprint, url_for, redirect
from manager.token import token_required, token_customer_required
from manager.model.model import ManagerUser
from manager.templates.admin import *

import uuid


indexs = Blueprint("indexs", __name__)



@indexs.route('/')
@token_required
def index(current_user):
    try:
        return render_template('home.html',current_user=current_user, role_user=current_user.role.name)
    except AttributeError:
        return redirect(url_for('managers.login'))

@indexs.route('/customer')
@token_customer_required
def index_customer(current_customer):
    return render_template('home_customer.html',current_customer=current_customer)

@indexs.route('/about')
@token_required
def about(current_user):
    return render_template('about.html',current_user=current_user,role_user=current_user.role.name)






