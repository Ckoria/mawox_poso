#Python Modules
from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from threading import Thread
import requests

#Own Modules
from .models.users import Users
from sales.models.models import *
from .extensions import db
from .forms import Register_form, Login_form
from .dash_data import *
from .gsheet import switch_backlog_sheets



main = Blueprint('main', __name__)
#Handling Home Page Information
@main.route('/')
@main.route('/home', methods= ['GET', 'POST'])
@login_required
def home():
    curr_date = my_days()[1]
    new_customers = {
        'no_of_customers'       : recent_customers(),
        'no_of_accounts'        : len(active_accounts("Active", 'Delivery')),
        'scheduled'             : len(today_schedule(curr_date)),
        'Unrecovered_Balances'  : f'{sum(Unrecovered_Balances())}'
        }
    return render_template('index.html', log_form= Login_form(),
    counts = new_customers, curr_date = curr_date,
    sales_qty= number_of_sales().get('products_data'))


@main.route('/reload', methods= ['GET', 'POST'])
@login_required
def reload_data_spreadsheet():
    if current_user.username.lower() == 'philile' or current_user.username.lower() == 'admin':
        time_taken = switch_backlog_sheets()
        flash(f'Successfully updated, bheka iSpreadsheet 👊', category='success')
    else:
        flash(f'Access denied🚷. Contact admin.', category='danger')
    return redirect(url_for('main.home'))


#Handling Registration process
@main.route('/register/nBbODq6YUEDojrj3HyeBZcXafcxopDqoF8dB0klA9OAzvDoqv', methods= ['GET','POST'])
def register_page():
    reg_form = Register_form()
    if reg_form.validate_on_submit():
        user_to_create = Users(username= reg_form.username.data,
                              email= reg_form.email.data,
                              password= reg_form.pwd_1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'{user_to_create.username} has successfully registered and logged in! 👊', category='success')
        return redirect(url_for('main.home'))
    #if there are errors from validations, write on log file
    if reg_form.errors != {}:
        for err_msg in reg_form.errors:
            flash(f'There was an error while trying to create the account! Please check your {err_msg}. 🚷',
                  category='danger')

    return render_template('register.html', form= reg_form)

#Handling Login process
@main.route('/login', methods= ['GET','POST'])
def login_page():
    log_form = Login_form()
    if log_form.validate_on_submit():
        login_attempt = Users.query.filter_by(username= log_form.username.data).first()
        if login_attempt and login_attempt.check_password_correction(pwd_attempt= log_form.pwd_1.data):
            login_user(login_attempt)
            flash(f'{login_attempt.username.title()} successfully logged in 💯!', category='success')
            return redirect(url_for('main.home'))
        else:
            flash(f'Either Username or Password is incorrect! Please try again ⛔', category='danger')
    return render_template('login.html', form= log_form)

#Handling Logout process
@main.route('/logout')
def logout_page():
    logout_user()
    flash('You have logged out ✌️.', category='info')
    return redirect(url_for('main.home'))