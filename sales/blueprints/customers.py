
#Python Modules
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy import desc
from flask import render_template, redirect, url_for, flash, request, Blueprint
from sqlalchemy.exc import IntegrityError
#Own Modules
from ..process import *
from ..extensions import db
from ..models.models import Customers_database
from ..forms import Login_form


customers = Blueprint('Customers', __name__)
@customers.route('/customers/<ref_id>', methods=['GET', 'POST'])
@login_required
def Add_Customer(ref_id):
    try:
        form_details = dict(request.form)
        form_details['User'] = current_user.username.title()
        form_details.pop('csrf_token')
        if  form_details.get("addNew") == "SAVE":
            del form_details["addNew"]
            last_db_row = Customers()
            form_details["Ref_id"] = form_details.get("First_Name")[0].upper() + form_details.get("Last_Name")[0].upper() + str(last_db_row.id + 1)
            if Search(form_details.get("Contact_No")).get('customers') != []:
                flash(f'{form_details.get("Contact_No")} already exist, please search customer with the number!',
                category='danger')
                return redirect(url_for('Customers.New_Customer'))
            else:
                Save_Customer(form_details)
                ref_id = form_details.get("Ref_id")
                flash(f'{Get_Customer_ByRef_Id(ref_id).First_Name.title()} has been successfully ADDED to our database!',
                        category='success')
                return redirect(url_for('Accounts.Accounts', ref_id= ref_id))
            #new_customer_details(form_details)
        elif form_details.get("addNew") == "UPDATE":
            del form_details["addNew"]
            Update_Customer(form_details, ref_id)
            flash(f'{form_details.get("First_Name").title()} has been successfully UPDATED to our database!',
                    category='success')
            return redirect(url_for('Accounts.Accounts', ref_id= ref_id))
    except IntegrityError as Err:
        flash(f"Error: {Err} This number {form_details.get('Contact_No')} already exist. Please search for existing customer",
               category="danger")
        return redirect(url_for("Customers.New_Customer"))


# Adds Customer details to Accounts page
@customers.route('/modify_customer/<ref_id>', methods=['GET', 'POST'])
@login_required
def Edit_Customer(ref_id):
    return render_template("customer.html", login_form= Login_form(),
                           customer_details= Get_Customers(ref_id), ref_id= ref_id, mode= "edit")


#Go to Customer form to create a new customer
@customers.route('/new_customer', methods=['GET', 'POST'])
@login_required
def New_Customer():
    return render_template("customer.html", login_form= Login_form(),
                           ref_id= Customers_database.query.count(), mode="save")