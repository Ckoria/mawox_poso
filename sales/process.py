from sales.models.models import *
from datetime import date
from flask import flash
import calendar

# The following information process data during the invoice creation
# ----------------------------------------------------------------
# get product details from database

def Get_Products(added_products, products, selected_item, form):
    unit_price = float(products.get("prices")[products.get("all").index(selected_item)])
    added = [products.get("ids")[products.get("all").index(selected_item)],
            selected_item, int(form.get("item_no",  0)),
            unit_price, int(form.get("item_no",  0)) * unit_price]
    if added != []:
        tmp_total = added_products[-1]
        added_products.pop(len(added_products)-1)
        added_products.append(added)
        total_amount = [ added_products[-1][-1] + tmp_total[0] ]
        added_products.append((total_amount))
    return added_products


def Calc_Amount(added_products, paid_amount, tmp_account):
    total_amount= (added_products[-1][0])
    added_account= added_products[0:-1]
    for i, items in enumerate(added_account):
        t_amount = items[-1]
        tmp_account= calculate_amount(paid_amount, t_amount, items, tmp_account, i)
    paid_amount = sum([(float(amount)) for amount in list(filter(lambda x: x != '', paid_amount))])
    tmp_account.append([total_amount-paid_amount, paid_amount, total_amount])
    return tmp_account


def calculate_amount(paid_amount: list, t_amount: float, items: list, tmp_account: list, i: int) -> list:
    if paid_amount[i] == '':
            items.append(0)
            items.append(t_amount)
    else:
        items.insert(-1,t_amount-float(paid_amount[i]))
        items.insert(-1, float(paid_amount[i]))
    if len(items) > 7:
        items.pop(4)
        items.pop(4)
    tmp_account.append(items)
    return tmp_account


def receipt_to_db(added_prods: list, form: dict, ref_id: str):
    for curr_account in (added_prods[0:-1]):
        Account_Info(form, ref_id, curr_account, {})
        Pay_Info(form, curr_account, {})
        Delivery_Info(form, curr_account[2], {"Delivered": 0})


def Remove_Items(added_products, all_products, form_data):
    checked_items= form_data.getlist('checked')
    for item in checked_items:
        all_products.append(item)
        for product in added_products:
            tmp_total = added_products[-1][0]
            if item in product:
                total = [(tmp_total - product[-1])]
                added_products.pop(added_products.index(product))
                added_products[-1] = total
    return added_products, all_products


def Save_Delivery(acc_info, frm_deliver):
    driver = frm_deliver.get('form_driver')
    tmp= frm_deliver.getlist("Qty")
    for i, acc in enumerate(acc_info):
        for key in ["_sa_instance_state", "Type",
            "Quantity","Date_Updated", "Customers_id", "Payments"]:
            del acc[key]
        if  tmp[i] != "":
            acc.update({'Delivered': int(acc.get('Delivered')) + int(tmp[i]),
                        'Remainder': int(acc.get('Remainder')) - int(tmp[i]),
                        'Delivery_Schedule':frm_deliver.get('form_date')})
            if int(acc.get('Remainder')) == 0:
                acc.update({"Status": "Closed"})
            Update_Account(acc)
            acc.update({'Delivered': int(tmp[i])})
            acc.update({'Drivers_Name': driver.title()})
            acc['Accounts_id'] = acc.pop("id")
            del acc[ "Status"]
            Add_Delivery(acc)

# ----------------------------------------------------------------
#Adding Customer details to a database
def Save_Customer(cust_info):
    db.session.add(Customers_database(**cust_info))
    db.session.commit()

# ----------------------------------------------------------------

# ADDING DATA TO DATABASE
# ----------------------------------------------------------------
#Save Private Note to the database
def Save_Notes(note_body):
    del note_body['csrf_token']
    del note_body['post_note']
    db.session.add(SpecialNotes(**note_body ))
    db.session.commit()

# ----------------------------------------------------------------
def Save_Xpenses(data):
    del data['add']
    del data['csrf_token']
    db.session.add(Expenses( **data))
    db.session.commit()

# ----------------------------------------------------------------
def Add_Payment(pay_form):
    db.session.add(Payments_database(**pay_form))
    db.session.commit()

# ----------------------------------------------------------------
def Add_Account(acc_form):
    db.session.add(Accounts_database(**acc_form))
    db.session.commit()

# ----------------------------------------------------------------
def Add_Delivery(delivery_frm):
    db.session.add(Delivery_database(**delivery_frm))
    db.session.commit()

# ----------------------------------------------------------------

# ---------------------- DELETE ACCOUNT ---------------------------

def delete_payment(account):
    for del_target in account.Payments:
        db.session.delete(del_target)


# ----------------------------------------------------------------
def delete_delivery(account):
    for del_target in account.Delivery:
        db.session.delete(del_target)


# ----------------------------------------------------------------
def delete_account(account):
    delete_payment(account)
    delete_delivery(account)
    db.session.delete(account)
    db.session.commit()


# UPDATING DATA TO DATABASE
# ----------------------------------------------------------------
# Update customer information in a database
def Update_Customer(cust_info, ref_id):
    update_target= Customers_database.query.filter_by(Ref_id = ref_id).first()
    for key, value in cust_info.items():
        setattr(update_target, key, value)
    db.session.commit()

# ----------------------------------------------------------------
# Update Accounts information in a database
def Update_Account(acc_info):
    update_target= Accounts_database.query.filter_by(id = acc_info.get('id')).first()
    for key, value in acc_info.items():
        setattr(update_target, key, value)
    db.session.commit()

# PROCESS DATA FROM DB INSTANCE

# ----------------------------------------------------------------------------
#Get all special notes attached to a customer id from the database
def Get_Notes(ref_id):
    all_notes = []
    for note in Get_Customer_ByRef_Id(ref_id).Notes:
        all_notes.append(dict(note.__dict__))
    all_notes.reverse()
    return {"notes" : all_notes}


# ----------------------------------------------------------------------------
# Get all special notes from the database
def all_notes():
    return SpecialNotes.query.group_by(
        SpecialNotes.Cust_id).order_by(
            SpecialNotes.Date_Created.desc())

# ---------------------------------------------------------------------------
def Get_All_Expenses():
    no_of_days, curr_date = my_days()
    xpenses  = []
    all_xpenses = All_Expenses(curr_date, no_of_days)
    for expense in all_xpenses:
        xpenses.append(dict(expense.__dict__))
    xpenses.reverse()
    return {"expenses": xpenses}

# ---------------------------------------------------------------------------
# Returns accounts, customer details summary, total amounts
def Search_Acc(ref_id) -> dict:
    return {'customer_info': Get_Customers(ref_id),
            'acc_details': Calc_Acc_Totals(0, 0, [], ref_id) }

# --------------------------------------------------------------------------
 #Limit number of customers to 30 per page
def Limit_Entries(customers_query_results, tmp_storage) -> list:
    for customer_query_instance in customers_query_results:
        if len(tmp_storage) <= 30:
            tmp_storage.append(Sort_Phone(dict(customer_query_instance.__dict__)))
        else:
            break
    return tmp_storage

# ------------------------------------------------------------------------

# Returns payment information and account summary
def Search_Payment(acc_id):
    account = Account_Summary(acc_id)
    if len(account.Payments) > 0:
        pay= (account.Payments)[-1]
    else:
        pay= (account.Payments)
    payment= dict(pay.__dict__)
    del payment['_sa_instance_state']
    return { 'payment_info': payment,
             'acc_info': dict(account.__dict__),
             'cust_info' : account.Customers_id }

# ------------------------------------------------------------------------
def Search_Delivery(account_id) -> dict:
    account = Account_Summary(account_id)
    return { 'delivery_info': Get_Delivery_Details(account, []),
             'acc_info': dict(account.__dict__),
             'cust_info' : account.Customers_id }

# ---------------------------------------------------------------------
#Returns dictionary from DB instance
def Get_Customers(ref_id) -> dict:
    return dict(Get_Customer_ByRef_Id(ref_id).__dict__)

# --------------------------------------------------------------------

def Get_Payments(acc_id, payments_list) -> dict:
    for payment in Payment_Details(acc_id):
        payments_list.append(dict(payment.__dict__))
    payments_list.reverse()
    return {'payments_info': payments_list}


# --------------------------------------------------------------------
def Get_Delivery_Details(account, delivery_list) -> list:
    for deliver in account.Delivery:
        delivery_list.append(dict(deliver.__dict__))
    delivery_list.reverse()
    return delivery_list


# RETRIEVE DATA FROM DATABASE THEN RETURN DB INSTANCE FOR LAST ROW
# --------------------------------------------------------------------
def Get_Account():
    return Accounts_database.query.order_by(
        Accounts_database.id.desc()).first()


# --------------------------------------------------------------------
def Get_Payment():
    return Payments_database.query.order_by(
        Payments_database.id.desc()).first()


def get_today_payment(curr_day):
    return db.session.query(Accounts_database.Type, Payments_database.Paid, Payments_database.Transaction_Type
                            ).join(Payments_database). \
            filter(Payments_database.Date_Updated >= (curr_day)).all()


def get_today_delivery(curr_day, ref_id ):
    curr_day = curr_day.strftime("%Y-%m-%d")
    return db.session.query( Accounts_database.Type, Delivery_database.Delivered,
                            Delivery_database.Remainder, Accounts_database.Quantity
                            ).join(Delivery_database).join(Customers_database). \
            filter(Delivery_database.Date_Updated >= str(curr_day),
                   Customers_database.Ref_id == ref_id).all()


def get_targeted_receipt(curr_day, ref_id ):
    return db.session.query(Accounts_database.id, Accounts_database.Type, Accounts_database.Quantity,
                            (Payments_database.Amount / Accounts_database.Quantity),
                            Payments_database.Balance, Payments_database.Paid,  Payments_database.Amount
                            ).join(Payments_database).join(Customers_database). \
            filter(Payments_database.Date_Updated >= str(curr_day),
                   Customers_database.Ref_id == ref_id).all()


# --------------------------------------------------------------------
def Customers():
    return Customers_database.query.order_by(
        Customers_database.id.desc()).first()


# --------------------------------------------------------------------
# Returns DB instance for Accounts
def Account_Summary(account_id):
    return Accounts_database.query.filter(
        Accounts_database.id == account_id).first()

# --------------------------------------------------------------------
# Returns DB instance for Payments
def Payment_Details(acc_id):
    return  Payments_database.query.filter(
        Payments_database.Accounts_id == acc_id).all()

# --------------------------------------------------------------------
def Last_Payment_Details(acc_id):
    return  Payments_database.query.filter(
        Payments_database.Accounts_id == acc_id).first()

# --------------------------------------------------------------------
#Returns Customer details DB instance
def Get_Customer_ByRef_Id(ref_id):
    return  Customers_database.query.filter_by(
        Ref_id=ref_id).first()

# RETURN MULTIPLE DB INSTANCES
# --------------------------------------------------------------------
# Only returns customers details based on a search keyword
def Search(searched) -> dict:
    return {
        'customers': Limit_Entries(
            Customers_database.query.filter(
            Customers_database.id.like('%'+searched+'%') |
            Customers_database.Ref_id.like('%'+searched+'%') |
            Customers_database.Contact_No.like('%'+searched+'%')|
            Customers_database.First_Name.like('%'+searched+'%')|
            Customers_database.Last_Name.like('%'+searched+'%') |
            Customers_database.Date_Created.like('%'+searched+'%')|
            Customers_database.User.like('%'+searched+'%')
            ).order_by(
                        Customers_database.Date_Updated.desc()
            ).all(),
            [] )
        }


# --------------------------------------------------------------------

def All_Expenses(curr_date, no_of_days):
    return Expenses.query.filter(
        Expenses.Date_Created >= (date(curr_date.year, curr_date.month, 1))
        ).all()

# CLEAN UP DATA
# --------------------------------------------------------------------
def Sort_Phone(customer) -> dict:
    if (customer.get("Contact_No") != None and "/" in (customer.get("Contact_No"))   ):
        customer.update({'Tel_No': customer.get("Contact_No").split("/")[1]})
        customer.update({'Contact_No': customer.get("Contact_No").split("/")[0]})
    return customer

# ----------------------------------------------------------------
def Balance_Details(frm_details, pay_info):
    if  frm_details.get('payBtn') == 'Pay' and frm_details.get('Transaction_Type') != None:
        if float( frm_details.get("Paid")) > float(pay_info.get("Balance")):
            flash('Please check the amount entered!', category='danger')
        else:
            del pay_info['id']
            pay_info.update({'Transaction_Type': frm_details.get('Transaction_Type'),
                             'Paid': frm_details.get('Paid'), 'Date_Updated': datetime.now(),
                             'Balance': float(pay_info.get('Balance')) - float(frm_details.get('Paid'))})
            Add_Payment(pay_info)
            flash('The payment has been successfully updated.', category='success')
    else:
        flash('Please check if you selected type of payment!', category='danger')

# ----------------------------------------------------------------
def my_days() -> date:
    curr_date= (date.today())
    days = calendar.monthrange(curr_date.year, curr_date.month)[1]
    return days, curr_date

# ----------------------------------------------------------------
def Status_Check(pay_form):
    if (pay_form.get("Balance") == 0):
        pay_form["Status"] = "Closed"
    else:
        pay_form["Status"] = "Active"

# ----------------------------------------------------------------
def Account_Info(form, ref_id, curr_account, acc_form):
    acc_form["Type"]= curr_account[1]
    acc_form["Remainder"]= acc_form["Quantity"]= curr_account[2]
    acc_form["Customers_id"]= ref_id
    acc_form["Delivered"]= 0
    acc_form["Delivery_Schedule"]= form.get('Delivery_Schedule')
    acc_form["Status"] = "Active"
    acc_form["Date_Updated"] = datetime.now()
    acc_form["User"]= form.get('User')
    Status_Check(acc_form)
    Add_Account(acc_form)

# ----------------------------------------------------------------
def Pay_Info(form, curr_account, pay_form):
    pay_form['Transaction_Type']= form.get('Transaction_Type')
    pay_form["Balance"]= curr_account[4]
    pay_form["Paid"]= curr_account[-2]
    pay_form["Amount"]= curr_account[-1]
    pay_form["Date_Updated"]= datetime.now()
    pay_form["Accounts_id"]= Get_Account().id
    pay_form["User"]= form.get('User')
    Status_Check(pay_form)
    Add_Payment(pay_form)

# ----------------------------------------------------------------
def Delivery_Info(form, remainder, delivery_frm):
    delivery_frm['Remainder']= remainder
    delivery_frm["Delivery_Schedule"]= form.get('Delivery_Schedule')
    delivery_frm["Date_Updated"]= datetime.now()
    delivery_frm["User"]= form.get('User')
    delivery_frm["Accounts_id"]= Get_Account().id
    Add_Delivery(delivery_frm)

# ----------------------------------------------------------------
def Calc_Acc_Totals(total_amount, total_balance, tmp_accs, ref_id) -> list:
    for account in Get_Customer_ByRef_Id(ref_id).Accounts:
        payment = account.Payments[-1]
        total_amount= total_amount + payment.Amount
        total_balance= total_balance + payment.Balance
        tmp_accs.append(dict(account.__dict__))
    tmp_accs.reverse()
    return [{"total_amount"  : total_amount,
            "total_balance"    : total_balance,
            "total_paid" : total_amount - total_balance},
            {"acc_info": tmp_accs}]


