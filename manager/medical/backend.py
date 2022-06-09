import datetime
from manager.config import app
from manager.extension import db
from manager.model.model import Medical,MedicalType
from flask import Flask, jsonify, request, Response, make_response, render_template, session, Blueprint, flash, redirect, url_for
from manager.medical.validate import Validate as V
V=V()
class BackEndMedical:
    def show_all_medical(self):
        medical = Medical.query.all()
        output = {}
        if medical:
            for i in medical:
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
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
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
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
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

    def search_medical_by_name(self):
        medical = self.show_all_medical()
        output = {}
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
        search_data = data['search']
        if medical:
            for i in medical.values():
                if search_data in i['name']:
                    item = {'id': i['id'], 'name': i['name'], 'type': i['type'], 'count': i['count'],
                            'buy_price': i['buy_price'],
                            'sell_price': i['sell_price'], 'exp_date': i['exp_date'], 'description': i['description']}
                    output[i['id']] = item
            return output
        return output

    def show_all_medical_type(self):
        medical = MedicalType.query.all()
        output = {}
        if medical:
            for i in medical:
                item = {'id': i.id, 'name': i.name, 'company': i.company}
                output[i.id] = item
            return output
        return output

    def show_medical_type(self,medical_type_id):
        medical_type = MedicalType.query.filter_by(id=medical_type_id).first()
        if medical_type:
            item = {'id': medical_type.id,'name':medical_type.name, 'company':medical_type.company}
            return item
        flash('none')
        return 'none', 404

    def insert_medical_type(self):
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
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
        c = request.headers.get('Content-Type')
        if c == 'application/json':
            data = request.json
        else:
            data = request.form
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


