from cerberus import Validator
from flask import Response


class Validate:
    def vali_add_to_cart(self, data):
        schema = {'medical_id': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'regex':'[0-9]+'},
                  'name':{'type':'string'},
                  'count': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'regex':'[0-9]+'},
                  'submit': {'type': 'string'},
                  'csrf_token': {'type': 'string'}}
        v = Validator(schema)
        if v.validate(data, schema):
            return True
        else:
            return v.errors

    def vali_update_cart(self, data):
        schema = {
            'count': {'type': 'string', 'empty': False, 'nullable': False, 'required': True, 'regex': '[0-9]+'},
            'submit': {'type': 'string'},
            'csrf_token': {'type': 'string'}}
        v = Validator(schema)
        if v.validate(data, schema):
            return True
        else:
            return v.errors