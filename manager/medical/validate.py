from cerberus import Validator
import validators
from urllib.parse import urlparse

from flask import Response


class Validate:
    def vali_insert_medical(self, data):
        schema = {'name': {'type': 'string', 'empty': False, 'required': True, 'nullable': False, 'minlength': 1, 'maxlength': 45},
                  'type_id': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'regex': r'[0-9]'},
                  'count': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'regex': r'[0-9]+'},
                  'buy_price': {'type': 'string', 'empty': False, 'nullable': False, 'required': True,'regex': r'[0-9]+.[0-9]+'},
                  'sell_price': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'regex': r'[0-9]+.[0-9]+'},
                  'exp_date': {'type': 'string', 'empty': False, 'nullable': False, 'required': True,'regex': r'[0-9]{4}-[0-9]{2}-[0-9]{2}'},
                  'description': {'type': 'string', 'empty': True, 'minlength': 1, 'maxlength': 255},
                  'submit': {'type': 'string'},
                  'csrf_token': {'type': 'string'}}
        v = Validator(schema)
        if v.validate(data, schema):
            return True
        else:
            return v.errors

    def vali_update_medical(self, data):
        schema = {'name': {'type': 'string', 'empty': False, 'required': True, 'nullable': False, 'minlength': 1, 'maxlength': 45},
                  'type_name': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'minlength': 1, 'maxlength': 45},
                  'count': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'regex': r'[0-9]+'},
                  'buy_price': {'type': 'string', 'empty': False, 'nullable': False, 'required': True,'regex': r'[0-9]+.[0-9]'},
                  'sell_price': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'regex': r'[0-9]+.[0-9]'},
                  'exp_date': {'type': 'string', 'empty': False, 'nullable': False, 'required': True,'regex': r'[0-9]{4}-[0-9]{2}-[0-9]{2}'},
                  'description': {'type': 'string', 'empty': True, 'maxlength': 255},
                  'submit': {'type': 'string'},
                  'csrf_token': {'type': 'string'}}
        v = Validator(schema)
        if v.validate(data, schema):
            return True
        else:
            return v.errors

    def vali_insert_medical_type(self,data):
        schema = {'name': {'type': 'string', 'empty': False, 'required': True, 'nullable': False, 'minlength': 1, 'maxlength': 45},
                  'company': {'type': 'string', 'empty': False, 'required': True, 'nullable': False, 'minlength': 1, 'maxlength': 45},
                  'submit': {'type': 'string'},
                  'csrf_token': {'type': 'string'}}
        v = Validator(schema)
        if v.validate(data,schema):
            return True
        return v.errors

    def vali_update_medical_type(self,data):
        schema = {'old_password':{'type': 'string', 'empty': False, 'nullable': False, 'required': True},
                  'new_password':{'type': 'string', 'empty': False, 'nullable': False, 'required': True},
                  'confirm_password':{'type': 'string', 'empty': False, 'nullable': False, 'required': True},'submit': {'type': 'string'},
                  'csrf_token': {'type': 'string'}}
        v = Validator(schema)
        if v.validate(data, schema):
            return True
        return v.errors

    def vali_register_user(self,data):
        schema = {'name': {'type': 'string', 'empty': False,'required': True,'minlength': 1, 'maxlength': 45},
                  'username': {'type': 'string', 'empty': False, 'nullable': False, 'required': True,'minlength': 1, 'maxlength': 45},
                  'password': {'type': 'string', 'empty': False, 'nullable': False, 'required': True},
                  'confirm_password':{'type': 'string', 'empty': False, 'nullable': False, 'required': True},
                  'role_id': {'type': 'string', 'empty': False, 'nullable': False, 'required': True,'regex': r'[0-9]','min':1,'max':3},
                  'phone': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'regex': r'[0-9]{11}'},
                  'submit':{'type':'string'},
                  'csrf_token':{'type':'string'}}
        v = Validator(schema)
        if v.validate(data, schema):
            return True
        return v.errors