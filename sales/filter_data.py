from operator import index
from sales.data_processing import db_connexion, queries
import json, pandas as pd


db_connection = db_connexion()

def read_json(json_file: json) -> dict:
    with open(json_file, "r") as file:
        data = json.load(file)
    return data

data = read_json("filter_queries.json")

def customers():
    return execute_db()


def accounts():
    pass
    

def payments():
    pass
    
    
def deliveries():
    pass

    
def relational_queries():
    bal = queries['relational_queries']['remainders']
    all_data = queries['relational_queries']['all']
    return execute_db(all_data)


def execute_db(command: str):
    global db_connection
    try:
        db_cursor = db_connection.cursor()
        data_obj = db_cursor.execute(command)
        return data_obj.fetchall()
    
    finally:
        db_cursor.close()
        db_connection.close()


def create_csv(data):
    import csv
    
    csv_file = 'mawox.csv'
    # Writing the list to a CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

data = relational_queries()
create_csv(data)

df_data = pd.DataFrame(data= data, columns=[
    'Ref_id', 'Last_Name', 'Contact_No', 'Area', 
    'Type', 'Quantity', 'Remainder', 'Delivered','Delivery_Schedule','Acc_Status', 'Acc_Date_Created',
    'Transaction_Type', 'Paid', 'Balance', 'P_Status', 'Pay_Date_Created', 'User'
    ])
