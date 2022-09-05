from flask import flash, Blueprint
from manager.medical.services import ManagementMedical as MM
from manager.token import token_required, token_customer_required
MM = MM()

medicals = Blueprint("medicals", __name__)

@medicals.route('/medical/show-all/<page_num>',methods=['GET','POST'])
@token_required
def show_all_medical(current_user, page_num):
    return MM.show_all_medical(current_user, page_num)

@medicals.route('/medical/search/<page_num>',methods=['GET','POST'])
@token_required
def search_medical(current_user, page_num):
    return MM.search_medical(current_user, page_num)

@medicals.route('/customer/medical/show-all/<page_num>',methods=['GET','POST'])
@token_customer_required
def show_all_medical_customer(current_customer, page_num):
    return MM.show_all_medical_customer(current_customer, page_num)

@medicals.route('/customer/medical/search/<page_num>', methods=['POST','GET'])
@token_customer_required
def search_medical_customer(current_customer, page_num):
    return MM.search_medical_customer(current_customer, page_num)

@medicals.route('/medical/show/<medical_id>',methods=['POST','GET'])
@token_required
def show_medical(current_user,medical_id):
    return MM.show_medical(current_user,medical_id)

@medicals.route('/medical/insert', methods = ['POST','GET'])
@token_required
def insert_medical(current_user):
    return MM.insert_medical(current_user)

@medicals.route('/medical/delete/<medical_id>', methods = ['POST','GET'])
@token_required
def del_medical(current_user,medical_id):
    return MM.del_medical(current_user,medical_id)

@medicals.route('/medical/update/<medical_id>', methods = ['POST','GET'])
@token_required
def update_medical(current_user,medical_id):
    return MM.update_medical(current_user,medical_id)

@medicals.route('/medical-type/insert', methods = ['POST','GET'])
@token_required
def insert_medical_type(current_user):
    return MM.insert_medical_type(current_user)

@medicals.route('/medical-type/show-all/<page_num>', methods=['GET', 'POST'])
@token_required
def show_all_medical_type(current_user, page_num):
    return MM.show_all_medical_type(current_user, page_num)

@medicals.route('/medical-type/search/<page_num>', methods=['GET','POST'])
@token_required
def search_medical_type(current_user, page_num):
    return MM.search_medical_type(current_user, page_num)

@medicals.route('/medical-type/show/<medical_type_id>', methods=['GET','POST'])
@token_required
def show_medical_type(current_user,medical_type_id):
    return MM.show_medical_type(current_user,medical_type_id)

@medicals.route('/medical-type/update-medical-type/<medical_type_id>', methods = ['Get','POST'])
@token_required
def update_medical_type(current_user,medical_type_id):
    return MM.update_medical_type(current_user,medical_type_id)

@medicals.route('/medical-type/delete-medical-type/<medical_type_id>', methods = ['Get','POST'])
@token_required
def delete_medical_type(current_user,medical_type_id):
    return MM.del_medical_type(current_user, medical_type_id)

