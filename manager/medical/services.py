from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, IntegerField, FloatField, DateField, DateTimeField, SelectField

from wtforms.validators import DataRequired, Length, NumberRange

from manager.model.model import MedicalType, Medical
from flask import request, jsonify, render_template, flash, url_for
from manager.medical.backend import BackEndMedical

BM = BackEndMedical()


class ManagementMedical:
    def show_all_medical(self,current_user):
        try:
            all_medical = BM.show_all_medical()
            search_form = SearchForm(request.form)
            output_1 = []
            headers = ('id','name', 'type', 'count', 'buy price', 'sell price','exp date', 'description')
            if request.method == 'GET':
                item = []

                for i in all_medical.values():
                    item = [i['id'],i['name'], i['type'], i['count'], i['buy_price'], i['sell_price'],i['exp_date'],i['description']]
                    output_1.append(item)
                return render_template('list_medical.html', title='All Medical', headers=headers, data=output_1,
                                       form=search_form, current_user=current_user, row=item,role_user=current_user.role.name)

            else:
                output_2 = []
                item = []
                list = BM.search_medical_by_name()
                for i in list.values():
                    item = [i['id'], i['name'], i['type'], i['count'],
                                    i['buy_price'], i['sell_price'], i['exp_date'], i['description']]
                    output_2.append(item)
                return render_template('list_medical.html', title='All Medical', headers=headers, data=output_2,
                                       form=search_form, current_user=current_user,role_user=current_user.role.name)
        except AttributeError:
            return redirect(url_for('managers.login'))


    def show_all_medical_customer(self,current_customer):
        try:
            all_medical = BM.show_all_medical()
            search_form = SearchForm(request.form)
            output_1 = []
            headers = ('id','name', 'type', 'count', 'price','exp date', 'description')
            if request.method == 'GET':
                item = []

                for i in all_medical.values():
                    item = [i['id'],i['name'], i['type'], i['count'], i['sell_price'],i['exp_date'],i['description']]
                    output_1.append(item)
                return render_template('list_medical_customer.html', title='All Medical', headers=headers, data=output_1,
                                       form=search_form, current_customer=current_customer, row=item)

            else:
                output_2 = []
                item = []
                list = BM.search_medical_by_name()
                for i in list.values():
                    item = [i['id'], i['name'], i['type'], i['count'],
                                    i['buy_price'], i['sell_price'], i['exp_date'], i['description']]
                    output_2.append(item)
                return render_template('list_medical_customer.html', title='All Medical', headers=headers, data=output_2,
                                       form=search_form, current_customer=current_customer)
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
                    return redirect(url_for('medicals.show_all_medical'))
                return redirect(url_for('medicals.insert_medical'))
        return render_template('insert_medical.html',title='insert medical',form=insert_form,current_user=current_user)

    def del_medical(self,current_user, medical_id):
        medical = Medical.query.filter_by(id=medical_id).first()
        if medical:
            if request.method == 'GET':
                BM.delete_medical(medical_id)
                return redirect(url_for('medicals.show_all_medical'))
            else:
                return redirect(url_for('medicals.show_all_medical'))
        else:
            return render_template('error_not_found.html', current_user=current_user)

    def update_medical(self, current_user, medical_id):
        medical = Medical.query.filter_by(id=medical_id).first()
        if medical:
            if request.method == 'POST':
                if BM.update_medical(medical_id) == ('update',202):
                    return redirect(url_for('medicals.show_all_medical'))
                return redirect(url_for('medicals.show_medical',medical_id=medical_id))
            else:
                return redirect(url_for('medicals.show_medical',medical_id=medical_id))
        return render_template('error_not_found.html', current_user=current_user)

    def show_all_medical_type(self,current_user):
        all_medical_type = BM.show_all_medical_type()
        search_form = SearchForm()
        output_1 = []
        headers = ('id', 'name', 'company')
        item = []
        if request.method == 'GET':
            for i in all_medical_type.values():
                item = [i['id'],i['name'], i['company']]
                output_1.append(item)
            return render_template('list_medical_type.html', title='All Medical Type', headers=headers, data=output_1,
                                   form=search_form, current_user=current_user, row=item)
        return render_template('list_medical_type.html', title='All Medical Type', headers=headers, data=output_1,
                               form=search_form, current_user=current_user, row=item)


    def show_medical_type(self,current_user,medical_type_id):
        medical_type_form = InsertMedicalTypeForm(request.form)
        medical_type = BM.show_medical_type(medical_type_id)
        if request.method == 'GET':
            medical_type_form.name.data = medical_type['name']
            medical_type_form.company.data = medical_type['company']
            return render_template('insert_medical_type.html', title = 'account', form = medical_type_form,current_user=current_user,role_user=current_user.role.name)
        else:
            if medical_type_form.validate_on_submit():
                return redirect(url_for('medicals.update_medical_type',medical_type_id=medical_type_id))
            return render_template('insert_medical_type.html', title='account', form=medical_type_form,
                                   current_user=current_user)

    def insert_medical_type(self,current_user):
        insert_mt_form = InsertMedicalTypeForm()
        if request.method == 'POST':
            if BM.insert_medical_type() == ('add',201):
                return redirect(url_for('medicals.show_all_medical_type'))
        return render_template('insert_medical_type.html', title='insert medical type', form=insert_mt_form, current_user=current_user,role_user=current_user.role.name)

    def update_medical_type(self, current_user, medical_type_id):
        medical_type = MedicalType.query.filter_by(id=medical_type_id).first()
        if medical_type:
            if request.method == 'POST':
                if BM.update_medical_type(medical_type_id) == ('update', 202):
                    return redirect(url_for('medicals.show_all_medical_type'))
                return redirect(url_for('medicals.show_medical_type', medical_type_id=medical_type_id))
            else:
                return redirect(url_for('medicals.show_medical_type', medical_type_id=medical_type_id))
        return render_template('error_not_found.html', current_user=current_user)

    def del_medical_type(self,current_user, medical_type_id):
        medical_type = MedicalType.query.get(medical_type_id)
        if medical_type:
            if request.method == 'GET':
                BM.delete_medical_type(medical_type_id)
                return redirect(url_for('medicals.show_all_medical_type'))
            return redirect(url_for('medicals.show_all_medical_type'))
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