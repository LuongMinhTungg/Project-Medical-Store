import datetime
from manager.config import app
from manager.extension import db, check_data
from manager.model.model import Medical,MedicalType
from flask import Flask, jsonify, request, Response, make_response, render_template, session, Blueprint, flash, redirect, url_for
from manager.medical.validate import Validate as V
V=V()
class BackEndMedical:
    list_medical_search = {}
    def show_all_medical(self):
        medical = Medical.query.all()
        output = {}
        if medical:
            for i in medical:
                item = {'id': i.id, 'name': i.name, 'type': i.medicaltype.name, 'count': i.count,
                        'buy_price': i.buy_price,
                        'sell_price': i.sell_price, 'exp_date': i.exp_date, 'description': i.description}
                output[i.id] = item
            return output
        return output

    def get_pages_search(self, page_num):
        data = check_data()
        search_data = data['search']
        medical = Medical.query.filter(Medical.name.contains(search_data)).paginate(int(page_num), per_page=5, error_out=False)
        if search_data == '':
            return self.get_pages_medical(page_num)
        return medical

    def search_medical_by_name(self):
        medical = self.get_pages_search(1)
        all = {}
        if medical.items:
            for i in range(1,medical.pages+1):
                output = []
                medical = self.get_pages_search(i)
                for j in medical.items:
                    item = {'id': j.id, 'name': j.name, 'type': j.medicaltype.name, 'count': j.count,
                            'buy_price': j.buy_price,
                            'sell_price': j.sell_price, 'exp_date': j.exp_date, 'description': j.description}
                    output.append(item)
                all[i] = output
            self.list_medical_search = all
            return all
        return 'none', 404

    def get_page_num_medical_search(self, medical_id):
        page = self.list_medical_search
        medical = Medical.query.filter_by(id=medical_id).first()
        x = 1
        for x in page.keys():
            if medical in page[x]:
                return x
        return x


    def get_pages_medical(self,page_num):
        medical = Medical.query.paginate(int(page_num), 5, False)
        return medical

    def get_page_number(self, medical_id):
        page = self.get_pages_medical(1)
        medical = Medical.query.filter_by(id=medical_id).first()
        c=1
        for i in range(1, page.pages+1):
            page = self.get_pages_medical(i)
            if medical in page.items:
                c = page.page
                return c
        return c


    def show_all_medical_page(self, page_num):
        medical = self.get_pages_medical(page_num)
        output = {}
        if medical:
            for i in medical.items:
                item = {'id':i.id,'name':i.name, 'type':i.medicaltype.name, 'count':i.count,'buy_price':i.buy_price,
                        'sell_price': i.sell_price, 'exp_date':i.exp_date, 'description':i.description}
                output[i.id] = item
            return output
        return output

    def show_medical(self,medical_id):
        medical = Medical.query.filter_by(id=medical_id).first()
        item = {}
        if medical:
            item = {'name':medical.name, 'type':medical.medicaltype.name, 'count':medical.count,'buy_price':medical.buy_price,
                    'sell_price': medical.sell_price, 'exp_date':medical.exp_date, 'description':medical.description}
            return item
        return item

    def insert_medical(self):
        data = check_data()
        if V.vali_insert_medical(data) == True:
            type = MedicalType.query.filter_by(name=data['type_name']).first()
            if not type:
                return 'not found medical type', 404
            else:
                if int(data['count']) >=0 and float(data['buy_price'])>=0 and float(data['sell_price']) >= 0:
                    new_medical = Medical(name=data['name'], type_id=type.id,
                                          count=data['count'], buy_price=data['buy_price'], sell_price=data['sell_price'],
                                          exp_date=data['exp_date'], description=data['description'])

                    db.session.add(new_medical)
                    db.session.commit()
                    flash('add')
                    return 'add', 201
                flash('not count')
                return 'not count', 404
        flash(V.vali_insert_medical(data))
        return V.vali_insert_medical(data)

    def delete_medical(self, medical_id):
        medical = Medical.query.filter_by(id=medical_id).first()
        if medical:
            try:
                db.session.delete(medical)
                db.session.commit()
                flash('delete')
                return 'delete', 204
            except:
                db.session.rollback()
                flash('medical is used! cant delete')
                return 'medical is used! cant delete', 404
        flash('none')
        return 'none', 404

    def update_medical(self, medical_id):
        medical = Medical.query.filter_by(id=medical_id).first()
        data = check_data()
        if V.vali_insert_medical(data):
            if medical:
                type = MedicalType.query.filter_by(name=data['type_name']).first()
                if not type:
                    flash('none type')
                    return 'none type', 404
                if int(data['count']) >= 0 and float(data['buy_price']) >= 0 and float(data['sell_price']) >= 0:
                    medical.name = data['name']
                    medical.type_id = type.id
                    medical.count = data['count']
                    medical.buy_price = data['buy_price']
                    medical.sell_price = data['sell_price']
                    medical.exp_date = data['exp_date']
                    medical.description = data['description']
                    db.session.commit()
                    flash('update')
                    return 'update', 202
                flash('not count')
                return 'not count', 404
            flash('none')
            return 'none', 404
        flash(V.vali_insert_medical(data))
        return V.vali_insert_medical(data)



    def show_all_medical_type(self):
        medical = MedicalType.query.paginate
        output = {}
        if medical:
            for i in medical:
                item = {'id': i.id, 'name': i.name, 'company': i.company}
                output[i.id] = item
            return output
        return output

    def show_medical_type_page(self, page_num):
        medical_type = self.get_pages_medical_type(page_num)
        output = {}
        if medical_type:
            for i in medical_type.items:
                item = {'id': i.id, 'name': i.name, 'company': i.company}
                output[i.id] = item
            return output
        return output

    def get_pages_medical_type(self, page_num):
        medical_type = MedicalType.query.paginate(int(page_num), 3, False)
        return medical_type

    def get_pages_number_medical_type(self, medical_type_id):
        page = self.get_pages_medical_type(1)
        medical_type = MedicalType.query.filter_by(id=medical_type_id).first()
        c=1
        for i in range(1, page.pages+1):
            page = self.get_pages_medical_type(i)
            if medical_type in page.items:
                c = page.page
                return c
        return c

    def show_medical_type(self,medical_type_id):
        medical_type = MedicalType.query.filter_by(id=medical_type_id).first()
        if medical_type:
            item = {'id': medical_type.id,'name':medical_type.name, 'company':medical_type.company}
            return item
        flash('none')
        return 'none', 404

    def insert_medical_type(self):
        c = request.headers.get('Content-Type')
        data = check_data()
        if V.vali_insert_medical_type(data) == True:
            new_medical_type = MedicalType(name=data['name'], company=data['company'])
            db.session.add(new_medical_type)
            db.session.commit()
            flash('add')
            return 'add', 201
        flash(V.vali_insert_medical_type(data))
        return V.vali_insert_medical_type(data)


    def delete_medical_type(self,medical_type_id):
        medical_type = MedicalType.query.filter_by(id=medical_type_id).first()
        if medical_type:
            try:
                db.session.delete(medical_type)
                db.session.commit()
                flash('delete')
                return 'delete', 204
            except:
                db.session.rollback()
                flash('medical type is used! cant delete')
                return 'medical type is used! cant delete', 404
        flash('none')
        return 'none', 404

    def update_medical_type(self,medical_type_id):
        medical_type = MedicalType.query.filter_by(id=medical_type_id).first()
        data = check_data()
        if V.vali_insert_medical_type(data):
            if medical_type:
                medical_type.name = data['name']
                medical_type.company = data['company']
                db.session.commit()
                flash('update')
                return 'update', 202
            flash('none')
            return 'none', 404
        flash(V.vali_insert_medical_type(data))
        return V.vali_insert_medical_type(data)


    def get_pages_search_medical_type(self, page_num):
        data = check_data()
        search_data = data['search']
        medical = MedicalType.query.filter(MedicalType.name.contains(search_data)).paginate(int(page_num), per_page=3, error_out=False)
        if search_data == '':
            return self.get_pages_medical_type(page_num)
        return medical

    def search_medical_type_by_name(self):
        medical = self.get_pages_search_medical_type(1)
        all = {}
        if medical.items:
            for i in range(1,medical.pages+1):
                output = []
                medical = self.get_pages_search_medical_type(i)
                for j in medical.items:
                    item = {'id': j.id, 'name': j.name, 'company': j.company}
                    output.append(item)
                all[i] = output
            return all
        return 'none', 404

