from flask_sqlalchemy import Pagination
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, IntegerField, FloatField, DateField, SelectField

from wtforms.validators import DataRequired, Length, NumberRange

from manager.model.model import MedicalType, Medical
from flask import request, jsonify, render_template, flash, url_for
from manager.medical.backend import BackEndMedical

BM = BackEndMedical()


class ManagementMedical:
    data = ''
    search_list = {}
    search_medical_pages = {}
    search_list_medical_type = {}
    search_medical_type_pages = {}
    search_list_customer = {}
    search_medical_customer_pages = {}
    def show_all_medical(self,current_user, page_num):
        try:
            all_medical = BM.show_all_medical_page(page_num)
            search_form = SearchForm(request.form)
            output_1 = []
            headers = ('id','name', 'type', 'count', 'buy price', 'sell price','exp date', 'description')
            if request.method == 'GET':
                item = []
                pages = BM.get_pages_medical(page_num)
                for i in all_medical.values():
                    item = [i['id'],i['name'], i['type'], i['count'], i['buy_price'], i['sell_price'],i['exp_date'],i['description']]
                    output_1.append(item)
                return render_template('list_medical.html', title='All Medical', headers=headers, data=output_1,
                                       form=search_form, current_user=current_user, row=item, pages=pages)
            else:
                self.data = search_form.search.data
                self.search_list = BM.search_medical_by_name()
                self.search_medical_pages = BM.get_pages_search(page_num)
                #return redirect(url_for('medicals.show_all_medical', page_num=1))
                return redirect(url_for('medicals.search_medical', page_num=1))
        except AttributeError:
            return redirect(url_for('managers.login'))

    def search_medical(self,current_user, page_num):
        output_1 = []
        headers = ('id', 'name', 'type', 'count', 'buy price', 'sell price', 'exp date', 'description')
        search_form = SearchForm(request.form)
        if request.method == 'GET':
            item = []
            if self.search_list == ('none', 404):
                search_form.search.data = self.data
                return render_template('list_medical.html', title='All Medical', headers=headers, data=output_1,
                                       form=search_form, current_user=current_user, row=item,
                                       pages=self.search_medical_pages)
            else:
                search_form.search.data = self.data
                for key in self.search_list.keys():
                    if int(page_num) == key:
                        for i in self.search_list[key]:
                            item = [i['id'], i['name'], i['type'], i['count'],
                                    i['buy_price'], i['sell_price'], i['exp_date'], i['description']]
                            output_1.append(item)
                        return render_template('list_medical.html', title='Medical', headers=headers, data=output_1,
                                               form=search_form, current_user=current_user, row=item,
                                               pages=self.search_medical_pages, search='a')
                return self.show_all_medical(current_user, 1)
        else:
            if search_form.search.data == '':
                return redirect(url_for('medicals.show_all_medical', page_num=1))
            return self.show_all_medical(current_user, 1)



    def show_all_medical_customer(self,current_customer, page_num):
        try:
            all_medical = BM.show_all_medical_page(page_num)
            search_form = SearchForm(request.form)
            output_1 = []
            headers = ('id','name', 'type', 'count', 'price','exp date', 'description')
            pages=BM.get_pages_medical(1)
            item = []
            if request.method == 'GET':
                for i in all_medical.values():
                    item = [i['id'],i['name'], i['type'], i['count'], i['sell_price'],i['exp_date'],i['description']]
                    output_1.append(item)
                return render_template('list_medical_customer.html', title='All Medical', headers=headers, data=output_1,
                                       form=search_form, current_customer=current_customer, row=item, pages=pages)
            else:
                self.data = search_form.search.data
                self.search_list_customer = BM.search_medical_by_name()
                self.search_medical_customer_pages = BM.get_pages_search(page_num)
                return redirect(url_for('medicals.search_medical_customer', page_num=1))
        except AttributeError:
            return redirect(url_for('customers.login_customer'))

    def search_medical_customer(self, current_customer, page_num):
        try:
            search_form = SearchForm(request.form)
            output_1 = []
            headers = ('id', 'name', 'type', 'count', 'price', 'exp date', 'description')
            item = []
            if request.method == 'GET':
                if self.search_list_customer == ('none', 404):
                    search_form.search.data = self.data
                    return render_template('list_medical_customer.html', title='All Medical', headers=headers, data=output_1,
                                           form=search_form, current_customer=current_customer, row=item,
                                           pages=self.search_medical_customer_pages, search='a')

                else:
                    search_form.search.data = self.data
                    for key in self.search_list_customer.keys():
                        if int(page_num) == key:
                            for i in self.search_list_customer[key]:
                                item = [i['id'], i['name'], i['type'], i['count'],
                                        i['buy_price'], i['sell_price'], i['exp_date'], i['description']]
                                output_1.append(item)
                            return render_template('list_medical_customer.html', title='Medical', headers=headers, data=output_1,
                                                   form=search_form, current_customer=current_customer, row=item,
                                                   pages=self.search_medical_customer_pages, search='a')
                    return redirect(url_for('medicals.show_all_medical_customer', page_num=1))
            else:
                if search_form.search.data == '':
                    return redirect(url_for('medicals.show_all_medical_customer', page_num=1))
                return self.show_all_medical_customer(current_customer, 1)
        except AttributeError:
            return redirect(url_for('customers.login_customer'))

    def show_medical(self,current_user,medical_id):
        medical_form = MedicalForm(request.form)
        medical_form.type_name.choices = [i.name for i in MedicalType.query.all()]
        medical = BM.show_medical(medical_id)
        if request.method == 'GET':
            medical_form.name.data = medical['name']
            medical_form.type_name.data = medical['type']
            medical_form.count.data = medical['count']
            medical_form.buy_price.data = medical['buy_price']
            medical_form.sell_price.data = medical['sell_price']
            medical_form.exp_date.data = medical['exp_date']
            medical_form.description.data = medical['description']
            return render_template('medical.html', title='account', form=medical_form,current_user=current_user)
        else:
            if medical_form.validate_on_submit():
                return self.update_medical(current_user, medical_id)
            return render_template('medical.html', title='account', form=medical_form, current_user=current_user)

    def insert_medical(self,current_user):
        insert_form = InsertMedicalForm(request.form)
        if request.method == 'POST':
            if insert_form.validate_on_submit() == True:
                if BM.insert_medical() == ('add', 201):
                    page_num = BM.get_pages_medical(1).pages
                    return redirect(url_for('medicals.show_all_medical', page_num=page_num))
                return redirect(url_for('medicals.insert_medical'))
        return render_template('insert_medical.html',title='insert medical',form=insert_form,current_user=current_user)

    def del_medical(self,current_user, medical_id):
        medical = Medical.query.filter_by(id=medical_id).first()
        page_num = BM.get_page_number(medical_id)
        if medical:
            if request.method == 'GET':
                BM.delete_medical(medical_id)
                return redirect(url_for('medicals.show_all_medical', page_num=page_num))
            else:
                return redirect(url_for('medicals.show_all_medical', page_num=page_num))
        else:
            return render_template('error_not_found.html', current_user=current_user)

    def update_medical(self, current_user, medical_id):
        medical = Medical.query.filter_by(id=medical_id).first()
        if medical:
            if request.method == 'POST':
                page_num = BM.get_page_number(medical_id)
                if BM.update_medical(medical_id) == ('update',202):
                    return redirect(url_for('medicals.show_all_medical', page_num=page_num))
            else:
                return redirect(url_for('medicals.show_medical',medical_id=medical_id))
        return render_template('error_not_found.html', current_user=current_user)


    def show_all_medical_type(self, current_user, page_num):
        all_medical_type = BM.show_medical_type_page(page_num)
        search_form = SearchForm()
        output_1 = []
        headers = ('id', 'name', 'company')
        item = []
        pages = BM.get_pages_medical_type(page_num)
        if request.method == 'GET':
            for i in all_medical_type.values():
                item = [i['id'],i['name'], i['company']]
                output_1.append(item)
            return render_template('list_medical_type.html', title='All Medical Type', headers=headers, data=output_1,
                                   form=search_form, current_user=current_user, row=item, pages=pages)
        else:
            self.data = search_form.search.data
            self.search_list_medical_type = BM.search_medical_type_by_name()
            self.search_medical_type_pages = BM.get_pages_search_medical_type(page_num)
            return redirect(url_for('medicals.search_medical_type', page_num=1))

    def search_medical_type(self, current_user, page_num):
        try:
            search_form = SearchForm()
            output_1 = []
            headers = ('id', 'name', 'company')
            item = []
            if request.method == 'GET':
                if self.search_list_medical_type == ('none', 404):
                    return render_template('list_medical_type.html', title='Medical Type', headers=headers,
                                           data=output_1, form=search_form, current_user=current_user,
                                           row=item, pages=self.search_medical_type_pages, search='a')

                else:
                    search_form.search.data = self.data
                    for key in self.search_list_medical_type.keys():
                        if int(page_num) == key:
                            for i in self.search_list_medical_type[key]:
                                item = [i['id'], i['name'], i['company']]
                                output_1.append(item)
                            return render_template('list_medical_type.html', title='Medical Type', headers=headers, data=output_1,
                                                   form=search_form, current_user=current_user, row=item,
                                                   pages=self.search_medical_type_pages, search='a')
                    return redirect(url_for('medicals.show_all_medical_type', page_num=1))
            else:
                if search_form.search.data == '':
                    return redirect(url_for('medicals.show_all_medical_type', page_num=1))
                return self.show_all_medical_type(current_user, 1)
        except AttributeError:
            return redirect(url_for('mangers.login'))


    def show_medical_type(self,current_user,medical_type_id):
        medical_type_form = InsertMedicalTypeForm(request.form)
        medical_type = BM.show_medical_type(medical_type_id)
        if request.method == 'GET':
            medical_type_form.name.data = medical_type['name']
            medical_type_form.company.data = medical_type['company']
            return render_template('insert_medical_type.html', title='account', form = medical_type_form,current_user=current_user,role_user=current_user.role.name)
        else:
            if medical_type_form.validate_on_submit():
                return self.update_medical_type(current_user, medical_type_id)
            return render_template('insert_medical_type.html', title='account', form=medical_type_form,
                                   current_user=current_user)

    def insert_medical_type(self,current_user):
        insert_mt_form = InsertMedicalTypeForm()
        if request.method == 'POST':
            if BM.insert_medical_type() == ('add',201):
                page_num = BM.get_pages_medical_type(1).pages
                return redirect(url_for('medicals.show_all_medical_type', page_num=page_num))
        return render_template('insert_medical_type.html', title='insert medical type', form=insert_mt_form, current_user=current_user)

    def update_medical_type(self, current_user, medical_type_id):
        medical_type = MedicalType.query.filter_by(id=medical_type_id).first()

        if medical_type:
            if request.method == 'POST':
                if BM.update_medical_type(medical_type_id) == ('update', 202):
                    page_num = BM.get_pages_number_medical_type(medical_type_id)
                    return redirect(url_for('medicals.show_all_medical_type', page_num=page_num))
                return redirect(url_for('medicals.show_medical_type', medical_type_id=medical_type_id))
            else:
                return redirect(url_for('medicals.show_medical_type', medical_type_id=medical_type_id))
        return render_template('error_not_found.html', current_user=current_user)

    def del_medical_type(self,current_user, medical_type_id):
        medical_type = MedicalType.query.get(medical_type_id)
        page_num = BM.get_pages_number_medical_type(medical_type_id)
        if medical_type:
            if request.method == 'GET':
                BM.delete_medical_type(medical_type_id)
                return redirect(url_for('medicals.show_all_medical_type', page_num=page_num))
            return redirect(url_for('medicals.show_all_medical_type', page_num=page_num))
        else:
            return render_template('error_not_found.html', current_user=current_user)

class SearchForm(FlaskForm):
    search = StringField('search')
    submit = SubmitField('Search')

class InsertMedicalForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=2, max=45)])
    type_name = SelectField('Type', validators=[DataRequired()], choices=[i.name for i in MedicalType.query.all()])
    count = IntegerField('Count', validators=[DataRequired(), NumberRange(min=0)])
    buy_price = FloatField('Buy Price', validators=[DataRequired(), NumberRange(min=0.1)])
    sell_price = FloatField('Sell Price', validators=[DataRequired(), NumberRange(min=0.1)])
    exp_date = DateField('Exp Date',validators=[DataRequired()],format="%Y-%m-%d")
    description = StringField('Description', validators=[Length(min=1,max=255)])
    submit = SubmitField('Add')

class InsertMedicalTypeForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=2, max=45)])
    company = StringField('Company', validators=[DataRequired(), Length(min=2, max=45)])
    submit = SubmitField('Add')

class MedicalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=45)])
    type_name = SelectField('Type', validators=[DataRequired()], choices=[])
    count = IntegerField('Count', validators=[DataRequired(), NumberRange(min=0)])
    buy_price = FloatField('Buy Price', validators=[DataRequired(), NumberRange(min=0.1)])
    sell_price = FloatField('Sell Price', validators=[DataRequired(), NumberRange(min=0.1)])
    exp_date = DateField('Exp Date', validators=[DataRequired()], format="%Y-%m-%d")
    description = StringField('Description', validators=[Length(min=1, max=255)])
    submit = SubmitField('Change',validators=[DataRequired()])