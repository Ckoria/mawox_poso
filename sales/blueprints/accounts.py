#Python Modules
from flask import render_template, flash, request, Blueprint, redirect, url_for
from datetime import date
from sqlalchemy import desc
from flask_login import login_required, current_user
import threading
#Own Modules
from ..models.models import Products, Payments_database, Customers_database
from ..forms import  Login_form
from ..exts import db
from ..process import *
from ..gsheet import *
from ..dash_data import *

# Working as expected
sheet = SPREADSHEET.worksheet('title','Products')
paid_amount = [0]
added_prods = [paid_amount]
n= 0
prods = {'ids':[id[0] for id in sheet.get_values('A2',"A100")],
            'prices': [price[0] for price in sheet.get_values('C2',"C100")],
            'all_products': [product[0] for product in sheet.get_values('B2',"B100")] ,
            'all': [product[0] for product in sheet.get_values('D2',"D100")]
            }


account = Blueprint('Accounts', __name__)
# Working as expected
@account.route('/accounts/<ref_id>', methods= ['POST', 'GET'])
@login_required
def Create_Account(ref_id: str, added_prods= added_prods):
    """_summary_

    Args:
        ref_id (str): _description_

    Returns:
        _type_: _description_
    """
    form = dict(request.form)
    form.pop('csrf_token')
    form['User']= current_user.username.title()
    day_scheduled = datetime.strptime(form.get('Delivery_Schedule'), '%Y-%m-%d')
    if ("btn_create" in form) and ("Transaction_Type" in form):
        if day_scheduled.date() >= my_days()[1] and len(today_schedule(day_scheduled.date())) < 10:
            form.pop('btn_create')
            receipt_to_db(added_prods, form, ref_id)
            receipt(ref_id, added_prods[0:-1], day_scheduled)
            added_prods = [[]]
            flash(f"New account has been created by {current_user.username.title()}.", category="success")
            cash_in()
            saveToPDF()
        else:
            flash("Please check if you selected the correct date", category="danger")
    else:
        flash("Please check if the transaction type was selected", category="danger")
    return redirect(url_for("Accounts.Search_Accounts", ref_id= ref_id))


# Working as expected
@account.route('/remove/<ref_id>', methods= ['POST'])
@login_required
def Remove_Products( ref_id: str, added_prods= added_prods):
    """_summary_

    Args:
        ref_id (str): _description_

    Returns:
        _type_: _description_
    """
    del_items= request.form
    if "btn_del" in del_items:
        added_prods, prods['all_products'] = Remove_Items( added_prods, prods.get('all_products'), del_items)
    elif 'btn_calc' in del_items:
        added_prods= Calc_Amount(added_prods, del_items.getlist('paid_amount'), [])
    return render_template("accounts.html", log_form = Login_form(), added_products = added_prods,
    all_products = prods.get('all_products'), customer_details = Get_Customers(ref_id),
    paid_amount = del_items.getlist('paid_amount'))


# Working as expected, Needs optimization
@account.route('/products/<ref_id>', methods= ['POST'])
@login_required
def Add_Products( ref_id: str, added_prods= added_prods):
    """_summary_
    Args:
        ref_id (str): _description_
        prods (_type_, optional): _description_. Defaults to prods.
    """
    added_items= request.form
    if "btn-add" in added_items and int(added_items.get("item_no",  0)) > 0:
        selected_item  = added_items["select_product"]
        if any(selected_item in prod for prod in added_prods):
            flash(f'{selected_item}, is already on the products',
                  category="danger")
        else:
            global prods
            added_prods = Get_Products(added_prods, prods,
                                       selected_item, added_items)
            prods.get('all_products').pop(
                prods.get('all_products').index(selected_item))
    else:
        flash("Please check if everything was selected", category="danger")
    return render_template("accounts.html", log_form = Login_form(), all_products = prods.get('all_products'),
            added_products= added_prods, customer_details = Get_Customers(ref_id), paid_amount = paid_amount)


# Working as expected
@account.route('/account/<ref_id>', methods= ['GET', 'POST'])
@login_required
def Accounts(ref_id: str, all_prods = prods['all']):
    """_summary_
    Args:
        ref_id (str): _description_
        all_prods (_type_, optional): _description_. Defaults to prods.get("all").
    """
    return render_template('accounts.html', log_form = Login_form(),
        added_products= added_prods, all_products = all_prods,
        customer_details= Get_Customers(ref_id), paid_amount = paid_amount)


# Working as expected
@account.route('/active_customers', methods= ['GET', 'POST'])
@login_required
def Active_Customers_Route():
    active_accs  = active_accounts("Active", 'Delivery')
    active_cust =  Active_Customers(active_accs, [])
    return render_template("search_customers.html", form= Login_form(),
                           results =active_cust, no_rst_msg="")


@account.route('/unpaid', methods= ['GET', 'POST'])
@login_required
def Unpaid_Balances():
    return render_template("search_customers.html", form= Login_form(),
                           results = Unrecovered_Balances(active_accounts("Closed", "")), no_rst_msg="")


# Working as expected
@account.route('/recent_customers', methods= ['GET', 'POST'])
@login_required
def Recent_Customers():
    tmp_storage= []
    search_results= Limit_Entries(recent_customers(), tmp_storage)
    return render_template("search_customers.html", form= Login_form(),
                           results = search_results, no_rst_msg="")


@account.route('/my_schedule/', methods= ['GET', 'POST'])
@login_required
def Scheduled_Accounts():
    selected_date = request.form.get('selected_date')
    if selected_date == '':
        current_day = my_days()[1]
    else:
        current_day = selected_date
    results = today_schedule(current_day)
    if len(results) >= 5:
        msg = 'Fully Scheduled'
    else:
        msg = f'Not fully Scheduled, {len(results)} scheduled yet.'
    return render_template("search_customers.html", form= Login_form(),
                           results= results, no_rst_msg=msg)


# Working as expected
@account.route('/search_results', methods= ['GET', 'POST'])
@login_required
def Search_Customer():
    searched= request.form.get('search_target')
    if searched == None:
        searched = "0"
    search_results= (Search(searched).get('customers'))
    if search_results == []:
        no_rst_msg= "No Results Found"
    else:
        no_rst_msg = ""
    return render_template("search_customers.html", form= Login_form(),
                           results = search_results, no_rst_msg=no_rst_msg)


# Working as expected
@account.route('/search_accounts/<ref_id>', methods= ['GET', 'POST'])
@login_required
def Search_Accounts(ref_id):
    info, notes  = Search_Acc(ref_id), Get_Notes(ref_id)
    acc_info= info.get('acc_details')[1]
    return render_template("search_accounts.html", form= Login_form(), total_payments = info.get('acc_details')[0],
                results = acc_info.get('acc_info'), cust_info = info.get('customer_info'), notes = notes.get("notes"))


# Working as expected
@account.route('/search_payments/<int:acc_id>', methods= ['GET', 'POST'])
@login_required
def Search_Payments(acc_id):
    get_payment_info = Search_Payment(acc_id)
    pay_info= Get_Payments(acc_id, [])
    return render_template("search_payments.html", form = Login_form(), acc_info = get_payment_info.get('acc_info'),
            payments= pay_info.get('payments_info'), ref_id= get_payment_info.get('cust_info'))


# Working as expected
@account.route('/process/payments/<int:acc_id>', methods= ['GET', 'POST'])
@login_required
def Pay_Balance(acc_id):
    get_payment_info = Search_Payment(acc_id)
    pay_info, frm_details = get_payment_info.get('payment_info'), dict(request.form)
    del frm_details['csrf_token']
    frm_details['User']= current_user.username.title()
    Balance_Details(frm_details, pay_info)
    pay_info= Get_Payments(acc_id, [])
    cash_in()
    return render_template("search_payments.html", form = Login_form(), payments= pay_info.get('payments_info'),
            ref_id= get_payment_info.get('cust_info'), acc_info = get_payment_info.get('acc_info') )


# Working as expected
@account.route('/payments/search_accounts/<ref_id>', methods= ['GET', 'POST'])
@login_required
def Payments_Update(ref_id):
    receipt_update(ref_id)
    return redirect(url_for("Accounts.Search_Accounts", ref_id= ref_id))


# Works as expected, needs optimization
@account.route('/delivery/<ref_id>', methods= ['GET', 'POST'])
@login_required
def Delivery(ref_id):
    try:
        frm = request.form
        if frm.get("Receipt") == "Deliver":
            info = Search_Acc(ref_id)
            acc_info= info.get('acc_details')[1].get("acc_info")
            scheduled_day = datetime.strptime(frm.get('form_date'), '%Y-%m-%d')
            handle_delivery(scheduled_day, frm, acc_info)
            driver = frm.get('form_driver')
            # Get all items that have been delivered today
            delivered_today = get_today_delivery(datetime.today(), ref_id)
            payment_info = info.get('acc_details')[0]
            delivery_to_invoice(ref_id, delivered_today, payment_info, scheduled_day, driver)
        elif frm.get("Receipt") == 'Generate_Receipt':
            generate_receipt(ref_id)

    except Exception as unknown:
        flash(f'😬Ooops something went wrong please try again!', category='danger')

    return redirect(url_for("Accounts.Search_Accounts", ref_id= ref_id))


# Works as expected
def handle_delivery(scheduled_day: date, frm: tuple, acc_info: list):
    if len(today_schedule(scheduled_day)) < 10 and scheduled_day.date() >= my_days()[1]:
        acc_info= [acc for acc in (acc_info)
        if acc.get("Type") != "Delivery" and acc.get("Remainder") != 0] #
        Save_Delivery(acc_info, frm)
        flash('Danko 👌! The items has been successfully delivered.', category='success')
    else:
        flash('🙈Ooops! Date selected is ether full or past date!', category='danger')


# Works as expected
@account.route('/delivery/delivered/<int:acc_id>', methods= ['GET', 'POST'])
def Get_Delivery(acc_id):
    delivery_info= Search_Delivery(acc_id)
    return render_template("delivery.html", acc_info= delivery_info.get('acc_info'),
                           delivery_info= delivery_info.get('delivery_info'))


@account.route('/delete_account/<int:acc_id>', methods= ['GET', 'POST'])
@login_required
def delete_record(acc_id):
    account = Account_Summary(acc_id)
    usr = (current_user.username).lower()
    if usr == 'admin' or usr == 'philile':
        delete_account(account)
        flash('Account has been successfully removed! ',
        'success')
    else:
        flash('Please login as admin! ',
        'warning')
    return redirect(url_for("Accounts.Search_Accounts",
                            ref_id= account.Customers_id))



# Works as expected
@account.route('/postnotes/<ref_id>', methods= ['GET', 'POST'])
@login_required
def Post_Notes(ref_id):
    info = Search_Acc(ref_id)
    acc_info= info.get('acc_details')[1]
    note_body = dict(request.form)
    note_body['User']= current_user.username.title()
    note_body['Cust_id']= ref_id
    if 'post_note' in request.form:
        Save_Notes(note_body)
    return render_template("search_accounts.html", form= Login_form(), 
                           results=acc_info.get('acc_info'), cust_info = info.get('customer_info'), 
                           total_payments = info.get('acc_details')[0], notes = Get_Notes(ref_id).get("notes"))


# Works as expected, needs optimization
@account.route('/generate/receipt/<ref_id>', methods= ['GET', 'POST'])
@login_required
def generate_receipt(ref_id):
    frm = dict(request.form)
    selected_date = datetime.strptime(frm.get('form_date'), '%Y-%m-%d')
    pay_details = get_targeted_receipt(selected_date, ref_id )
    receipt(ref_id, pay_details, None)
    flash('Receipt has been successfully generated, please go to receipts.', category='success')
    return redirect(url_for("Accounts.Search_Accounts", ref_id= ref_id))


# Works as expected
@account.route('/expenses/expense', methods= ['GET', 'POST'])
@login_required
def Xpenses():
    no_results, data= "", dict(request.form)
    data['User']= current_user.username.title()
    if data.get("add") == "Save":
        Save_Xpenses(data)
        flash("The record has been saved 👍", "success")
    xpenses= Get_All_Expenses()
    record_xpenses()
    if len(xpenses) > 0:
        expenses_info= xpenses.get("expenses")
    else:
        no_results = "🤷️No records found for this month."
    return render_template("expenses.html", form= Login_form(), expenses= expenses_info, no_results= no_results)

# Works as expected
@account.route('/notes', methods= ['GET', 'POST'])
@login_required
def Notes():
    notes = []
    notes_info = all_notes()
    old_date = datetime.now()
    for note in notes_info:
        tmp_notes = Get_Notes(note.Cust_id).get('notes')[0] # Most recent note per customer
        nold_date = datetime.now()
        if tmp_notes.get('Status') != 'Resolved':
            # names = Search_Acc(note.Cust_id).get('customer_info')
            # tmp_notes['fname'] = names['First_Name']
            # tmp_notes['lname'] = names.get('Last_Name', '')
            notes.append(tmp_notes)
            print(datetime.now() - nold_date)
    print(datetime.now() - old_date)
    return render_template("notes.html", form= Login_form(), notes= notes)