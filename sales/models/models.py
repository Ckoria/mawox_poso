#Python Modules
from datetime import datetime
#Own Modules
from ..exts import db

class Products(db.Model):
    #Creating a Database for items
    id = db.Column(db.Integer(), primary_key = True, unique= True)
    Product_Name = db.Column(db.String(length=30), nullable = False)
    Product_Price = db.Column(db.Integer(), nullable = False)

#Create database and relationships
class Customers_database(db.Model):
    #Creating a Database for items
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(), nullable = False)
    First_Name = db.Column(db.String(length=30), nullable = False)
    Last_Name = db.Column(db.String(length=30), nullable = False)
    Contact_No = db.Column(db.String(length=10), nullable = False, unique = True)
    Tel_No = db.Column(db.String(), nullable = True)
    Email_Address = db.Column(db.String(), nullable = True)
    Street_Address = db.Column(db.String(), nullable = False)
    Area = db.Column(db.String(), nullable = False)
    City = db.Column(db.String(), nullable = False)
    Country = db.Column(db.String(), nullable = False)
    Date_Created = db.Column(db.String(), default= datetime.now, nullable = False)
    Date_Updated = db.Column(db.DateTime(), default= datetime.now, onupdate= datetime.now, nullable = False)
    Accounts = db.relationship('Accounts_database', backref='reference')
    User = db.Column(db.String(), nullable = False)


class Accounts_database(db.Model):
    #Creating a Database for Accounts
    id = db.Column(db.Integer(), primary_key = True)
    Type = db.Column(db.String(), nullable = False)
    Quantity = db.Column(db.Integer(), nullable = False)
    Remainder = db.Column(db.Integer(), nullable = False)
    Delivered = db.Column(db.Integer(), nullable = False)
    Status = db.Column(db.String(), nullable = False)
    Date_Created = db.Column(db.String(), default= datetime.now, nullable = False)
    Date_Updated = db.Column(db.DateTime(), default= datetime.now, onupdate= datetime.now, nullable = False)
    Customers_id = db.Column(db.Integer, db.ForeignKey('customers_database.id'), nullable = False)
    Payments = db.relationship('Payments_database', backref='reference')
    User = db.Column(db.String(), nullable = False)
    
class Payments_database(db.Model):
    #Creating a Database for Payments
    id = db.Column(db.Integer(), primary_key = True)
    Transtion_Type = db.Column(db.String(), nullable = False)
    Balance = db.Column(db.Integer(), nullable = False)
    Paid = db.Column(db.Integer(), nullable = False)
    Amount = db.Column(db.Integer(), nullable = False)
    Status = db.Column(db.String(), nullable = False)
    Date_Created = db.Column(db.String(), default= datetime.now, nullable = False)
    Date_Updated = db.Column(db.DateTime(), default= datetime.now, onupdate= datetime.now, nullable = False)
    Accounts_id = db.Column(db.Integer(), db.ForeignKey('accounts_database.id'), nullable = False)
    User = db.Column(db.String(), nullable = False)
    
    