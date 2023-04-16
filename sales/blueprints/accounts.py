#Python Modules
from flask import render_template, flash, request, Blueprint, redirect, url_for
from datetime import datetime
from flask_login import login_required, current_user
#Own Modules
from ..models.models import Accounts_database, Products, Payments_database, Customers_database
from ..forms import  Login_form
from ..exts import db
from ..process import Get_Customers, Get_Products, Get_Accounts, Search, Search_Acc, Search_Payment

paid_amount = 0.00
added_products = [[paid_amount]]
account = Blueprint('Accounts', __name__)
clicked=''
#Collectes account details from html table
@account.route('/accounts/<int:id>', methods= ['POST', 'GET'])
@login_required
def Create_Account(id):
    customer_details= Get_Customers(id)
    curr_user, now= current_user.username.title(), (datetime.now()).strftime("%c")
    #After pressing Create Account Button
    if "btn_create" in request.form:
        for curr_account in added_products[0:-1]:
            if curr_account[2] == 0 and curr_account[4] == 0:
                status= "Closed"
            else:
                status= "Active"
            db_accounts= Accounts_database(
                    Type= curr_account[1],
                    Quantity= curr_account[2],
                    Remainder= curr_account[2],
                    Delivered= curr_account[2]-curr_account[2],
                    Status= status,
                    Customers_id= id,
                    User= curr_user
                    )
            db.session.add(db_accounts)
            db.session.commit()
            account_details= Get_Accounts(id)
            acc_id= account_details.get("id")
            db_payments= Payments_database(
                    Transtion_Type= request.form["payment_type"],
                    Balance= curr_account[4],
                    Paid= curr_account[5],
                    Amount= curr_account[6],
                    Status= status,
                    Accounts_id = acc_id,
                    User= curr_user
                    )
            db.session.add(db_payments)
            acc_id= acc_id +1
        db.session.commit()
        flash(f"New account has been created by {curr_user} on {now}",
              category="success")
    else:
        pass
    return render_template('accounts.html', log_form = Login_form(), added_products = added_products, 
    Curr_Date_Time= now, paid_amount= paid_amount, all_products= Get_Products(), customer_details=customer_details)

#Handling Deleting Products process
@account.route('/remove/<int:id>', methods= ['POST'])
@login_required
def Remove_Products(id, added_products= added_products):
    paid_amount= request.form.getlist('paid_amount')
    if "btn_del" in request.form:
        #get a list of checked items
        checked_items= request.form.getlist('checked')
        for item in checked_items:
            for product in added_products:
                tmp_total = added_products[-1][0]
                if item in product:
                    total = [(tmp_total - product[-1])]
                    added_products.pop(added_products.index(product))   
                    added_products[-1] = total
    elif 'btn_calc' in request.form:
        #Total amount for poducts on the added products list
        total_amount= (added_products[-1][0])
        #All products on the added products list 
        added_account= added_products[0:-1]
        tmp_account= []
        #Create a temporary account for all added products
        for i, items in enumerate(added_account):
            t_amount = items[-1]
            if paid_amount[i] == '':
                items.append(0)
                items.append(t_amount)
            else:
                items.insert(-1,t_amount-int(paid_amount[i]))
                items.insert(-1, int(paid_amount[i]))
            tmp_account.append(items)
        #Sum of paid amounts
        paid_amount = sum([(float(amount)) for amount in list(filter(lambda x: x != '', paid_amount))])
        tmp_account.append([total_amount-paid_amount, paid_amount, total_amount])
        added_products= tmp_account
        #added_products.insert([request.form])
    return render_template("accounts.html", log_form = Login_form(), added_products= added_products, 
                                all_products= Get_Products(), customer_details = Get_Customers(id))
    
#Handling Adding Products process
@account.route('/products/<int:id>', methods= ['POST'])
@login_required
def Add_Products(id):
    if "btn_add" in request.form: 
        #Selected product from a droplist
        selected_item  = request.form["select_product"]
        #Check if selected item has already been added to the list
        if any(selected_item in product for product in added_products):
            flash(f'{selected_item}, is already on the products', category="danger")
        #if the added products list is empty
        else:
            #added_products = [list of added products, total amount of all added products as last value]
            #list values, 0. id, 1. name, 2. quantity, 3. unit price, 4. total amount
            unit_price= float(Products.query.filter_by(Product_Name= selected_item).first().Product_Price)
            added= [Products.query.filter_by(Product_Name= selected_item).first().id,
                    Products.query.filter_by(Product_Name= selected_item).first().Product_Name,
                    int(request.form.get("item_no",  0)),
                    unit_price, int(request.form.get("item_no",  0)) * unit_price
            ]
            #take last items total
            tmp_total = added_products[-1]
            #Remove the last items total
            added_products.pop(len(added_products)-1) 
            added_products.append(added)
            #Update items total
            total_amount=[added_products[-1][-1]+tmp_total[0]]
            #Append new items total
            added_products.append((total_amount)) 
    else:
        flash(f'Please check added products...', category="danger")
    return render_template("accounts.html",log_form = Login_form(), all_products= Get_Products(),
                             added_products= added_products, customer_details = Get_Customers(id))       
    
@account.route('/account/<int:id>', methods= ['GET', 'POST'])
def Accounts(id):
    added_products = [[]]
    all_products= Get_Products()
    return render_template('accounts.html', log_form = Login_form(), Curr_Date_Time= (datetime.now()).strftime("%c"), 
        added_products= added_products, all_products = all_products, customer_details= Get_Customers(id))

#Search for customer details from all customers in database
@account.route('/search_results', methods= ['GET', 'POST'])
def search_customer(): 
    print("I was here to search")
    searched= request.form.get('search_target')
    if searched != '' and searched:
        results= Search(searched)  
    print("came back with no results")
    return render_template("tb_customers.html", form= Login_form(), results=results)

#Search for account details from a specific customer in database
@account.route('/search_accounts/<int:id>', methods= ['GET', 'POST'])
def Search_Accounts(id):
    acc_info, cust_info, totals= Search_Acc(id)
    return render_template("tb_accounts.html", form= Login_form(), 
            results=acc_info, cust_info=cust_info, totals=totals)

#Search for payments details from a specific accounts in database
@account.route('/search_payments/<int:id>', methods= ['GET', 'POST'])
def Search_Payments(id):
    pay_info, acc_info= Search_Payment(id)
    return render_template("tb_payments.html", form= Login_form(), results=pay_info, acc_info=acc_info)
    

