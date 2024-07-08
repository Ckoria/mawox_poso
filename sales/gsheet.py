import pygsheets
import pandas as pd
import requests, os, sys
from flask import redirect, url_for, flash
from pathlib import Path
from sales.models.models import *
from datetime import date, datetime, timedelta
from download_creds import download_file_from_google_drive
from .dash_data import remaining_items
from sales.process import *
from dotenv import load_dotenv

"""
    This module is responsible for taking data from the database
    and add it to the Google Sheets using sheets API
"""


def gsheet_auth() -> None:
    """
        Authentication for Google Sheets
    """
    #current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    load_dotenv()
    if("win" in sys.platform):
        service_file = "\\" + os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    else:
        service_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
    current_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else os.getcwd()
    serv = current_dir + service_file
    download_file_from_google_drive(os.getenv("SERVICE_ACC_CREDS"),  serv)
    s_account = pygsheets.authorize(service_account_file= serv)
    os.remove(serv)
    return s_account.open("Products")


# Working as expected
try:
    SPREADSHEET = gsheet_auth()
except ConnectionError:
    redirect(url_for('main.home'))


# Working as expected
def personal_info(curr_sheet: object, cust_info: dict, fisrt_row: int, last_row: int, id_cell: str) -> None:
    """
        Add personal info for the client
        Args:
            curr_sheet (object): Current Sheet
            cust_info (dict): Contains customer information
            first_row, last_row (int): range where customer information will inserted
            id_cell (str): Cell for customer ID
    """
    customer= [[cust_info.get('First_Name').title()], [cust_info.get('Last_Name').title()],
               [cust_info.get('Area').title()], ["'" + str(cust_info.get('Contact_No'))]]
    curr_sheet.update_values(crange= f"C{fisrt_row}:C{last_row}", values= customer)
    curr_sheet.update_value(id_cell, cust_info.get('Ref_id'))


# Working as expected
def receipt( ref_id: str, curr_account: list, day_scheduled) -> None:
    """
        Adds products and customer details to a list
        Args:
            row_idx (int): Current row to be updated with data
            ref_id (str): Customer ID
            curr_account (list): list of payment details, unit price, qty, bal, paid, total
    """
    all_info = Search_Acc(ref_id).get('acc_details')
    p_type = all_info[1]['acc_info'][0].get('Payments')[0] # Get first payment from DB
    balance = all_info[0].get('total_balance')
    total_amount = all_info[0].get('total_amount')
    header_names= ['ID#', 'Description', 'Qty', 'Unit Price', 'Balance', 'Paid', 'Total']
    data = pd.DataFrame(curr_account,  columns=header_names)
    receipt= SPREADSHEET.worksheet('title','Receipt')
    clear_currsheet(receipt, 13, 28)
    receipt.set_dataframe(data, (12, 1))
    receipt.update_value('C29', str(day_scheduled))
    personal_info(receipt, Get_Customers(ref_id), 7, 10, "G7")
    receipt.update_value("F31", balance)
    receipt.update_value("C28", p_type.Transaction_Type)
    receipt.update_value("F34", total_amount)


# Working as expected
def clear_currsheet(curr_sheet: object, start: int, end: int) -> None:
    """
        Clears all rows for product information in a receipt
        Args:
            curr_sheet (object): the currently active sheet
            start, end (int): Row indices for rows to be cleared
    """
    for c in range(start, end):
        curr_sheet.update_row(c, [c, '-', '', '', '', '', ''])


# Working as expected
def receipt_update(ref_id: str) -> None:
    """
        Clears the receipt and updates the customer information

        Args:
            ref_id (str) : the ID of the customer
    """
    receipt= SPREADSHEET.worksheet('title','Receipt')
    row_idx = 13
    clear_currsheet(receipt, row_idx, 28)
    accs_info= Calc_Acc_Totals(0, 0, [], ref_id)
    balance = accs_info[0].get('total_balance')
    total_amount = accs_info[0].get('total_amount')
    personal_info(receipt, Get_Customers(ref_id), 7, 10, "G7")
    for acc in (accs_info[-1].get('acc_info')):
        pay_info= acc.get('Payments')
        last_updated= pay_info[-1].Date_Updated
        if last_updated != None and ((datetime.today() - last_updated).seconds) <= 180:
            cell_values=[row_idx, acc.get('Type'), acc.get('Quantity'),
            pay_info[-1].Amount/acc.get('Quantity'), pay_info[-1].Balance,
            pay_info[-1].Paid, pay_info[-1].Amount]
            invoice_update(receipt, row_idx, cell_values)
            row_idx +=  1
    receipt.update_value("F31", balance)
    receipt.update_value("C28", pay_info[-1].Transaction_Type)
    receipt.update_value("F34", total_amount)
    flash('The payment has been successfully updated.', category='success')


def cash_in() -> None:
    """
        Get payment information from the database
        and append to a list based on payment type.
        Index 0 Cash, Index 1 Card, Index 2 EFT
    """
    paid_items = {'Blocks' : [0, 0, 0], 'Cement' : [0, 0, 0], 'Poles' : [0, 0, 0],
                  'Lentils' : [0, 0, 0], 'Sand' : [0, 0, 0], 'Delivery' : [0, 0, 0]}
    cashin = SPREADSHEET.worksheet('title','Delivery_Invoice')
    todays_income = get_today_payment(date.today())
    for items in todays_income:
        add_amount_to_item(paid_items, items)
    add_money_to_cashin(paid_items)


def add_amount_to_item(paid_items: dict, items: tuple) -> dict:
    """
        Checks the type of item and adds the amount to the corresponding list

        Args:
            item (db object): contains account information
            paid (float): Amount paid by the customer to be appended on a list for cash in.
            payment_type (str): Cash, Card or EFT
            paid_items (dict): passes list of items to appended
        Return:
            paid_items (dict): Appended items
    """
    if "Blocks" in items[0] or "Part" in items[0]:
        paid_items['Blocks'] = paid_amount(items, paid_items['Blocks'])
    elif "Sand" in items[0] or "Stone" in items[0]:
        paid_items['Sand'] = paid_amount(items, paid_items['Sand'])
    elif "Lint" in items[0]:
        paid_items['Lentils'] = paid_amount(items, paid_items['Lentils'])
    elif "Pole" in items[0]:
        paid_items['Poles'] = paid_amount(items, paid_items['Poles'])
    elif "Del" in items[0]:
        paid_items['Delivery'] = paid_amount(items, paid_items['Delivery'])
    elif "Cement" in items[0]:
        paid_items['Cement'] = paid_amount(items, (paid_items['Cement']))
    return paid_items


def paid_amount(items: tuple, paid_item: list) -> list:
    """Checks the type of payment and allocate it to a corresponding item

    Args:
        payment_type (str): Payment type, Cash, Card or EFT
        paid (float): Actual amount paid for the item
        paid_item (list): The item to be paid

    Returns:
        list: List of amounts paid for the specified items
    """
    if items[2] == "Cash":
        paid_item[0] += items[1]
    elif items[2] == "Card":
        paid_item[1] += items[1]
    elif items[2] == "EFT":
        paid_item[2] += items[1]
    return paid_item


def add_money_to_cashin(paid_items: dict) -> None:
    """
        Converts dictionary with sum of paid amount to dataframe
        then set dataframe to google sheets
    Args:
        cashin (object): Google sheet where the amount is stored
        paid_items (dict): All amounts paid with corresponding headers
    """
    cashin = SPREADSHEET.worksheet('title', 'Cash-In')
    paid_items= pd.DataFrame(paid_items)
    cashin.set_dataframe(paid_items, (3, 2))


def delivery_to_invoice(ref_id: str, get_delivered_info: list, payment: dict,
                        scheduled_day: date, driver:str) -> None:
    """
        Passes the customer information to the invoice on Google Sheet
        Get account details using customer ID and pass it to the invoice
    Args:
        info (dict): Contains customer information

    """
    balance = payment.get('total_balance')
    header_names= ['Type', 'Delivered', 'Remainder', 'Total']
    invoice = SPREADSHEET.worksheet('title','Delivery_Invoice')
    clear_currsheet(invoice, 15, 30)
    personal_info(invoice, Get_Customers(ref_id), 9, 12, "D6")
    get_delivered_info = pd.DataFrame(get_delivered_info, columns= header_names)
    invoice.set_dataframe(get_delivered_info , (14, 2))
    invoice.update_value("E31", balance)
    invoice.update_value("C33", driver.title())
    invoice.update_value("D32", str(scheduled_day))


def invoice_update(invoice: object, row_idx: int, item_details: list):
    """
        Update details to the invoice
        Args:
            invoice (obj): Current Sheet
            row_idx (int): Row number where data will be inserted
            item_details (list): List of delivery info per row
    """
    invoice.update_row(row_idx, item_details)


def products_to_gsheets(product_type: str) -> None:
    products = remaining_items(product_type)
    header_names= ['ID', 'Name', 'Last', 'Amount Paid', 'Remainder', 'Quantity',
    'Balance', 'Date Created', 'Last Updated']
    data= pd.DataFrame(products, columns=header_names)
    date_columns = [col for col in data.columns if 'Date_Updated' in col]
    data[date_columns] = data[date_columns].apply(pd.to_datetime)
    data.sort_values(by=date_columns, ascending=False, inplace=True)
    data = data.groupby('ID').head(1)
    backlog = SPREADSHEET.worksheet('title', product_type.title())
    backlog.set_dataframe(data,(2,1))
    sa_time = datetime.now() + timedelta(minutes = 120)
    backlog.update_value('H1', str(sa_time)[:16])


def switch_backlog_sheets():
    backlog_sheets = ['cement', 'sand', 'blocks', 'lintels', 'partition', 'delivery', 'poles']
    for product_type in backlog_sheets:
        start = datetime.now()
        products_to_gsheets(product_type)
    return datetime.now() - start


def record_xpenses():
    all_xpenses = Get_All_Expenses()
    xpenses = all_xpenses.get('expenses')
    xpensez = SPREADSHEET.worksheet('title', 'Xpenses')
    xpenses = pd.DataFrame(xpenses)
    try:
        xpenses = xpenses.drop(['_sa_instance_state', 'id'], axis=1)
    except KeyError:
        xpenses = xpenses
    xpensez.set_dataframe(xpenses, (3, 1))

def saveToPDF():
    # 
    web_app_url = os.getenv("WEB_URL")

    response = requests.get(web_app_url)

    if response.status_code == 200:
        print(response.content)
        flash("Successfully saved to Google Drive")
    else:
        flash("Failed to save the recept! ")

