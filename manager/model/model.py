from datetime import datetime
from sqlalchemy.orm import relationship, backref
from manager.extension import db
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey


class Role(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    users = relationship('ManagerUser', backref='role', lazy=False)


class ManagerUser(db.Model):
    id = Column(Integer, primary_key=True, autoincrement = True)
    name = Column(String(45), nullable=False)
    username = Column(String(45), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    role_id = Column(Integer, ForeignKey(Role.id), nullable=False)
    phone = Column(String(45), nullable=False)
    join_date = Column(Date, nullable=False, default=datetime.now())


class Customer(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    username = Column(String(45), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    address = Column(String(45), nullable=False)
    phone = Column(String(45), nullable=False)
    join_date = Column(Date, nullable=False, default=datetime.now())
    bills = relationship('Bill', backref='customer', lazy=False)


class MedicalType(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    company = Column(String(45), nullable=False)
    medicals = relationship('Medical', backref='medicaltype', lazy=False)


class Medical(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    type_id = Column(Integer, ForeignKey(MedicalType.id), nullable=False)
    count = Column(Integer, nullable=False)
    buy_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    exp_date = Column(Date, nullable=False)
    description = Column(String(255))
    bills = relationship('BillDetail', backref='medical')


class Bill(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    status = Column(Integer, nullable=False, default=0)
    added_on = Column(Date, nullable=False, default=datetime.now())
    medicals = relationship('BillDetail', backref='bill')


class BillDetail(db.Model):
    bill_id = Column(ForeignKey(Bill.id), primary_key=True)
    medical_id = Column(ForeignKey(Medical.id), primary_key=True)
    count = Column(Integer, nullable=False, default=1)
    added_on = Column(Date, nullable=False, default=datetime.now())

