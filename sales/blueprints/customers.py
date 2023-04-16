#Python Modules
from flask_login import login_required, current_user
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, Blueprint
from sqlalchemy.exc import IntegrityError
#Own Modules
from ..process import Get_Customers 
from ..exts import db
from ..models.models import Customers_database
from ..forms import Login_form

customers = Blueprint('Customers', __name__)

#Adds Customer details to Accounts page
@customers.route('/customers/<int:id>', methods=['GET', 'POST'])
@login_required
def Add_Customer(id):
    #Avoid adding existing number error
    try:
        print(id, "Add Customers")
        if request.form.get("addNew") == "Add Customer":
            #Save customer details to database
            db_customers= Customers_database(
                        title= request.form.get("title"), First_Name= request.form.get("first_name"),
                        Last_Name= request.form.get("last_name"), Contact_No= request.form.get("phone"),
                        Tel_No= request.form.get("alt-phone"), Email_Address= request.form.get("your_email"),
                        Street_Address= request.form.get("street"), Area= request.form.get("zip"),
                        City= request.form.get("place"), Country= request.form.get("country"),
                        User= current_user.username.title()
                        )
            db.session.add(db_customers)
            db.session.commit()
            flash(f'{db_customers.First_Name} has been successfully ADDED to our database!', category='success')
            db_customers=Customers_database.query.filter_by(Contact_No=db_customers.Contact_No).first()
            return redirect(url_for('Accounts.Accounts', id= db_customers.id))
        else: 
            #adding a new account from existing customer
            customer_details= Get_Customers(id)
            return redirect(url_for('Accounts.Accounts', id= id))       
    except IntegrityError:
        customer_details= Get_Customers(id)
        flash (f"This number {request.form.get('phone')} already exist. Please search for existing customer",
               category="danger")
        return render_template("customer.html", login_form= Login_form(), id=id, customer_details= customer_details )    
#Adds Customer details to Accounts page
@customers.route('/modify_customer/<int:id>', methods=['GET', 'POST'])
@login_required
def Edit_Customer(id):
    print("Customer")
    if request.form.get("addNew") == "Save":
        customer_details= Get_Customers(id)
        #Save customer details to database
        update_customer= Customers_database.query.get_or_404(id)
        update_customer.First_Name, update_customer.Last_Name = request.form.get("first_name"), request.form.get("last_name")
        update_customer.Contact_No, update_customer.Tel_No= request.form.get("phone"), request.form.get("alt-phone")
        update_customer.title, update_customer.Email_Address= request.form.get("title"), request.form.get("your_email")
        update_customer.User= current_user.username.title()
        update_customer.Street_Address, update_customer.Area= request.form.get("street"), request.form.get("zip")
        update_customer.City, update_customer.Country= request.form.get("place"), request.form.get("country"),
        db.session.commit()
        flash(f'{update_customer.First_Name} has been successfully UPDATED to our database!', category='success')
        return redirect(url_for('main.home', id=id))
#Go to Customer form to create a new customer
@customers.route('/new_customer', methods=['GET', 'POST'])
@login_required
def New_Customer():
    id= 0
    return render_template("customer.html", login_form= Login_form(), id= id)  