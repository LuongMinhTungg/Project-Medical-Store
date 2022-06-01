from cerberus import Validator
import validators
from urllib.parse import urlparse

from flask import Response


class Validate:
    def vali_login(self,data):
        schema = {'username':{'type': 'string', 'empty': False, 'nullable': False, 'required': True,'minlength': 1, 'maxlength': 45},
                  'password': {'type': 'string', 'empty': False, 'nullable': False, 'required': True},'submit':{'type':'string'},
                  'csrf_token':{'type':'string'}}
        v = Validator(schema)
        if v.validate(data, schema):
            return True
        else:
            return v.errors

    def vali_update_user_admin(self,data):
        schema = {'name':{'type':'string', 'empty': True},
                  'role':{'type':'string', 'empty': True, 'required': True, 'allowed': ['manager', 'staff', 'admin']},
                  'phone':{'type': 'string', 'empty': True, 'nullable': True, 'required': False},
                  'submit': {'type': 'string'},
                  'csrf_token': {'type': 'string'}}
        v = Validator(schema)
        if v.validate(data,schema):
            return True
        return v.errors

    def vali_update_user(self,data):
        schema = {'name':{'type':'string', 'empty': True},
                  'role':{'type':'string', 'empty': True, 'required': True, 'allowed': ['manager', 'staff']},
                  'phone':{'type': 'string', 'empty': True, 'nullable': True, 'required': False},
                  'submit': {'type': 'string'},
                  'csrf_token': {'type': 'string'}}
        v = Validator(schema)
        if v.validate(data,schema):
            return True
        return v.errors

    def vali_reset_password_user(self,data):
        schema = {'old_password':{'type': 'string', 'empty': False, 'nullable': False, 'required': True},
                  'new_password':{'type': 'string', 'empty': False, 'nullable': False, 'required': True},
                  'confirm_password':{'type': 'string', 'empty': False, 'nullable': False, 'required': True},'submit': {'type': 'string'},
                  'csrf_token': {'type': 'string'}}
        v = Validator(schema)
        if v.validate(data, schema):
            return True
        return v.errors

    def vali_change_password_user(self,data):
        schema = {'username':{'type': 'string', 'empty': False,'required': True,'minlength': 1, 'maxlength': 45},
                  'old_password':{'type': 'string', 'empty': False, 'nullable': False, 'required': True},
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
                  'role': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'allowed': ['admin', 'manager', 'staff']},
                  'phone': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'regex': r'[0-9]{11}'},
                  'submit':{'type':'string'},
                  'csrf_token':{'type':'string'}}
        v = Validator(schema)
        if v.validate(data, schema):
            return True
        return v.errors

    def vali_register_user_manager(self,data):
        schema = {'name': {'type': 'string', 'empty': False,'required': True,'minlength': 1, 'maxlength': 45},
                  'username': {'type': 'string', 'empty': False, 'nullable': False, 'required': True,'minlength': 1, 'maxlength': 45},
                  'password': {'type': 'string', 'empty': False, 'nullable': False, 'required': True},
                  'confirm_password':{'type': 'string', 'empty': False, 'nullable': False, 'required': True},
                  'role': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'allowed': ['manager', 'staff']},
                  'phone': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'regex': r'[0-9]{11}'},
                  'submit':{'type':'string'},
                  'csrf_token':{'type':'string'}}
        v = Validator(schema)
        if v.validate(data, schema):
            return True
        return v.errors

    def vali_insert_role(self,data):
        schema = {'name': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'minlength': 1, 'maxlength': 45},
                  'submit': {'type': 'string'},
                  'csrf_token': {'type': 'string'}}
        v = Validator(schema)
        if v.validate(data, schema):
            return True
        return v.errors