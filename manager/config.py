from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:trafalgarlaw1910@localhost/medical_store_management?charset=utf8mb4"
app.secret_key = 'asfsfe2r23rfad@afwefwef131wfafd!'

SQLALCHEMY_TRACK_MODIFICATIONS = False