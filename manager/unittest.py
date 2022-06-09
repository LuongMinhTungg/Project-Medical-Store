import json
import sys
import unittest
import requests
from manager.manager_user.backend import BackEndManagerUser
from manager.model.model import ManagerUser
from manager.extension import db
from manager import create_app
from manager.postman import postmans
from manager.manager_user.controller import managers

BM = BackEndManagerUser()
URL_get_user = 'http://127.0.0.1:3000/get-user/admin'
URL_get_user_postman = 'http://127.0.0.1:3000/backend/user/get/admin'
URL_insert_user_postman = 'http://127.0.0.1:3000/backend/user/insert'
class BaseCase(unittest.TestCase):
    current_user = ManagerUser.query.filter_by(id=1).first()
    data = {
        "join_date": "2022-05-20",
        "name": "admin",
        "phone": "11111111111",
        "role": "admin",
        "username": "admin"}

    def setUp(self):
        app = create_app()
        self.app = app.test_client()
        self.db = db.Model



class TestApi(BaseCase):
    def test_thing(self):
        response = self.app.get('/')


    def test_show_all_user(self):
        self.assertTrue(BM.get_all_user())

    def test_get_user(self):
        response = requests.get(URL_get_user_postman)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(json.loads(response.get_data().decode(sys.getdefaultencoding())), self.data)
        self.assertEqual(json.dumps(self.data), response.json)

    def test_medical_type(self):
        medical_type = {
            "company": "abc",
            "id": 1,
            "name": "vitamin"}
        test_client = self.app.test_client()
        response = test_client.get('http://127.0.0.1:3000/backend/medical-type/show/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.dumps(medical_type), response.data)

    def test_hello_world(self):
        response = self.app.get(URL_get_user_postman)
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())),
            self.data
        )

    def test_login(self):
        str=''
        user = json.dumps({
            "username": 'admin',
            "password": '123'
        })
        response = self.app.post('http://127.0.0.1:3000/backend/user/login', data=user, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)
        print(response.data)
        return bytes.fromhex(response.data.hex()).decode('utf-8')

    def test_login_customer(self):
        customer = json.dumps({
            "username": 'a1',
            "password": '123'
        })
        response = self.app.post('http://127.0.0.1:3000/backend/customer/login', data=customer, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)
        return bytes.fromhex(response.data.hex()).decode('utf-8')

    def test_insert_user(self):
        token = self.test_login()

        user = json.dumps({
            "name":"manager_4",
            "username":"manager_4",
            "password":"123",
            "confirm_password":"123",
            "role":"manager",
            "phone":"33332224444"})

        response = self.app.post('http://127.0.0.1:3000/backend/user/insert',data=user, headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 201)
        print(response.data)

    def test_insert_user_1(self):
        token = self.test_login()

        user = json.dumps({
            "name":"manager_4",
            "username":"manager_40",
            "password":"123",
            "confirm_password":"123",
            "role":"manager",
            "phone":"33332224444"})

        response = requests.post('http://127.0.0.1:3000/backend/user/insert',data=user, headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 201)
        print(response.request.body)

    def test_del_user(self):
        token = self.test_login()
        response = self.app.delete('http://127.0.0.1:3000/backend/user/delete/manager_40', headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 204)
        print(response.data)

    def test_update_user(self):
        user = json.dumps({
            "name": "staff",
            "role": "staff",
            "phone": "33333333343"})
        token=self.test_login()
        response = self.app.put('http://127.0.0.1:3000/backend/user/update/staff', data=user,
                                   headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 404)
        print(response.data)

    def test_insert_medical(self):
        medical = json.dumps({"name":"tyh",
            "type_name":"vitamin",
            "count":"22",
            "buy_price":"30000.0",
            "sell_price":"30000.0",
            "exp_date":"2022-06-01",
            "description":"asdf"})

        token = self.test_login()
        response = self.app.post('http://127.0.0.1:3000/backend/medical/insert', data=medical,
                                headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 201)
        print(response.data)

    def test_delete_medical(self):
        token = self.test_login()
        response = self.app.delete('http://127.0.0.1:3000/backend/medical/delete/12',
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 204)
        print(response.data)


    def test_update_medical(self):
        token = self.test_login()
        medical = json.dumps({
            "name":"tyh",
            "type_name":"vitamin",
            "count":"22",
            "buy_price":"30000.0",
            "sell_price":"30000.0",
            "exp_date":"2022-6-1",
            "description":"asdf"})

        response = self.app.put('http://127.0.0.1:3000/backend/medical/update/10', data=medical,
                                   headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 202)
        print(response.data)

    def test_add_to_cart(self):
        token = self.test_login_customer()
        medical = json.dumps({
            "medical_id":"2",
            "count":"2"})
        response = self.app.post('http://127.0.0.1:3000/backend/cart/add', data=medical,
                                headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 201)
        print(response.data)

    def test_show_cart(self):
        token = self.test_login_customer()
        response = self.app.get('http://127.0.0.1:3000/backend/cart/show',
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 200)
        print(response.data)