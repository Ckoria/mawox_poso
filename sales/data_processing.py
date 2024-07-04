import sqlite3


def db_connexion():
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/sales_data.db')

    # Create a cursor object to execute SQL queries
    return conn


queries = {
    "customers": {
        
    },
    "accounts": {

    },
    "payments": {

    },
    "notes": {

    },
    "by_date": "SELECT * FROM {} WHERE Date_Created LIKE {}",
    "relational_queries": {
        "remainders": """SELECT Accounts_database.Type 
        FROM {} INNER JOIN {} 
        WHERE {}.id = {}.id AND {}.Balance = 0 
        ORDER BY  Accounts_database.id desc 
        LIMIT 10""",
        
        "all": """SELECT cd.Ref_id, cd.Last_Name, cd.Contact_No, cd.Area,
        ad.Type, ad.Quantity, ad.Remainder, ad.Delivered, ad.Delivery_Schedule, ad.Status, ad.Date_Created,
        pd.Transaction_Type, pd.Paid, pd.Balance, pd.Status, pd.Date_Created, cd.User
        FROM Customers_database as cd 
        JOIN Accounts_database as ad ON cd.Ref_id = ad.Customers_id 
        JOIN Payments_database as pd ON pd.Accounts_id = ad.id
        ORDER BY ad.Date_Created DESC"""    
    }
}