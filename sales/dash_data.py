from sales.models.models import *
from datetime import date, time
from .process import my_days, Get_Customer_ByRef_Id, Get_Customers, Last_Payment_Details
import pandas as pd
from flask import flash



list_of_products= ["Blocks", "Cement", "Sand","Partition", "Poles","Lintels"]

def filter_products(product_type, start_date, end_date):

    target_item = f"%{product_type}%"
    products_data = Accounts_database.query.filter(Accounts_database.Type.like(target_item),
                                             Accounts_database.Date_Created.between( start_date, end_date)
                                            ).all()

    return sum([qty.Quantity for qty in products_data])


def created_accounts(start_date, last_date):
    recent_accounts = Accounts_database.query.filter(
                        Accounts_database.Date_Created.between(
                            start_date, last_date)
                            ).count()
    return recent_accounts


def number_of_sales():
    recent_accs, product_qty, last_six_months = [], [], []
    global list_of_products
    last_date= date.today()
    y, m= last_date.year, last_date.month
    for c in range(1, 7):
        n = ((m - c) % 12) + 1
        #Switch to previous year if month is greater than 12
        if n > m:
            y = (date.today()).year - 1
        start_date = date(y, n, 1)
        recent_accs.append(created_accounts(start_date, last_date)) #LIST FOR RECENTLY CREATED ACCOUNTS GROUPED BY MONTH CREATED
        search_items = [ filter_products(item, start_date, last_date) for item in list_of_products ] #
        product_qty.append(search_items)
        last_date= start_date
        last_six_months.append(start_date.strftime("%B"))
    return {'products_data':{
            'results': (product_qty),
            'products': list_of_products,
            'months': last_six_months,
            'recent_accounts': recent_accs
            }
        }


def today_schedule(target_date: date) -> list:
    item_type = f'%{"Blocks"}%'
    return sheduled_customers(Accounts_database.query.filter(
        Accounts_database.Type.like(item_type),
        Accounts_database.Delivery_Schedule == target_date
            ).all())


def sheduled_customers(schedule: list) -> list:
    return [Get_Customers(account.Customers_id) for account in schedule]


def recent_customers():
    last_day, curr_date = my_days()
    return Customers_database.query.filter(
            Customers_database.Date_Created.between(
            date(curr_date.year, curr_date.month, 1),
            date(curr_date.year, curr_date.month, last_day))
            ).order_by(Customers_database.Date_Updated.desc()).all()

def active_accounts(status: str, item_type: str) -> list:
    accounts_active= Accounts_database.query.filter(
                        Accounts_database.Status == status, Accounts_database.Type != item_type ).order_by(
                            Accounts_database.Date_Updated.desc()).all()  #paginate(per_page= 30)
    return accounts_active


def Active_Customers(accounts_active: list, customers: list) -> list:
    for account in accounts_active[:50]:
        customer = Get_Customer_ByRef_Id(account.Customers_id)
        if customer not in customers:
            customers.append(customer)
    return [dict(cust.__dict__) for cust in customers]


def Unrecovered_Balances():
    payment_balance=  db.session.query(Payments_database.Balance
                            ).join(Accounts_database).join(Customers_database). \
            filter(
                Payments_database.Balance > 0,
                Accounts_database.Remainder == 0
                ).all()
    return [float(amount[0]) for amount in payment_balance]


def remaining_items(item_type) -> list:
    oustanding_accounts=  db.session.query(Customers_database.Ref_id,
                                       Customers_database.First_Name,
                                       Customers_database.Last_Name,
                                       Payments_database.Amount - Payments_database.Balance,
                                       Accounts_database.Remainder,
                                       Accounts_database.Quantity,
                                       Payments_database.Balance,
                                       Accounts_database.Date_Created,
                                       Accounts_database.Date_Updated
                            ).join(Payments_database).join(Customers_database). \
            filter(
                Accounts_database.Type.like('%'+item_type+'%'),
                Accounts_database.Status == 'Active').all()
    return oustanding_accounts



