from sales.models.models import *
#Get account details from database

def Get_Accounts(id):
    db_accounts =  Accounts_database.query.filter_by(id=id).first()
    accounts_details= {
                    "id":db_accounts.id, "type":db_accounts.Type,
                    "qty":db_accounts.Quantity, "Rem":db_accounts.Remainder,
                    "cDate":db_accounts.Date_Created,'uDate':db_accounts.Date_Updated,
                    'ref':db_accounts.Customers_id, 'user':db_accounts.User
    } 
    return accounts_details          

#Get customer details from database
def Get_Customers(id):
    db_customers = Customers_database.query.filter_by(id=id).first()
    customer_details= { 
                    'id':db_customers.id, 'fname':db_customers.First_Name,
                    'lname':db_customers.Last_Name, 'cNo':db_customers.Contact_No,
                    'tel':db_customers.Tel_No, 'email':db_customers.Email_Address,
                    'stAddress':db_customers.Street_Address, 'area':db_customers.Area,
                    'city':db_customers.City,'country':db_customers.Country,
                    'user':db_customers.User
    }             
    return (customer_details)

#Get product details from database      
def Get_Products():
    #All product items to go on a dropdown list
    all_products= [product.Product_Name for product in Products.query.all()]
    return all_products

def Delivery():
    pass

def Search(searched):
    #Search for customers from database
    searched_customer= []
    results_no= Customers_database.query.filter(Customers_database.id.like('%'+searched+'%') | 
                                                Customers_database.Contact_No.like('%'+searched+'%')|
                                                Customers_database.First_Name.like('%'+searched+'%')|
                                                Customers_database.Last_Name.like('%'+searched+'%')
    ).all()
    for customer in results_no:
        customers={'id':customer.id,'first_name':customer.First_Name, 'last_name':customer.Last_Name, 
                'phone1':customer.Contact_No,'email':customer.Email_Address, 'phone2':customer.Tel_No, 
                'address1':customer.Street_Address, 'address2':customer.Area, 'cDate':str(customer.Date_Created)[0:10],
                'uDate':str(customer.Date_Updated)[0:10], 'user':customer.User
        }
        searched_customer.append([customers])
    return searched_customer

def Search_Acc(target):
    customer= Customers_database.query.filter(Customers_database.id == target).first()
    tmpAcc, t_amount, paid_amount, t_balance= [], [], [], []
    for account in customer.Accounts:
        #sAccounts for searched accounts
        sAccounts= {'id':account.id,'type':account.Type, 'qty':account.Quantity, 
                'rem':account.Remainder, 'deliver':account.Delivered, 'status':account.Status,'cDate':str(account.Date_Created)[0:10],
                'uDate':str(account.Date_Updated)[0:10], 'user':account.User
        }
        tmpAcc.append(sAccounts)
        pay, acc = Search_Payment(sAccounts.get('id'))
        t_amount.append(pay[-1].get('amount'))
        paid_amount.append(pay[-1].get('paid'))
        t_balance.append(pay[-1].get('bal'))
    t_amount, paid_amount, t_balance= sum(t_amount), sum(paid_amount), sum(t_balance)   
    totals= {
            'bal': t_balance, 
            'paid':paid_amount, 
            'total': t_amount
    }
    customer_info= {
                    "id":customer.id, "fname":customer.First_Name, 
                    "lname":customer.Last_Name, "cNo":customer.Contact_No
    }
    Search_Payment(target)
    return tmpAcc, customer_info, totals

def Search_Payment(target):
    tmpPay= []
    account= Accounts_database.query.filter(Accounts_database.id == target).first()
    for pay in account.Payments:
        tmpPayment= {'id':pay.id,'type':pay.Transtion_Type, 'bal':pay.Balance, 
                    'paid':pay.Paid,'amount':pay.Amount, 'status':pay.Status,'cDate':str(pay.Date_Created)[0:10],
                    'uDate':str(pay.Date_Updated)[0:10], 'user':account.User
        }
        tmpPay.append(tmpPayment)
    acc_info= {
        "id": account.id, "type":account.Type, 
        "rem":account.Remainder, "deliver":account.Delivered
    }
    return tmpPay, acc_info